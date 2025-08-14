#!/bin/bash
# stop.sh — Detiene el servidor Flask iniciado con start.sh

set -euo pipefail

PROJECT_DIR="$HOME/Documentos/@Laboral/TTS-converte-Pro"
PID_FILE="$PROJECT_DIR/flask.pid"

echo "==================================="
echo " Deteniendo TTS-converte-Pro"
echo "==================================="

if [ -f "$PID_FILE" ]; then
  PID="$(cat "$PID_FILE")"
  if ps -p "$PID" > /dev/null 2>&1; then
    echo "Matando proceso Flask con PID: $PID"
    kill "$PID"
    # espera breve y fuerza si sigue vivo
    sleep 1
    if ps -p "$PID" > /dev/null 2>&1; then
      echo "Forzando kill -9 $PID"
      kill -9 "$PID" || true
    fi
    rm -f "$PID_FILE"
    echo "Servidor detenido."
  else
    echo "PID $PID no existe. Limpio $PID_FILE."
    rm -f "$PID_FILE"
  fi
else
  echo "No existe $PID_FILE; nada que detener."
fi

echo "==================================="
