import asyncio
import os
from pathlib import Path
import time
from flask import Flask, Response, render_template, request
from werkzeug.utils import secure_filename

from tts import (
    DEFAULT_CHUNK_DELAY,
    DEFAULT_CHUNK_LINES,
    read_docx,
    read_txt,
    synthesize_book,
)

APP_VERSION = "1.3.0"
__version__ = APP_VERSION
app = Flask(__name__)

VOICE_MAP = {
    "castellano": {
        "femenina": "es-ES-ElviraNeural",
        "masculina": "es-ES-AlvaroNeural",
    },
    "catalan": {
        "femenina": "ca-ES-AlbaNeural",
        "masculina": "ca-ES-EnricNeural",
    },
}

SPEED_MAP = {"lenta": "-25%", "normal": "+0%", "rapida": "+25%"}

LOG: list[str] = []


def add_log(msg: str) -> None:
    LOG.append(msg)


@app.route("/")
def index():
    return render_template("index.html", version=APP_VERSION)


@app.route("/convert", methods=["POST"])
def convert():
    LOG.clear()
    add_log("Inicio de conversión")
    file = request.files["archivo"]
    idioma = request.form.get("idioma")
    genero = request.form.get("genero")
    velocidad = request.form.get("velocidad")
    pitch_val = request.form.get("pitch", type=int) or 0
    pitch = f"{pitch_val:+d}Hz"
    lineas = request.form.get("lineas", type=int) or DEFAULT_CHUNK_LINES
    pausa = request.form.get("pausa", type=float) or DEFAULT_CHUNK_DELAY
    nombre = request.form.get("nombre") or Path(file.filename).stem
    book_name = secure_filename(nombre)
    filename = secure_filename(file.filename)
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    upload_path = os.path.join(upload_dir, filename)
    file.save(upload_path)
    output_dir = upload_dir

    if filename.lower().endswith(".txt"):
        text = read_txt(upload_path)
    elif filename.lower().endswith(".docx"):
        text = read_docx(upload_path)
    else:
        return "Formato no soportado", 400

    voice = VOICE_MAP.get(idioma, VOICE_MAP["castellano"])[genero]
    rate = SPEED_MAP.get(velocidad, "+0%")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    files = loop.run_until_complete(
        synthesize_book(
            text,
            voice,
            rate,
            output_dir,
            book_name,
            chunk_lines=lineas,
            chunk_delay=pausa,
            pitch=pitch,
            log_callback=add_log,
        )
    )
    loop.close()

    display_files = [os.path.basename(f) for f in files]
    return render_template("exito.html", archivos=display_files, version=APP_VERSION)


@app.route("/logs")
def logs():
    def stream():
        last = 0
        while True:
            if last < len(LOG):
                data = LOG[last]
                last += 1
                yield f"data: {data}\n\n"
            time.sleep(0.5)
    return Response(stream(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True)
