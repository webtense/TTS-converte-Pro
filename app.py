import asyncio
import os
from pathlib import Path
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from tts import (
    DEFAULT_CHUNK_DELAY,
    DEFAULT_CHUNK_LINES,
    read_docx,
    read_txt,
    synthesize_book,
)

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

SPEED_MAP = {"lenta": "-25%", "normal": "0%", "rapida": "+25%"}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    file = request.files["archivo"]
    idioma = request.form.get("idioma")
    genero = request.form.get("genero")
    velocidad = request.form.get("velocidad")
    pitch_val = request.form.get("pitch", type=int) or 0
    pitch = f"{pitch_val:+d}%"
    carpeta = request.form.get("carpeta") or "salida"
    lineas = request.form.get("lineas", type=int) or DEFAULT_CHUNK_LINES
    pausa = request.form.get("pausa", type=float) or DEFAULT_CHUNK_DELAY

    book_name = Path(file.filename).stem
    filename = secure_filename(file.filename)
    upload_path = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(upload_path)

    if filename.lower().endswith(".txt"):
        text = read_txt(upload_path)
    elif filename.lower().endswith(".docx"):
        text = read_docx(upload_path)
    else:
        return "Formato no soportado", 400

    voice = VOICE_MAP.get(idioma, VOICE_MAP["castellano"])[genero]
    rate = SPEED_MAP.get(velocidad, "0%")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    files = loop.run_until_complete(
        synthesize_book(
            text,
            voice,
            rate,
            carpeta,
            book_name,
            chunk_lines=lineas,
            chunk_delay=pausa,
            pitch=pitch,
        )
    )
    loop.close()

    return render_template("exito.html", archivos=files, carpeta=carpeta)


if __name__ == "__main__":
    app.run(debug=True)
