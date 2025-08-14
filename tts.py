import asyncio
import os
import re
from typing import List, Tuple

import edge_tts
from docx import Document
from pydub import AudioSegment
import textract


DEFAULT_CHUNK_LINES = 200
# Pausa por defecto entre peticiones para no saturar los servidores
DEFAULT_CHUNK_DELAY = float(os.getenv("REQUEST_PAUSE", "1"))


def read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


def read_doc(path: str) -> str:
    text = textract.process(path)
    return text.decode("utf-8")


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
    pitch: str = "0%",
) -> None:
    lines = text.splitlines()
    chunks = [
        "\n".join(lines[i : i + chunk_lines])
        for i in range(0, len(lines), chunk_lines)
    ]
    temp_files = []
    for idx, chunk in enumerate(chunks):
        communicate = edge_tts.Communicate(chunk, voice=voice, rate=rate, pitch=pitch)
        tmp_file = f"{output_path}_tmp_{idx}.mp3"
        await communicate.save(tmp_file)
        temp_files.append(tmp_file)
        await asyncio.sleep(chunk_delay)
    audio = AudioSegment.empty()
    for f in temp_files:
        audio += AudioSegment.from_file(f)
        os.remove(f)
    audio.export(output_path, format="mp3")


async def synthesize_book(
    text: str,
    voice: str,
    rate: str,
    out_dir: str,
    book_name: str,
    chunk_lines: int = DEFAULT_CHUNK_LINES,
    chunk_delay: float = DEFAULT_CHUNK_DELAY,
    pitch: str = "0%",
) -> List[str]:
    os.makedirs(out_dir, exist_ok=True)
    chapters = split_into_chapters(text)
    files = []
    for i, (_, chapter_text) in enumerate(chapters, start=1):
        filename = os.path.join(out_dir, f"{book_name}_capitulo_{i}.mp3")
        await synthesize(
            chapter_text,
            voice,
            rate,
            filename,
            chunk_lines=chunk_lines,
            chunk_delay=chunk_delay,
            pitch=pitch,
        )
        files.append(filename)
    return files
