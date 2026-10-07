#!/bin/sh
# ECS detiene la tarea con SIGTERM mientras el ALB todavía le manda tráfico unos
# segundos (la baja del grupo de destino tarda en propagarse). uvicorn cierra al
# instante, así que esas peticiones fallaban con 502. Esperamos DRAIN_SECONDS antes de
# pasarle la señal: el ALB ya dejó de enviar y uvicorn termina lo que tenga en curso.
# El stopTimeout de la task definition (60 s) cubre la espera más el cierre.
set -e
DRAIN_SECONDS="${DRAIN_SECONDS:-15}"

# Trazas X-Ray (control 50): solo cuando la tarea trae el colector ADOT, que define
# OTEL_EXPORTER_OTLP_ENDPOINT. Sin cuerpos de petición ni prompts (dato de salud).
RUN=""
if [ -n "${OTEL_EXPORTER_OTLP_ENDPOINT:-}" ]; then
  export OTEL_TRACES_EXPORTER=otlp OTEL_METRICS_EXPORTER=none OTEL_LOGS_EXPORTER=none
  export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf OTEL_PYTHON_ID_GENERATOR=xray
  export OTEL_PYTHON_FASTAPI_EXCLUDED_URLS="health"
  RUN="opentelemetry-instrument"
fi

$RUN uvicorn app.main:app --host 0.0.0.0 --port 8090 --workers 2 \
  --proxy-headers --forwarded-allow-ips "*" &
PID=$!

trap 'sleep "$DRAIN_SECONDS"; kill -TERM "$PID" 2>/dev/null' TERM INT
wait "$PID" || true
trap - TERM INT
wait "$PID" 2>/dev/null || true
