#!/bin/bash
# start.sh: arranca Flask y soluciona audioop en Python 3.13+
set -euo pipefail
PID_FILE="flask.pid"

# Parar cualquier proceso previo
if [ -x ./stop.sh ]; then ./stop.sh || true; fi

# venv
if [ ! -f ".venv/bin/activate" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

# ffmpeg
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "[INFO] instalando ffmpeg..."
  sudo apt-get update -y && sudo apt-get install -y ffmpeg
fi

# deps
pip install -U pip setuptools wheel
[ -f requirements.txt ] && pip install -r requirements.txt

# Python 3.13+: instalar audioop-lts si no está
python - <<'PY'
try:
    import sys
    if sys.version_info >= (3,13):
        try:
            import audioop  # noqa
            print("[OK] audioop presente")
        except Exception:
            import subprocess
            print("[INFO] instalando audioop-lts…")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "audioop-lts"])
except Exception as e:
    print("Aviso audioop:", e)
PY

# pydub actualizado
pip install -U pydub

# .env
[ -f .env ] && export $(grep -v '^#' .env | xargs || true)

# lanzar
python app.py & echo $! > "$PID_FILE"
echo "[OK] Servidor en http://localhost:5000  (PID $(cat "$PID_FILE"))"
