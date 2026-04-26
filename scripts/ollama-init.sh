#!/bin/sh
# Pull the inference model. Runs once at container startup.
# The model will be cached in the named volume, so subsequent starts are fast.

set -e

echo "[ollama-init] Pulling qwen3:0.8b ..."
ollama pull qwen3.5:0.8b

echo "[ollama-init] Done. qwen3.5:0.8b is ready."