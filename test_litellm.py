"""
Semantic cache research test suite.

Tests cache hit/miss behaviour by sending semantically similar prompts
to LiteLLM and observing response times and cache headers.

Usage:
    pip install openai httpx rich
    python tests/research.py
"""

import time
import statistics
from dataclasses import dataclass, field
from typing import Optional

import httpx
from openai import OpenAI
from rich.console import Console
from rich.table import Table

# ── Config ────────────────────────────────────────────────────────────────────

BASE_URL = "http://localhost/v1"      # via Nginx
API_KEY  = "sk-research-local-1234"  # must match litellm config master_key
MODEL    = "qwen3"

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
console = Console()

# ── Data structures ───────────────────────────────────────────────────────────

@dataclass
class Result:
    prompt: str
    latency_ms: float
    cache_hit: Optional[str]
    response_preview: str
    group: str = ""

@dataclass
class ExperimentGroup:
    name: str
    description: str
    prompts: list[str]
    results: list[Result] = field(default_factory=list)

# ── Helpers ───────────────────────────────────────────────────────────────────

def send_prompt(prompt: str, group: str = "") -> Result:
    """Send a completion request and capture latency + cache headers."""
    start = time.perf_counter()

    # Use the raw httpx client so we can inspect response headers
    with httpx.Client(base_url=BASE_URL, timeout=120) as http:
        resp = http.post(
            "/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 100,
            },
        )
        resp.raise_for_status()
        data = resp.json()

    latency_ms = (time.perf_counter() - start) * 1000
    cache_hit  = resp.headers.get("x-litellm-cache-hit") or resp.headers.get("x-cache-hit")
    content    = data["choices"][0]["message"]["content"]

    return Result(
        prompt=prompt,
        latency_ms=latency_ms,
        cache_hit=cache_hit,
        response_preview=content[:80].replace("\n", " "),
        group=group,
    )

# ── Experiment groups ─────────────────────────────────────────────────────────

EXPERIMENTS: list[ExperimentGroup] = [
    ExperimentGroup(
        name="Exact duplicate",
        description="Same prompt sent twice — expect cache hit on second call.",
        prompts=[
            "What is the capital of France?",
            "What is the capital of France?",
        ],
    ),
    ExperimentGroup(
        name="Paraphrase (high similarity)",
        description="Semantically identical, different wording — tests similarity threshold.",
        prompts=[
            "What is the capital of France?",
            "Which city serves as the capital of France?",
            "Tell me the capital city of France.",
        ],
    ),
    ExperimentGroup(
        name="Related but distinct (medium similarity)",
        description="Same topic, different question — may or may not hit cache depending on threshold.",
        prompts=[
            "What is the capital of France?",
            "What is the population of Paris?",
            "What language is spoken in France?",
        ],
    ),
    ExperimentGroup(
        name="Unrelated (low similarity)",
        description="Completely different topics — should never hit cache.",
        prompts=[
            "What is the capital of France?",
            "How does photosynthesis work?",
            "Explain the rules of chess.",
        ],
    ),
    ExperimentGroup(
        name="Load balancing probe",
        description="10 identical requests to observe load balancing across Ollama instances.",
        prompts=["Say hello in one word."] * 10,
    ),
]

# ── Main runner ───────────────────────────────────────────────────────────────

def run_experiments() -> list[Result]:
    all_results: list[Result] = []

    for experiment in EXPERIMENTS:
        console.rule(f"[bold]{experiment.name}")
        console.print(f"[dim]{experiment.description}[/dim]\n")

        for i, prompt in enumerate(experiment.prompts):
            label = f"  [{i+1}/{len(experiment.prompts)}] {prompt[:60]}..."
            console.print(label, end="")

            result = send_prompt(prompt, group=experiment.name)
            experiment.results.append(result)
            all_results.append(result)

            hit_tag = "[green]HIT[/green]" if result.cache_hit == "True" else "[yellow]MISS[/yellow]" if result.cache_hit == "False" else "[dim]?[/dim]"
            console.print(f"  {hit_tag}  {result.latency_ms:7.0f} ms")

        console.print()

    return all_results

def print_summary(results: list[Result]) -> None:
    console.rule("[bold]Summary")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Group", style="dim", width=28)
    table.add_column("Prompt", width=38)
    table.add_column("Cache", justify="center", width=6)
    table.add_column("Latency (ms)", justify="right", width=13)

    for r in results:
        hit_str = "✓" if r.cache_hit == "True" else "✗" if r.cache_hit == "False" else "?"
        hit_style = "green" if r.cache_hit == "True" else "yellow" if r.cache_hit == "False" else "dim"
        table.add_row(
            r.group,
            r.prompt[:36] + "..." if len(r.prompt) > 36 else r.prompt,
            f"[{hit_style}]{hit_str}[/{hit_style}]",
            f"{r.latency_ms:.0f}",
        )

    console.print(table)

    # Latency stats by cache status
    hits   = [r.latency_ms for r in results if r.cache_hit == "True"]
    misses = [r.latency_ms for r in results if r.cache_hit == "False"]

    console.print()
    if hits:
        console.print(f"[green]Cache HIT  [/green] avg={statistics.mean(hits):.0f} ms  "
                      f"median={statistics.median(hits):.0f} ms  n={len(hits)}")
    if misses:
        console.print(f"[yellow]Cache MISS [/yellow] avg={statistics.mean(misses):.0f} ms  "
                      f"median={statistics.median(misses):.0f} ms  n={len(misses)}")
    if hits and misses:
        speedup = statistics.mean(misses) / statistics.mean(hits)
        console.print(f"\n[bold]Cache speedup: {speedup:.1f}×[/bold]")


if __name__ == "__main__":
    console.print("[bold cyan]Semantic Cache Research — LiteLLM + Ollama + Redis[/bold cyan]\n")
    all_results = run_experiments()
    print_summary(all_results)