#!/bin/bash
# stop.sh
# Detiene el servidor Flask iniciado con start.sh

PROJECT_DIR="$HOME/Documentos/@Laboral/TTS-converte-Pro"
PID_FILE="$PROJECT_DIR/flask.pid"

echo "==================================="
echo " Deteniendo TTS-converte-Pro"
echo "==================================="

# 1. Comprobar si existe el archivo con el PID
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null; then
        echo "Matando proceso Flask con PID: $PID"
        kill $PID
        rm -f "$PID_FILE"
        echo "Servidor detenido correctamente."
    else
        echo "No se encontró proceso Flask en ejecución."
    fi
else
    echo "No existe $PID_FILE, no sé qué proceso detener."
fi

echo "==================================="
