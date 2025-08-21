#!/bin/bash
# stop.sh - detener servidor Flask del proyecto

set -euo pipefail
PID_FILE="flask.pid"
PORT=5000

echo "======================="
echo " Deteniendo Flask"
echo "======================="

# 1. Detener usando el PID guardado
if [ -f "$PID_FILE" ]; then
  PID=$(cat "$PID_FILE")
  if ps -p "$PID" > /dev/null 2>&1; then
    echo "Matando PID $PID..."
    kill "$PID" || true
    sleep 1
    ps -p "$PID" > /dev/null 2>&1 && kill -9 "$PID" || true
  else
    echo "PID $PID ya no existe"
  fi
  rm -f "$PID_FILE"
fi

# 2. Detener cualquier proceso en el puerto 5000
PID_PORT=$(lsof -ti tcp:$PORT || true)
if [ -n "$PID_PORT" ]; then
  echo "Matando procesos en puerto $PORT: $PID_PORT"
  kill -9 $PID_PORT || true
fi

# 3. Fallback: matar procesos Python con app.py
pkill -f app.py || true

echo "[OK] Flask detenido"
