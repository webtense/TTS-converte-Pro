import asyncio
import re
import time
from pathlib import Path
from typing import Callable, List, Optional

import edge_tts
from docx import Document
from pydub import AudioSegment  # requiere ffmpeg

DEFAULT_CHUNK_DELAY: float = 0.5   # segundos entre bloques
DEFAULT_CHUNK_LINES: int = 0       # 0 = capítulo entero

def read_txt(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="ignore").replace("\r\n","\n").replace("\r","\n")

def read_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs).replace("\r\n","\n").replace("\r","\n")

# --- particionado por capítulos y líneas ---
_CHAPTER_RX = re.compile(r"(?im)^\s*(cap[ií]tulo\s+\d+|chapter\s+\d+)\b.*$", re.MULTILINE)

def split_chapters(text: str) -> List[str]:
    cuts = [m.start() for m in _CHAPTER_RX.finditer(text)]
    if not cuts:
        return [text.strip()]
    cuts.append(len(text))
    return [text[cuts[i]:cuts[i+1]].strip() for i in range(len(cuts)-1)]

def chunk_by_lines(ch_text: str, n_lines: int) -> List[str]:
    if n_lines <= 0:
        return [ch_text.strip()]
    lines = ch_text.splitlines()
    chunks, buf = [], []
    for ln in lines:
        buf.append(ln)
        if len(buf) >= n_lines:
            chunks.append("\n".join(buf).strip()); buf = []
    if buf:
        chunks.append("\n".join(buf).strip())
    return [c for c in chunks if c]

# --- guardado robusto con reintentos ---
async def tts_to_file(text: str, voice: str, rate: str, pitch: str, out_path: Path,
                      log: Optional[Callable[[str], None]] = None,
                      max_retries: int = 5, base_sleep: float = 1.0) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    attempt = 0
    last_exc: Optional[Exception] = None
    while attempt < max_retries:
        attempt += 1
        try:
            if log: log(f"   · TTS intento {attempt}/{max_retries} → {out_path.name}")
            com = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
            await com.save(str(out_path))
            # Verificar resultado
            if out_path.exists() and out_path.stat().st_size > 0:
                if log: log(f"   ✓ guardado {out_path.name} ({out_path.stat().st_size} bytes)")
                return
            else:
                raise FileNotFoundError(f"Generación vacía o inexistente: {out_path}")
        except Exception as e:
            last_exc = e
            if log: log(f"   ! fallo TTS: {e.__class__.__name__}: {e}")
            # backoff exponencial con jitter ligero
            sleep_time = base_sleep * (2 ** (attempt - 1))
            time.sleep(min(sleep_time, 8.0))
    # si llegamos aquí, no se pudo generar
    raise RuntimeError(f"No se pudo generar {out_path} tras {max_retries} intentos") from last_exc

# --- síntesis principal ---
async def synthesize_book(
    full_text: str,
    voice: str,
    rate: str,
    output_dir: str,
    book_name: str,
    chunk_lines: int = DEFAULT_CHUNK_LINES,
    chunk_delay: float = DEFAULT_CHUNK_DELAY,
    pitch: str = "+0Hz",
    merge: bool = False,
    log_callback: Callable[[str], None] | None = None,
) -> List[str]:
    def log(msg: str):
        if log_callback:
            log_callback(msg)

    out_dir = Path(output_dir); out_dir.mkdir(parents=True, exist_ok=True)
    chapters = split_chapters(full_text)
    total = len(chapters)
    log(f"Capítulos detectados: {total}")

    generated_paths: List[Path] = []
    merged_audio: AudioSegment | None = None

    for i, ch in enumerate(chapters, start=1):
        log(f"[{i}/{total}] Preparando capítulo…")
        pieces = chunk_by_lines(ch, chunk_lines)

        if merge:
            for j, piece in enumerate(pieces, start=1):
                tmp_file = out_dir / f"._tmp_{book_name}_c{i:02d}_b{j:02d}.mp3"
                log(f"  - bloque {j}/{len(pieces)}")
                await tts_to_file(piece, voice, rate, pitch, tmp_file, log=log)
                seg = AudioSegment.from_file(tmp_file)
                merged_audio = seg if merged_audio is None else (merged_audio + seg)
                tmp_file.unlink(missing_ok=True)
                if chunk_delay > 0:
                    time.sleep(chunk_delay)
        else:
            chap_audio: AudioSegment | None = None
            for j, piece in enumerate(pieces, start=1):
                tmp_file = out_dir / f"._tmp_{book_name}_c{i:02d}_b{j:02d}.mp3"
                log(f"  - bloque {j}/{len(pieces)}")
                await tts_to_file(piece, voice, rate, pitch, tmp_file, log=log)
                seg = AudioSegment.from_file(tmp_file)
                chap_audio = seg if chap_audio is None else (chap_audio + seg)
                tmp_file.unlink(missing_ok=True)
                if chunk_delay > 0:
                    time.sleep(chunk_delay)
            out_file = out_dir / f"{book_name}_cap{i:02d}.mp3"
            chap_audio.export(out_file, format="mp3")
            generated_paths.append(out_file)
            log(f"  ✓ capítulo {i} exportado: {out_file.name}")

    if merge:
        out_file = out_dir / f"{book_name}.mp3"
        if merged_audio is None:
            merged_audio = AudioSegment.silent(duration=500)
        merged_audio.export(out_file, format="mp3")
        generated_paths = [out_file]
        log(f"✓ audio combinado exportado: {out_file.name}")

    return [str(p) for p in generated_paths]
