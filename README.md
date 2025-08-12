# TTS-converte-Pro

Aplicación web en Flask que convierte libros en formatos **TXT**, **DOCX** o **DOC** a archivos de audio **MP3**, generando un archivo por capítulo mediante voces de **Microsoft Edge TTS**.

## Requisitos
- Python 3.10+
- ffmpeg instalado
- Dependencias de `requirements.txt`

## Uso
1. (Opcional) Crea un entorno virtual: `python -m venv .venv && source .venv/bin/activate`.
2. Instala dependencias: `pip install -r requirements.txt`.
3. Ejecuta la aplicación: `python app.py`.
4. Abre `http://localhost:5000` y sube un archivo.
5. Elige idioma, género, velocidad y carpeta de salida.
6. Se generará un MP3 por capítulo en la carpeta indicada.

El sistema detecta capítulos mediante encabezados como "Capítulo X" o "Chapter X". Cada capítulo se procesa en bloques de 200 líneas con una pausa de un segundo entre peticiones para evitar límites del servicio. Durante la conversión se muestra una barra de progreso estimada basada en el tamaño del archivo.
