# Granja LLM Escalable con Docker Compose

Este proyecto levanta una arquitectura local orientada a escalabilidad y disponibilidad para servir modelos LLM usando contenedores.

La solución se basa en estos componentes:

- Ollama: runtime de modelos abiertos (inferencia local).
- LiteLLM: gateway compatible con APIs tipo OpenAI para enrutar peticiones a los modelos.
- Nginx: punto de entrada y reverse proxy para exponer un endpoint unificado.
- Redis: soporte de estado compartido/caché para mejorar comportamiento en escenarios con varios servicios.

Objetivo general:

- Tener una base reproducible con Docker Compose para desplegar una "granja" de LLM local.
- Facilitar crecimiento horizontal y mayor disponibilidad del servicio mediante separación de responsabilidades (proxy, gateway, modelo y estado).

## Puesta en marcha

Para hacerlo funcionar, sigue estos pasos en este orden:

1. Crear el archivo `.env`

```bash
cp .env.example .env
```

2. Ejecutar Docker Compose

```bash
docker compose up -d --build
```

3. Descarga de modelos (Automática)

Los modelos necesarios (`qwen3.5:0.8b` para inferencia y `nomic-embed-text` para embeddings/búsqueda semántica) se descargan de forma automática al iniciar los contenedores de Ollama mediante los scripts `scripts/ollama-init.sh` y `scripts/ollama-embed-init.sh`. No es necesario ejecutar ningún comando manual para descargarlos.

4. Probar que funciona con `test_litellm.py`

Puedes ejecutar el conjunto de pruebas usando `uv` (que gestionará e instalará todas las dependencias declaradas automáticamente) o con Python directamente:

```bash
uv run python test_litellm.py
```

Si este test responde correctamente, el stack (Ollama + LiteLLM + Nginx + Redis) está completamente operativo.
