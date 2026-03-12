# Plan de trabajo — Granja de Modelos LLM

## 1. Contexto del proyecto

**Asignatura:** Servidores Web de altas prestaciones  
**Idea:** Diseñar una infraestructura local de inferencia LLM basada en contenedores, con balanceo/proxy inverso, caché semántica y despliegue reproducible.

Este trabajo busca demostrar conceptos clave de la asignatura:
- escalabilidad horizontal,
- reparto de carga,
- reducción de latencia,
- resiliencia ante fallos,
- observabilidad básica de servicios.

**Restricción prioritaria:** el diseño debe funcionar en equipos modestos (sin GPU y/o con poca RAM), priorizando estabilidad y reproducibilidad sobre máximo rendimiento bruto.

---

## 2. Objetivo general

Construir y evaluar una **granja de inferencia LLM** con:
- **Ollama** como motor de modelos,
- **LiteLLM y/o Nginx** como capa de proxy inverso y enrutamiento,
- **Redis** como caché semántica,
- **Docker Compose + Dockerfiles** como sistema de orquestación y despliegue.

---

## 3. Objetivos específicos

1. Desplegar múltiples instancias de Ollama para simular nodos de inferencia.
2. Publicar una entrada única para clientes mediante proxy inverso.
3. Implementar una estrategia de caché semántica para reducir llamadas repetidas al modelo.
4. Medir y comparar métricas antes y después de la caché (latencia, throughput, ratio de aciertos).
5. Documentar arquitectura, decisiones de diseño, pruebas y limitaciones.

---

## 4. Alcance (MVP + ampliaciones)

## 4.0 Perfil objetivo de hardware
- **Escenario base del trabajo:** CPU-only, sin aceleración GPU.
- **RAM ajustada:** priorizar 1 modelo activo principal y un segundo nodo opcional para pruebas de balanceo.
- **Modelos recomendados para MVP:** pequeños (aprox. 1B–4B parámetros) para evitar swapping y tiempos inestables.
- **Meta realista:** demostrar mejora relativa con caché y proxy, no competir con rendimiento de infraestructura GPU.

## 4.1 MVP (obligatorio)
- `docker-compose.yml` con servicios:
  - `ollama-1` (obligatorio) y `ollama-2` (opcional según RAM),
  - `litellm` o `nginx` como frontend,
  - `redis` para caché,
  - `cliente-test` (script de carga/requests).
- Dockerfiles para componentes que lo necesiten.
- Flujo de petición:
  1. cliente → proxy,
  2. consulta de caché semántica,
  3. si miss, inferencia en Ollama,
  4. almacenamiento de resultado en Redis,
  5. respuesta al cliente.
- Métricas mínimas:
  - latencia media/p95,
  - peticiones por segundo,
  - tasa de cache hit/miss,
  - consumo de memoria por servicio (al menos lectura de referencia durante pruebas).

## 4.2 Ampliaciones (opcionales)
- Balanceo por round-robin y/o por salud del nodo.
- Healthchecks y reinicio automático de servicios.
- Dashboard de observabilidad (Prometheus/Grafana).
- Pruebas A/B: con y sin caché semántica.
- Afinación de TTL, top-k y umbral de similitud para la caché.

---

## 5. Arquitectura propuesta

## 5.1 Componentes
- **Cliente de prueba**: genera prompts y carga concurrente.
- **Proxy/API Gateway (LiteLLM/Nginx)**: punto de entrada único, routing y políticas.
- **Caché semántica (Redis)**: guarda embeddings/hash semántico + respuesta.
- **Nodos Ollama**: ejecutan inferencia de modelos ligeros orientados a CPU.
- **Módulo de métricas**: recolecta y exporta tiempos y contadores.

## 5.2 Flujo lógico
1. El cliente envía prompt al endpoint del proxy.
2. El proxy/middleware calcula representación semántica de la consulta (o clave derivada).
3. Se consulta Redis:
   - **hit**: se devuelve respuesta cacheada.
   - **miss**: se enruta la petición a un nodo Ollama.
4. Se devuelve respuesta y se persiste en caché con TTL.
5. Se registran métricas de servicio.

---

## 6. Plan de trabajo por fases

## Fase 0 — Preparación (0,5 semana)
**Tareas**
- Delimitar alcance MVP y criterios de éxito.
- Elegir stack exacto para proxy:
  - Opción A: LiteLLM (más orientado a LLM),
  - Opción B: Nginx + backend Python.
- Definir modelo(s) base de Ollama para las pruebas (priorizar variantes pequeñas aptas para CPU).

**Entregable**
- Documento de arquitectura inicial + backlog priorizado.

## Fase 1 — Infraestructura base (1 semana)
**Tareas**
- Crear `docker-compose.yml` inicial.
- Levantar nodos Ollama + Redis + proxy.
- Añadir redes, volúmenes y healthchecks básicos.
- Configurar límites de recursos y concurrencia segura para evitar saturación de RAM.

**Entregable**
- Entorno reproducible con `docker compose up`.

## Fase 2 — Proxy y routing (1 semana)
**Tareas**
- Exponer endpoint único de inferencia.
- Implementar balanceo entre nodos de Ollama.
- Manejar errores/reintentos ante nodo caído.

**Entregable**
- Peticiones distribuidas correctamente y validadas.

## Fase 3 — Caché semántica (1 semana)
**Tareas**
- Diseñar clave/cálculo semántico (texto normalizado o embedding).
- Integrar Redis para `lookup` y `store`.
- Definir política de expiración (TTL) y estrategia de invalidación.

**Entregable**
- Sistema con cache hit/miss funcional.

## Fase 4 — Carga y evaluación (1 semana)
**Tareas**
- Preparar batería de prompts de prueba.
- Ejecutar pruebas de carga con concurrencia creciente pero acotada (p. ej., baja/media), adecuada al hardware disponible.
- Comparar escenarios:
  - sin caché,
  - con caché.

**Entregable**
- Tabla de métricas y gráficas comparativas.

## Fase 5 — Documentación y defensa (0,5 semana)
**Tareas**
- Redactar memoria final (diseño, implementación, resultados, límites).
- Preparar demo guiada y diapositivas.
- Ensayar respuestas para preguntas técnicas.

**Entregable**
- Memoria + presentación + demo reproducible.

---

## 7. Reparto de trabajo (equipo)

## Rol 1 — Infraestructura
- Dockerfiles, Compose, networking, persistencia, healthchecks.

## Rol 2 — Backend/Proxy
- Configuración de LiteLLM/Nginx, balanceo, fallback, API de entrada.

## Rol 3 — Caché y evaluación
- Integración Redis, política de caché, scripts de benchmark y análisis.

> Si sois 2 personas: fusionar Rol 1+2 y mantener Rol 3 separado.

---

## 8. Cronograma sugerido (4–5 semanas)

- **Semana 1:** Fase 0 + Fase 1
- **Semana 2:** Fase 2
- **Semana 3:** Fase 3
- **Semana 4:** Fase 4
- **Semana 5 (si aplica):** Fase 5 y pulido final

> Si el hardware es muy limitado, fusionar Fase 2 y Fase 3 en una sola iteración simple para llegar antes a métricas comparables.

---

## 9. Riesgos y mitigaciones

1. **Consumo alto de recursos (CPU/RAM/GPU).**  
   Mitigación: usar modelos pequeños, limitar concurrencia y reservar recursos por contenedor.

2. **Inestabilidad de nodos de inferencia.**  
   Mitigación: healthchecks, restart policy y timeout/retry en proxy.

3. **Caché semántica con falsos positivos.**  
   Mitigación: umbral de similitud conservador + evaluación manual de calidad.

4. **Complejidad excesiva para el tiempo disponible.**  
   Mitigación: priorizar MVP y dejar ampliaciones como extras.

---

## 10. Criterios de éxito

- El stack se levanta completo con un único comando.
- Existe endpoint único de inferencia operando al menos con 1 nodo (y 2 nodos si la RAM lo permite).
- La caché semántica reduce latencia media bajo carga repetitiva.
- Hay resultados medidos y comparables en al menos 2 escenarios.
- La documentación permite reproducir la demo por terceros.

---

## 11. Estructura de entregables

- **Código:** Compose + Dockerfiles + scripts de test.
- **Informe técnico:** arquitectura, decisiones, resultados.
- **Anexos:** configuración, comandos y logs clave.
- **Presentación:** problema, solución, demo, resultados.

---

## 12. Próximos pasos inmediatos

1. Elegir stack de proxy principal (**LiteLLM** recomendado para MVP).
2. Definir modelo Ollama de pruebas ligero para CPU (y un alternativo solo si cabe en RAM).
3. Crear el primer `docker-compose.yml` funcional mínimo con límites de recursos.
4. Implementar un script de prueba simple para línea base de latencia y memoria.
5. Añadir caché semántica y repetir medición en el mismo hardware.
