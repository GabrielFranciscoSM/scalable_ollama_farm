"""
Semantic cache research test suite.

Tests cache hit/miss by sending prompts to LiteLLM and reading
cache status directly from the LiteLLM container logs (since the
semantic cache doesn't set x-litellm-cache-hit response headers).

Usage:
    uv run python test_litellm.py
"""

import os
import re
import subprocess
import time
import statistics
from dataclasses import dataclass, field
from typing import Optional

import httpx
from rich.console import Console
from rich.table import Table

BASE_URL = "http://localhost/v1"
API_KEY  = os.getenv("LITELLM_MASTER_KEY", "sk-fase0-local")
MODEL    = "qwen3"

client = httpx.Client(base_url=BASE_URL, timeout=120)
console = Console()


@dataclass
class Result:
    prompt: str
    latency_ms: float
    cache_hit: Optional[bool]
    deployment: str
    response_preview: str
    group: str = ""


@dataclass
class ExperimentGroup:
    name: str
    description: str
    prompts: list[str]
    no_cache: bool = False
    results: list[Result] = field(default_factory=list)


# ── Log-based cache detection ────────────────────────────────────────────────
# LiteLLM does NOT set x-litellm-cache-hit for semantic cache. Instead we read
# "Cache Hit!" lines from the container logs. This is reliable because:
#   - "Cache Hit!" is logged synchronously BEFORE the HTTP response is sent
#   - We snapshot before request, snapshot after, and check if count increased

def _snapshot() -> tuple[int, dict[str, int]]:
    """Return (total_cache_hits, {deployment_name: request_count})."""
    r = subprocess.run(
        ["docker", "compose", "logs", "litellm", "--no-log-prefix"],
        capture_output=True, text=True, timeout=15,
    )
    log = r.stdout
    hits = log.count("Cache Hit!")
    d1 = log.count("api_base='http://ollama-1:11434'")
    d2 = log.count("api_base='http://ollama-2:11434'")
    return hits, {"ollama-1": d1, "ollama-2": d2}


def _last_ollama_deployment() -> str:
    """Return the last Ollama api_base that handled a completion."""
    r = subprocess.run(
        ["docker", "compose", "logs", "litellm", "--no-log-prefix"],
        capture_output=True, text=True, timeout=15,
    )
    matches = re.findall(r"api_base='(http://ollama-\d:11434)'", r.stdout)
    return matches[-1][0] if matches else "unknown"


# ── Helpers ──────────────────────────────────────────────────────────────────

def send_prompt(prompt: str, no_cache: bool = False) -> dict:
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100,
    }
    if no_cache:
        body["cache"] = {"no-cache": True}

    resp = client.post(
        "/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json=body,
    )
    resp.raise_for_status()
    return resp.json()


# ── Experiment groups ─────────────────────────────────────────────────────────
# Each group uses unique seed prompts to avoid cross-contamination.

def _exact_duplicates() -> ExperimentGroup:
    """10 different topics × 2 identical prompts — second MUST always be HIT."""
    topics = [
        "What is the boiling point of water?",
        "What is the atomic number of carbon?",
        "What is the square root of 144?",
        "What is the freezing point of water?",
        "What is the pH of pure water?",
        "What is the density of water?",
        "What is the speed of sound?",
        "What is the chemical symbol for gold?",
        "What is the value of pi to 3 decimal places?",
        "What is the chemical formula of methane?",
    ]
    prompts = [p for topic in topics for p in (topic, topic)]
    return ExperimentGroup(
        name="Exact duplicates",
        description="10 topics × 2 identical prompts — second MUST always be HIT.",
        prompts=prompts,
    )


def _paraphrase_geography() -> ExperimentGroup:
    """5 geography topics × 3 closely related phrasings."""
    return ExperimentGroup(
        name="Paraphrase — Geography",
        description="5 geography topics × 3 phrasings — prompt 2+ should HIT.",
        prompts=[
            "What is the capital of France?",
            "What is the capital city of France?",
            "Which city serves as the capital of France?",
            "What is the longest river in the world?",
            "Which river is the longest in the world?",
            "What is the world's longest river?",
            "How many continents are there on Earth?",
            "What is the number of continents on Earth?",
            "How many continents exist on Earth?",
            "What is the largest ocean on Earth?",
            "Which ocean is the largest on Earth?",
            "What is the biggest ocean in the world?",
            "What is the tallest mountain in the world?",
            "Which mountain is the highest on Earth?",
            "What is the highest peak in the world?",
        ],
    )


def _paraphrase_science() -> ExperimentGroup:
    """5 science topics × 3 closely related phrasings."""
    return ExperimentGroup(
        name="Paraphrase — Science",
        description="5 science topics × 3 phrasings — prompt 2+ should HIT.",
        prompts=[
            "How does photosynthesis work?",
            "Explain the process of photosynthesis",
            "What happens during photosynthesis?",
            "How many planets are in our solar system?",
            "What is the number of planets orbiting the sun?",
            "How many planets orbit our sun?",
            "What is gravity?",
            "How does gravity work?",
            "What force pulls objects toward Earth?",
            "What gas do plants absorb from the atmosphere?",
            "Which gas do plants take in from the air?",
            "What gas is absorbed by plants during photosynthesis?",
            "How does sound travel?",
            "How does sound propagate through air?",
            "What is the mechanism by which sound travels?",
        ],
    )


def _paraphrase_history() -> ExperimentGroup:
    """5 history/arts topics × 3 closely related phrasings."""
    return ExperimentGroup(
        name="Paraphrase — History & Arts",
        description="5 history/arts topics × 3 phrasings — prompt 2+ should HIT.",
        prompts=[
            "Who painted the Mona Lisa?",
            "Who was the artist of the Mona Lisa?",
            "Who created the Mona Lisa painting?",
            "When did World War II end?",
            "What year did World War II end?",
            "When was the end of World War II?",
            "Who wrote Romeo and Juliet?",
            "Who was the author of Romeo and Juliet?",
            "Who penned Romeo and Juliet?",
            "What is the Great Wall of China?",
            "Describe the Great Wall of China",
            "What is the Great Wall of China made of?",
            "Who discovered penicillin?",
            "Who discovered the antibiotic penicillin?",
            "Who is credited with discovering penicillin?",
        ],
    )


def _related_distinct() -> ExperimentGroup:
    """3 topics × 3 different facts asked about each — must NOT cross-hit."""
    return ExperimentGroup(
        name="Related but distinct",
        description="Same domain, different facts — should MISS at 0.85.",
        prompts=[
            "What is a list in Python?",
            "How do you sort a list in Python?",
            "What is a dictionary in Python?",
            "What temperature should you bake bread at?",
            "How long does it take to bake bread?",
            "What ingredients are in bread dough?",
            "How long is a football match?",
            "How many players are on a football team?",
            "What is offside in football?",
        ],
    )


def _unrelated() -> ExperimentGroup:
    """Diverse single prompts that share no domain — must never HIT."""
    return ExperimentGroup(
        name="Unrelated (cross-check)",
        description="Completely different topics — must never hit cache.",
        prompts=[
            "What is the speed of light?",
            "Who invented the telephone?",
            "Explain how a lever works.",
            "What is the boiling point of ethanol?",
            "How do vaccines work?",
        ],
    )


def _load_balancing() -> ExperimentGroup:
    """10 identical requests with cache OFF — shows request distribution."""
    return ExperimentGroup(
        name="Load balancing probe",
        description="10 identical requests with cache OFF — shows request distribution.",
        prompts=["Say hello in one word."] * 10,
        no_cache=True,
    )


EXPERIMENTS: list[ExperimentGroup] = [
    _exact_duplicates(),
    _paraphrase_geography(),
    _paraphrase_science(),
    _paraphrase_history(),
    _related_distinct(),
    _unrelated(),
    _load_balancing(),
]

# ── Cache reset ────────────────────────────────────────────────────────────────

def reset_cache() -> None:
    """Drop Redis semantic index and restart LiteLLM so the index is recreated.

    FT.DROPINDEX deletes hash keys asynchronously — the old keys can
    still be picked up by the recreated index, so we FLUSHDB first.
    """
    console.print("[bold]Resetting Redis semantic cache ...[/bold]")
    subprocess.run(
        ["docker", "compose", "exec", "redis", "redis-cli", "FLUSHDB"],
        capture_output=True, text=True, timeout=15,
    )
    subprocess.run(
        ["docker", "compose", "restart", "litellm"],
        capture_output=True, text=True, timeout=60,
    )
    # Wait for litellm to be healthy
    for _ in range(30):
        try:
            r = httpx.post(
                f"{BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {API_KEY}"},
                json={"model": MODEL, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 1},
                timeout=10,
            )
            if r.status_code < 500:
                break
        except Exception:
            pass
        time.sleep(2)
    console.print("[green]  Cache reset done.[/green]\n")


# ── Warmup ───────────────────────────────────────────────────────────────────

WARMUP_PROMPTS = [
    "Count from one to five.",
    "What color is the sky?",
    "Is water wet?",
    "Tell me a joke.",
]


def warmup() -> None:
    console.print("[bold]Warming up models ...[/bold]")
    for p in WARMUP_PROMPTS:
        start = time.perf_counter()
        client.post(
            "/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": MODEL, "messages": [{"role": "user", "content": p}], "max_tokens": 10},
        )
        console.print(f"  warmup: {p}  ({((time.perf_counter()-start)*1000):.0f} ms)")
    console.print()


# ── Main runner ──────────────────────────────────────────────────────────────

def run_experiments() -> list[Result]:
    all_results: list[Result] = []

    for experiment in EXPERIMENTS:
        console.rule(f"[bold]{experiment.name}")
        console.print(f"[dim]{experiment.description}[/dim]\n")

        for i, prompt in enumerate(experiment.prompts):
            label = f"  [{i+1}/{len(experiment.prompts)}] {prompt[:60]}..."
            console.print(label, end="")

            # Snapshot cache & deployment counts before request
            hits_before, depl_before = _snapshot()

            start = time.perf_counter()
            data = send_prompt(prompt, no_cache=experiment.no_cache)
            latency_ms = (time.perf_counter() - start) * 1000

            # Snapshot after request
            hits_after, depl_after = _snapshot()

            # Determine if this request was a cache hit
            delta_hits = hits_after - hits_before
            cache_hit = delta_hits > 0

            # Determine which deployment handled this request
            delta_1 = depl_after.get("ollama-1", 0) - depl_before.get("ollama-1", 0)
            delta_2 = depl_after.get("ollama-2", 0) - depl_before.get("ollama-2", 0)
            if delta_1 > 0:
                deployment = "ollama-1"
            elif delta_2 > 0:
                deployment = "ollama-2"
            else:
                deployment = _last_ollama_deployment()

            content = data["choices"][0]["message"]["content"]
            result = Result(
                prompt=prompt,
                latency_ms=latency_ms,
                cache_hit=cache_hit,
                deployment=deployment.replace("http://", "").replace(":11434", ""),
                response_preview=content[:80].replace("\n", " "),
                group=experiment.name,
            )
            experiment.results.append(result)
            all_results.append(result)

            hit_tag = "[green]HIT[/green]" if cache_hit else "[yellow]MISS[/yellow]"
            console.print(f"  {hit_tag}  {result.latency_ms:7.0f} ms  [{result.deployment}]")

        console.print()

    return all_results


# ── Reporting ────────────────────────────────────────────────────────────────

def print_summary(results: list[Result]) -> None:
    console.rule("[bold]Per-request results")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Group", style="dim", width=26)
    table.add_column("Prompt", width=36)
    table.add_column("Cache", justify="center", width=6)
    table.add_column("Deploy", width=10)
    table.add_column("Latency", justify="right", width=10)

    for r in results:
        hit_str = "H" if r.cache_hit else "M"
        hit_style = "green" if r.cache_hit else "yellow"
        table.add_row(
            r.group[:25],
            r.prompt[:34] + "..." if len(r.prompt) > 34 else r.prompt,
            f"[{hit_style}]{hit_str}[/{hit_style}]",
            r.deployment,
            f"{r.latency_ms:.0f}",
        )
    console.print(table)

    # Aggregate stats
    hits = [r for r in results if r.cache_hit]
    misses = [r for r in results if not r.cache_hit]
    console.print()
    if hits:
        hl = [r.latency_ms for r in hits]
        console.print(f"[green]Cache HIT  [/green] avg={statistics.mean(hl):.0f} ms  "
                      f"median={statistics.median(hl):.0f} ms  n={len(hits)}")
    if misses:
        ml = [r.latency_ms for r in misses]
        console.print(f"[yellow]Cache MISS [/yellow] avg={statistics.mean(ml):.0f} ms  "
                      f"median={statistics.median(ml):.0f} ms  n={len(misses)}")
    if hits and misses:
        speedup = statistics.mean(ml) / statistics.mean(hl)
        console.print(f"\n[bold]Cache speedup: {speedup:.1f}×[/bold]")

    # Deployment distribution
    console.rule("[bold]Load balancing distribution")
    depl = {"ollama-1": 0, "ollama-2": 0}
    for r in results:
        if r.deployment in depl:
            depl[r.deployment] += 1
    total = sum(depl.values())
    if total:
        for name, count in sorted(depl.items()):
            pct = count / total * 100
            bar = "█" * max(1, int(pct / 5)) + "░" * (20 - max(1, int(pct / 5))) if pct > 0 else "░" * 20
            console.print(f"  {name:12s} {count:4d} req  {bar} {pct:.0f}%")
        console.print(f"  {'TOTAL':12s} {total:4d} req")


if __name__ == "__main__":
    console.print("[bold cyan]Semantic Cache Research — LiteLLM + Ollama + Redis[/bold cyan]\n")
    reset_cache()
    warmup()
    results = run_experiments()
    print_summary(results)
