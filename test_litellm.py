#!/usr/bin/env python3

import json
import os
import sys
import urllib.error
import urllib.request

API_URL = os.getenv("LITELLM_URL", "http://localhost:8088/v1/chat/completions")
API_KEY = os.getenv("LITELLM_MASTER_KEY", "sk-fase0-local")
MODEL = os.getenv("LITELLM_MODEL", "local-chat")
THINK = os.getenv("LITELLM_THINK", "false").lower() == "true"
PROMPT = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Say hello in Spanish"

payload = {
    "model": MODEL,
    "messages": [{"role": "user", "content": PROMPT}],
    "max_tokens": 40,
    "think": THINK,
}

request = urllib.request.Request(
    API_URL,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    method="POST",
)

try:
    with urllib.request.urlopen(request, timeout=60) as response:
        body = response.read().decode("utf-8")
        parsed = json.loads(body)
        message = parsed["choices"][0]["message"]["content"]
        print("Model:", parsed.get("model", MODEL))
        print("Reply:", message)
except urllib.error.HTTPError as error:
    print(f"HTTP {error.code}: {error.reason}")
    print(error.read().decode("utf-8", errors="replace"))
    sys.exit(1)
except Exception as error:
    print("Request failed:", error)
    sys.exit(1)
