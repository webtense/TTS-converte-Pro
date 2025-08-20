import asyncio
import os
import re
from typing import List, Tuple

__version__ = "1.5.0"

import edge_tts
from docx import Document
from pydub import AudioSegment


DEFAULT_CHUNK_LINES = 200
# Pausa por defecto entre peticiones para no saturar los servidores
DEFAULT_CHUNK_DELAY = float(os.getenv("REQUEST_PAUSE", "1"))


def read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


def split_into_chapters(text: str) -> List[Tuple[str, str]]:
    pattern = re.compile(r"^(?:Cap[ií]tulo|Chapter)\s+\d+", re.IGNORECASE | re.MULTILINE)
    matches = list(pattern.finditer(text))
    if not matches:
        return [("capitulo_1", text)]
    chapters = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        chapter_text = text[start:end].strip()
        chapters.append((f"capitulo_{i + 1}", chapter_text))
    return chapters


async def synthesize(
    text: str,
    voice: str,
    rate: str,
    output_path: str,
    chunk_lines: int = DEFAULT_CHUNK_LINES,
    chunk_delay: float = DEFAULT_CHUNK_DELAY,
    pitch: str = "+0Hz",
    log_callback=None,
) -> None:
    if chunk_lines <= 0:
        chunks = [text]
    else:
        lines = text.splitlines()
        chunks = [
            "\n".join(lines[i : i + chunk_lines])
            for i in range(0, len(lines), chunk_lines)
        ]
    temp_files = []
    for idx, chunk in enumerate(chunks):
        if not chunk.strip():
            continue
        communicate = edge_tts.Communicate(chunk, voice=voice, rate=rate, pitch=pitch)
        tmp_file = f"{output_path}_tmp_{idx}.mp3"
        await communicate.save(tmp_file)
        temp_files.append(tmp_file)
        if chunk_delay > 0:
            if log_callback:
                remaining = int(chunk_delay)
                while remaining > 0:
                    log_callback(f"Reanudando en {remaining}s")
                    await asyncio.sleep(1)
                    remaining -= 1
                remainder = chunk_delay - int(chunk_delay)
                if remainder > 0:
                    await asyncio.sleep(remainder)
                log_callback("BEEP")
            else:
                await asyncio.sleep(chunk_delay)
    audio = AudioSegment.empty()
    for f in temp_files:
        if os.path.exists(f):
            audio += AudioSegment.from_file(f)
            os.remove(f)
        elif log_callback:
            log_callback(f"Segmento perdido: {f}")
    audio.export(output_path, format="mp3")


async def synthesize_book(
    text: str,
    voice: str,
    rate: str,
    out_dir: str,
    book_name: str,
    chunk_lines: int = DEFAULT_CHUNK_LINES,
    chunk_delay: float = DEFAULT_CHUNK_DELAY,
    pitch: str = "+0Hz",
    log_callback=None,
) -> List[str]:
    os.makedirs(out_dir, exist_ok=True)
    chapters = split_into_chapters(text)
    files = []
    if log_callback:
        log_callback(f"Capítulos detectados: {len(chapters)}")
    total_chunks = 0
    if chunk_lines > 0:
        for _, chapter_text in chapters:
            lines = chapter_text.splitlines()
            total_chunks += max(1, (len(lines) + chunk_lines - 1) // chunk_lines)
    else:
        total_chunks = len(chapters)
    if log_callback:
        est_total = total_chunks * chunk_delay
        log_callback(f"Tiempo estimado: {int(est_total)}s")
    for i, (_, chapter_text) in enumerate(chapters, start=1):
        if log_callback:
            log_callback(f"Procesando capítulo {i}")
        filename = os.path.join(out_dir, f"{book_name}_capitulo_{i}.mp3")
        await synthesize(
            chapter_text,
            voice,
            rate,
            filename,
            chunk_lines=chunk_lines,
            chunk_delay=chunk_delay,
            pitch=pitch,
            log_callback=log_callback,
        )
        files.append(filename)
        if log_callback:
            log_callback(f"Capítulo {i} listo")
    if log_callback:
        log_callback("Conversión finalizada")
    return files
