# 🎙️ TTS-converte-Pro

Aplicación web en **Flask** que convierte libros en **TXT** o **DOCX** en archivos de audio **MP3** usando voces de **Microsoft Edge TTS**.

La interfaz minimalista (oscuro con acentos rojos) está optimizada para usabilidad: muestra versión actual, parámetros de voz, panel de progreso en vivo y enlaces de descarga al terminar.

---

## ✨ Características principales

* 📂 **Entrada**: archivos `.txt` o `.docx`
* 🔊 **Salida**: archivos `.mp3` (un MP3 por capítulo o uno único combinado)
* 🌐 **Voces**: soporte para **Microsoft Edge TTS** (idiomas Castellano y Catalán, voz masculina/femenina)
* ⚡ **Parámetros configurables**:

  * Idioma y género
  * Velocidad de lectura (lenta / normal / rápida)
  * Pitch (Hz, positivo o negativo)
  * Número de líneas por bloque (0 = capítulo entero)
  * Pausa entre bloques (segundos)
* 🗂️ **Gestión de proyectos**:

  * Carpeta de salida configurable
  * Nombre base del proyecto
  * Autocreación de subcarpeta por proyecto
* 📊 **Panel de log en vivo**:

  * Mensajes de conversión por bloque
  * Cuenta atrás en pausas
  * Estimación de progreso
  * Beep al reanudar
* 🖥️ **Interfaz web limpia**: blanco/negro + toques rojos, responsive
* 🛠️ **Scripts incluidos**:

  * `start.sh` → instala dependencias, arranca servidor
  * `stop.sh` → detiene cualquier instancia en puerto 5000
  * (opcional) `restart.sh` → parar + arrancar

---

## 📦 Requisitos

* Python **3.10+** (compatible con 3.13 usando `audioop-lts`)
* `ffmpeg` instalado (necesario para `pydub`)
* Conexión a internet (para Microsoft Edge TTS)

---

## 🚀 Instalación

### Linux / macOS

```bash
git clone git@github.com:webtense/TTS-converte-Pro.git
cd TTS-converte-Pro

# Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Windows

```powershell
git clone https://github.com/webtense/TTS-converte-Pro.git
cd TTS-converte-Pro

# Crear y activar entorno virtual
py -m venv .venv
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## ▶️ Uso

### Con scripts (recomendado)

```bash
./start.sh
```

Esto:

* Verifica `ffmpeg`
* Instala dependencias
* Lanza Flask en `http://localhost:5000`

Para detener:

```bash
./stop.sh
```

Para reiniciar:

```bash
./stop.sh && ./start.sh
```

### Manual

```bash
source .venv/bin/activate
python app.py
```

---

## 🌐 Interfaz Web

1. Abre `http://localhost:5000`
2. Sube un archivo `.txt` o `.docx`
3. Configura:

   * Idioma / género
   * Velocidad y pitch
   * Líneas por bloque y pausa entre bloques
   * Carpeta de salida y nombre de proyecto
   * Opción de unir capítulos en un solo MP3
4. Haz clic en **Convertir**
5. Observa progreso en el panel derecho
6. Descarga los MP3 desde la página de éxito

---

## 📂 Estructura del proyecto

```
TTS-converte-Pro/
├── app.py            # Flask main
├── tts.py            # Lógica de síntesis y parsing libros
├── start.sh          # Arranca servidor
├── stop.sh           # Detiene servidor
├── requirements.txt  # Dependencias Python
├── templates/
│   ├── index.html    # Interfaz principal
│   └── exito.html    # Página de descarga
├── static/           # CSS, JS, imágenes
└── README.md         # Este archivo
```

---

## 🔮 Roadmap / TODO

* [ ] Añadir más idiomas y voces
* [ ] Exportar a otros formatos (WAV, OGG)
* [ ] Autodetectar idioma en TXT/DOCX
* [ ] Subida de múltiples ficheros a la vez
* [ ] Contenedor Docker oficial
* [ ] Panel de administración con histórico de proyectos

---

## 📸 Capturas


---

## 🤝 Contribuir

1. Haz un fork del repo
2. Crea tu rama (`git checkout -b feature/nueva-funcion`)
3. Haz commit de tus cambios (`git commit -m "feat: lo que hiciste"`)
4. Push (`git push origin feature/nueva-funcion`)
5. Abre un Pull Request

---

## 📜 Licencia

Este proyecto está bajo licencia MIT.
Puedes usarlo, modificarlo y redistribuirlo libremente, siempre manteniendo los créditos.

---

## 👤 Autor

**Andrés Sánchez (@webtense)**
Director de IT y SSTT
💻 GitHub: [webtense](https://github.com/webtense)
