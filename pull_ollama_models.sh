#!/bin/bash

set -u

MODELS=(
  "qwen3.5:0.8b"
  "gemma3:1b"
  "llama3.2:3b"
  "phi4-mini"
  "gemma3:4b"
  "qwen3.5:9b"
  "gemma3:12b"
  "phi4:14b"
)

MIN_REQS=(
  "2 GB RAM or 1 GB VRAM"
  "3 GB RAM or 2 GB VRAM"
  "6 GB RAM or 4 GB VRAM"
  "6 GB RAM or 4 GB VRAM"
  "8 GB RAM or 6 GB VRAM"
  "12 GB RAM or 8 GB VRAM"
  "16 GB RAM or 12 GB VRAM"
  "18 GB RAM or 16 GB VRAM"
)

if [ $# -ge 1 ]; then
  MODEL="$1"
else
  echo "Select a model to pull (low -> high demand):"
  for i in "${!MODELS[@]}"; do
    idx=$((i + 1))
    echo "  $idx) ${MODELS[$i]}  | min: ${MIN_REQS[$i]}"
  done
  echo "  9) custom model"
  echo

  read -rp "Choice [1-9]: " CHOICE

  if [[ "$CHOICE" =~ ^[1-8]$ ]]; then
    MODEL="${MODELS[$((CHOICE - 1))]}"
  elif [ "$CHOICE" = "9" ]; then
    read -rp "Enter custom model (e.g. mistral:7b): " MODEL
    if [ -z "$MODEL" ]; then
      echo "No model entered. Exiting."
      exit 1
    fi
  else
    echo "Invalid choice. Exiting."
    exit 1
  fi
fi

OLLAMA_PORTS=(11434 11435 11436)
OLLAMA_CONTAINERS=("fase0-ollama1" "fase0-ollama2" "fase0-ollama3")
DNS_TEST_HOST="registry.ollama.ai"

SUCCESS_COUNT=0
FAIL_COUNT=0

echo "Pulling $MODEL model for each Ollama service..."

for i in "${!OLLAMA_CONTAINERS[@]}"; do
  CONTAINER=${OLLAMA_CONTAINERS[$i]}
  PORT=${OLLAMA_PORTS[$i]}

  if ! docker ps --format '{{.Names}}' | grep -qx "$CONTAINER"; then
    echo "Container $CONTAINER is not running."
    echo "Start it with: docker compose up -d $CONTAINER"
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo
    continue
  fi

  if ! docker exec "$CONTAINER" sh -lc "getent hosts $DNS_TEST_HOST >/dev/null"; then
    echo "DNS lookup failed inside $CONTAINER for $DNS_TEST_HOST."
    echo "If you updated docker-compose DNS settings, recreate containers with:"
    echo "  docker compose up -d --force-recreate ollama1 ollama2 ollama3"
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo
    continue
  fi

  echo "Attempting to pull $MODEL on $CONTAINER (port $PORT)..."
  if docker exec "$CONTAINER" ollama pull "$MODEL"; then
    echo "Successfully pulled $MODEL on $CONTAINER."
    SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
  else
    echo "Failed to pull $MODEL on $CONTAINER."
    FAIL_COUNT=$((FAIL_COUNT + 1))
  fi

  echo
done

echo "Script finished. Success: $SUCCESS_COUNT | Failed: $FAIL_COUNT"
