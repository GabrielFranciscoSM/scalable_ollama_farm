# Fase 0 — Preparación (MVP)

Esta carpeta contiene una base mínima para arrancar la decisión de arquitectura del proyecto en modo local:

- `Ollama` como motor de modelo local.
- `LiteLLM` como capa orientada a modelos LLM.
- `Nginx` como reverse proxy de entrada única.

## ¿Por qué ambos y no uno solo?

- `LiteLLM` resuelve la parte de **LLM gateway** (normalización de API de modelos, routing por modelo, políticas de uso).
- `Nginx` resuelve la parte de **frontal web/red** (proxy de red, punto único de entrada, capa de perímetro).

Decisión para el MVP: usar **Nginx delante** y **LiteLLM detrás**.

## Estructura

- `docker-compose.yml`: levanta `ollama`, `litellm` y `nginx`.
- `ollama/Dockerfile`: imagen personalizada de Ollama con modelo por defecto.
- `ollama/start-ollama.sh`: arranca servidor y hace `pull` automático del modelo.
- `nginx/default.conf`: proxy HTTP hacia LiteLLM.
- `litellm/config.yaml`: mapeo inicial de modelo local (`tinyllama`).
- `.env.example`: variables necesarias.

## Arranque rápido

1. Copia variables de entorno:

```bash
cp .env.example .env
```

2. Levanta servicios (se construye la imagen de Ollama y se precarga `tinyllama` automáticamente en el primer arranque):

```bash
docker compose up -d --build
```

## Prueba mínima

```bash
curl http://localhost:8088/v1/models \
  -H "Authorization: Bearer sk-fase0-local"
```

Si responde la lista de modelos, la fase 0 queda validada como base para continuar con Fase 1.

Prueba de chat mínima:

```bash
curl http://localhost:8088/v1/chat/completions \
  -H "Authorization: Bearer sk-fase0-local" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "local-chat",
    "messages": [{"role": "user", "content": "Di hola en una frase."}]
  }'
```
