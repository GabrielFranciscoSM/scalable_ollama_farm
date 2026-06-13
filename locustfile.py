"""
Locust load test for LLM Farm with semantic cache.

Usage:
    # Sustained load test (5 users, 5 minutes, sin reset de caché):
    uv run locust --headless -u 5 -r 2 --run-time 5m --csv=locust_results

    # Benchmark limpio (resetea caché primero):
    CACHE_RESET=1 uv run locust --headless -u 5 -r 2 --run-time 5m --csv=locust_results

    # Prueba de balanceo (sin caché):
    NO_CACHE=1 uv run locust --headless -u 5 -r 2 --run-time 3m --csv=locust_lb

    # Web UI interactiva:
    uv run locust

Variables de entorno:
    LOCUST_HOST    : Base URL (default: http://localhost)
    API_KEY        : LiteLLM API key (default: sk-fase0-local)
    MODEL          : Model name (default: qwen3)
    CACHE_RESET    : "1" para resetear Redis antes de empezar
    NO_CACHE       : "1" para desactivar caché (prueba de balanceo puro)
"""

import os
import subprocess
import time
import random

import httpx
from locust import HttpUser, task, between, events


HOST = os.getenv("LOCUST_HOST", "http://localhost")
API_KEY = os.getenv("API_KEY", "sk-fase0-local")
MODEL = os.getenv("MODEL", "qwen3")
NO_CACHE = os.getenv("NO_CACHE") == "1"

# ── Prompts de cada grupo ────────────────────────────────────────────

EXACT_TOPICS = [
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

PARA_GEO = [
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
]

PARA_SCI = [
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
]

PARA_HIST = [
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
]

RELATED = [
    "What is a list in Python?",
    "How do you sort a list in Python?",
    "What is a dictionary in Python?",
    "What temperature should you bake bread at?",
    "How long does it take to bake bread?",
    "What ingredients are in bread dough?",
    "How long is a football match?",
    "How many players are on a football team?",
    "What is offside in football?",
]

UNRELATED = [
    "What is the speed of light?",
    "Who invented the telephone?",
    "Explain how a lever works.",
    "What is the boiling point of ethanol?",
    "How do vaccines work?",
]

WARMUP = [
    "Count from one to five.",
    "What color is the sky?",
    "Is water wet?",
    "Tell me a joke.",
]


def _reset_cache():
    print("[setup] Resetting Redis semantic cache ...")
    subprocess.run(
        ["docker", "compose", "exec", "redis", "redis-cli", "FLUSHDB"],
        capture_output=True, text=True, timeout=15,
    )
    subprocess.run(
        ["docker", "compose", "restart", "litellm"],
        capture_output=True, text=True, timeout=60,
    )
    for _ in range(30):
        try:
            r = httpx.post(
                f"{HOST}/v1/chat/completions",
                headers={"Authorization": f"Bearer {API_KEY}"},
                json={"model": MODEL, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 1},
                timeout=10,
            )
            if r.status_code < 500:
                break
        except Exception:
            pass
        time.sleep(2)
    print("[setup] Cache reset done.")


@events.init.add_listener
def on_locust_init(environment, **kwargs):
    if os.getenv("CACHE_RESET") == "1":
        _reset_cache()
    mode = "NO-CACHE" if NO_CACHE else "CACHE"
    print(f"[setup] Target: {HOST}/v1 | Model: {MODEL} | Mode: {mode}")


# ── Helper ───────────────────────────────────────────────────────────

def make_body(prompt: str) -> dict:
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100,
    }
    if NO_CACHE:
        body["cache"] = {"no-cache": True}
    return body


# ── User class ───────────────────────────────────────────────────────

class LLMFarmUser(HttpUser):
    host = HOST
    wait_time = between(1.0, 3.0)

    def on_start(self):
        for p in WARMUP:
            self.client.post(
                "/v1/chat/completions",
                json=make_body(p),
                headers={"Authorization": f"Bearer {API_KEY}"},
                name="[warmup]",
            )

    @task(10)
    def exact_duplicates(self):
        topic = random.choice(EXACT_TOPICS)
        self.client.post(
            "/v1/chat/completions",
            json=make_body(topic),
            headers={"Authorization": f"Bearer {API_KEY}"},
            name="exact_dup",
        )
        self.client.post(
            "/v1/chat/completions",
            json=make_body(topic),
            headers={"Authorization": f"Bearer {API_KEY}"},
            name="exact_dup",
        )

    @task(5)
    def paraphrase_geography(self):
        prompt = random.choice(PARA_GEO)
        self.client.post(
            "/v1/chat/completions",
            json=make_body(prompt),
            headers={"Authorization": f"Bearer {API_KEY}"},
            name="paraphrase_geo",
        )

    @task(5)
    def paraphrase_science(self):
        prompt = random.choice(PARA_SCI)
        self.client.post(
            "/v1/chat/completions",
            json=make_body(prompt),
            headers={"Authorization": f"Bearer {API_KEY}"},
            name="paraphrase_sci",
        )

    @task(5)
    def paraphrase_history(self):
        prompt = random.choice(PARA_HIST)
        self.client.post(
            "/v1/chat/completions",
            json=make_body(prompt),
            headers={"Authorization": f"Bearer {API_KEY}"},
            name="paraphrase_hist",
        )

    @task(3)
    def related_distinct(self):
        prompt = random.choice(RELATED)
        self.client.post(
            "/v1/chat/completions",
            json=make_body(prompt),
            headers={"Authorization": f"Bearer {API_KEY}"},
            name="related_distinct",
        )

    @task(2)
    def unrelated(self):
        prompt = random.choice(UNRELATED)
        self.client.post(
            "/v1/chat/completions",
            json=make_body(prompt),
            headers={"Authorization": f"Bearer {API_KEY}"},
            name="unrelated",
        )

    @task(2)
    def load_balancing(self):
        """Probe de balanceo: siempre MISS (no_cache) para ver distribución."""
        body = make_body("Say hello in one word.")
        body["cache"] = {"no-cache": True}
        self.client.post(
            "/v1/chat/completions",
            json=body,
            headers={"Authorization": f"Bearer {API_KEY}"},
            name="load_balance",
        )
