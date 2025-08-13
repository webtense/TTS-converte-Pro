# TTS-converte-Pro

Aplicación web en Flask que convierte libros en formatos **TXT**, **DOCX** o **DOC** a archivos de audio **MP3**, generando un archivo por capítulo mediante voces de **Microsoft Edge TTS**.

## Requisitos
- Python 3.10+
- ffmpeg instalado
- Dependencias de `requirements.txt`

## Uso
1. Instala dependencias: `pip install -r requirements.txt`.
2. Ejecuta la aplicación: `python app.py`.
3. Abre `http://localhost:5000` y sube un archivo.
4. Elige idioma, género, velocidad, número de líneas por bloque, pausa entre bloques y carpeta de salida.
5. Se generará un MP3 por capítulo en la carpeta indicada.

El sistema detecta capítulos mediante encabezados como "Capítulo X" o "Chapter X". Cada capítulo se procesa en bloques de líneas configurables con una pausa entre peticiones para evitar límites del servicio. Durante la conversión se muestra una barra de progreso estimada basada en el tamaño del archivo.
