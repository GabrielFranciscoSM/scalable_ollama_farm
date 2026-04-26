#!/bin/sh
# Pull the embedding model used by LiteLLM for semantic cache lookups.

set -e

echo "[ollama-embed-init] Pulling nomic-embed-text ..."
ollama pull nomic-embed-text

echo "[ollama-embed-init] Done. nomic-embed-text is ready."