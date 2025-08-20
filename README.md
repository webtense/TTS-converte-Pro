# TTS-converte-Pro

Aplicación web en Flask que convierte libros en formatos **TXT** o **DOCX** a archivos de audio **MP3** usando voces de **Microsoft Edge TTS**. La interfaz minimalista (blanco/negro con toques rojos) muestra la versión actual y permite ajustar idioma, género, velocidad, *pitch*, número de líneas por bloque, pausa entre bloques, carpeta de salida y nombre base del archivo. Puede generarse un MP3 por capítulo o un único archivo con todos los capítulos unidos. Los MP3 se guardan en la carpeta seleccionada y, durante la conversión, un panel de log muestra el progreso, las cuentas atrás entre bloques y emite un beep al reanudar. Se estima el tiempo total restante y se presenta una cuenta regresiva. La página de éxito ofrece enlaces para descargar los archivos resultantes. Versión actual: **1.6.0**.

## Requisitos
- Python 3.10+
- `ffmpeg` instalado
- Dependencias de `requirements.txt`

## Descarga
### Linux / macOS
1. `git clone https://github.com/tuusuario/TTS-converte-Pro.git`
2. `cd TTS-converte-Pro`

### Windows
1. Instala [Git](https://git-scm.com/download/win) y abre **Git Bash**.
2. Ejecuta:
   ```bash
   git clone https://github.com/tuusuario/TTS-converte-Pro.git
   cd TTS-converte-Pro
   ```

## Instalación
### Linux / macOS
1. *(Opcional)* `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`

### Windows
1. *(Opcional)* `py -m venv .venv && .venv\Scripts\activate`
2. `pip install -r requirements.txt`

## Uso
### Con scripts
1. `./start.sh` instala dependencias y lanza la web.
2. Abre `http://localhost:5000` y sube un archivo.
3. `./stop.sh` detiene la aplicación.

### Manual
1. `python app.py`
2. Abre `http://localhost:5000`.

En la web puedes:
- Elegir idioma, género y velocidad.
- Ajustar *pitch*, líneas por bloque y pausa entre bloques (0 procesa el capítulo completo de una sola vez).
- Definir la carpeta de salida, el nombre base del archivo MP3 y si deseas unir todos los capítulos en un único MP3.
- Consultar la versión actual en la parte inferior de la página.

Se generará un MP3 por capítulo o uno único con todos los capítulos (según se seleccione) en la carpeta elegida, nombrando los archivos con el nombre del proyecto. Los capítulos se detectan mediante encabezados como "Capítulo X" o "Chapter X". Cada capítulo se procesa en bloques con una pausa (`REQUEST_PAUSE`) entre peticiones para evitar saturar el servicio. Durante la conversión se muestra una barra de progreso, un contador del tiempo estimado restante y, en el panel derecho, un log con el estado de cada capítulo, la cuenta atrás antes de reanudar y un beep al continuar. Al finalizar, la página muestra enlaces para descargar los MP3 generados.
