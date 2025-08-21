import asyncio, os, time
from pathlib import Path
from flask import Flask, Response, abort, render_template, request, send_file
from werkzeug.utils import secure_filename

from tts import (
    DEFAULT_CHUNK_DELAY,
    DEFAULT_CHUNK_LINES,
    read_docx,
    read_txt,
    synthesize_book,
)

APP_VERSION = "1.6.1"
HOME_DIR = str(Path.home())
BASE_OUTPUT_ROOT = os.environ.get("BASE_OUTPUT_ROOT", os.path.join(HOME_DIR, "TTS-output"))

app = Flask(__name__, template_folder="templates", static_folder="static")

VOICE_MAP = {
    "castellano": {"femenina": "es-ES-ElviraNeural", "masculina": "es-ES-AlvaroNeural"},
    "catalan":    {"femenina": "ca-ES-AlbaNeural",   "masculina": "ca-ES-EnricNeural"},
}
SPEED_MAP = {"lenta": "-25%", "normal": "+0%", "rapida": "+25%"}
LOG: list[str] = []

def add_log(msg: str) -> None:
    LOG.append(msg)

def normalize_output_dir(user_input: str, book_name: str) -> Path:
    base_root = Path(BASE_OUTPUT_ROOT).expanduser().resolve()
    candidate = Path(user_input).expanduser() if user_input else base_root
    if not candidate.is_absolute():
        candidate = base_root / candidate
    candidate = candidate.resolve()
    home = Path(HOME_DIR).resolve()
    if home not in candidate.parents and candidate != home:
        candidate = base_root
    project_dir = candidate / secure_filename(book_name)
    project_dir.mkdir(parents=True, exist_ok=True)
    return project_dir

@app.route("/")
def index():
    return render_template("index.html", version=APP_VERSION, home_dir=HOME_DIR, base_output=BASE_OUTPUT_ROOT)

@app.route("/convert", methods=["POST"])
def convert():
    LOG.clear()
    add_log("Inicio de conversión")

    file = request.files.get("archivo")
    if not file or file.filename == "":
        return "Debes subir un archivo .txt o .docx", 400
    filename = secure_filename(file.filename)

    idioma = request.form.get("idioma") or "castellano"
    genero = request.form.get("genero") or "femenina"
    velocidad = request.form.get("velocidad") or "normal"
    pitch_val = request.form.get("pitch", type=int) or 0
    pitch = f"{pitch_val:+d}Hz"
    lineas = request.form.get("lineas", type=int) or DEFAULT_CHUNK_LINES
    pausa = request.form.get("pausa", type=float) or DEFAULT_CHUNK_DELAY
    unir = request.form.get("unir") == "on"
    nombre = request.form.get("nombre") or Path(filename).stem
    book_name = secure_filename(nombre)

    salida_txt = request.form.get("salida", "").strip()
    project_dir = normalize_output_dir(salida_txt, book_name)
    upload_path = project_dir / filename
    file.save(str(upload_path))

    if filename.lower().endswith(".txt"):
        text = read_txt(str(upload_path))
    elif filename.lower().endswith(".docx"):
        text = read_docx(str(upload_path))
    else:
        return "Formato no soportado", 400

    voice = VOICE_MAP.get(idioma, VOICE_MAP["castellano"]).get(genero, VOICE_MAP["castellano"]["femenina"])
    rate = SPEED_MAP.get(velocidad, "+0%")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    files = loop.run_until_complete(
        synthesize_book(
            text, voice, rate, str(project_dir), book_name,
            chunk_lines=lineas, chunk_delay=pausa, pitch=pitch, merge=unir,
            log_callback=add_log,
        )
    )
    loop.close()

    display_files = [(os.path.basename(f), f) for f in files]
    return render_template("exito.html", archivos=display_files, destino=str(project_dir), version=APP_VERSION)

@app.route("/logs")
def logs():
    def stream():
        last = 0
        while True:
            if last < len(LOG):
                data = LOG[last]; last += 1
                yield f"data: {data}\n\n"
            time.sleep(0.5)
    return Response(stream(), mimetype="text/event-stream")

@app.route("/download")
def download():
    path = request.args.get("path")
    if not path or not os.path.exists(path):
        abort(404)
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
