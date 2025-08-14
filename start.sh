#!/bin/bash
<<<<<<< HEAD
set -e
pip install -r requirements.txt
python app.py &
echo $! > app.pid
=======
# start.sh
# Arranca el proyecto Flask TTS-converte-Pro

# ===== CONFIGURACIÓN =====
PROJECT_DIR="$HOME/Documentos/@Laboral/TTS-converte-Pro"
PYTHON_ENV=".venv"                # Carpeta del entorno virtual
MAIN_FILE="app.py"                # Archivo principal del proyecto
FLASK_HOST="0.0.0.0"
FLASK_PORT="5000"

echo "==================================="
echo " Iniciando TTS-converte-Pro"
echo " Carpeta: $PROJECT_DIR"
echo "==================================="

# 1. Ir al directorio del proyecto
cd "$PROJECT_DIR" || { echo "Error: no se pudo entrar en $PROJECT_DIR"; exit 1; }

# 2. Activar entorno virtual
if [ -f "$PYTHON_ENV/bin/activate" ]; then
    echo "Activando entorno virtual..."
    source "$PYTHON_ENV/bin/activate"
else
    echo "No se encontró $PYTHON_ENV. Creando e instalando dependencias..."
    python3 -m venv "$PYTHON_ENV"
    source "$PYTHON_ENV/bin/activate"
    pip install -r requirements.txt
fi

# 3. Cargar variables del archivo .env si existe
if [ -f ".env" ]; then
    echo "Cargando variables de entorno desde .env..."
    export $(grep -v '^#' .env | xargs)
fi

# 4. Lanzar el servidor Flask
echo "Arrancando Flask en http://$FLASK_HOST:$FLASK_PORT ..."
python "$MAIN_FILE" &

# 5. Guardar el PID por si quieres detenerlo luego
echo $! > flask.pid

# 6. Abrir navegador (si está disponible)
if command -v xdg-open >/dev/null; then
    xdg-open "http://localhost:$FLASK_PORT"
elif command -v gnome-open >/dev/null; then
    gnome-open "http://localhost:$FLASK_PORT"
fi

echo "==================================="
echo " Proyecto lanzado."
echo " Para detenerlo: kill \$(cat flask.pid)"
echo "==================================="
>>>>>>> origin/main
