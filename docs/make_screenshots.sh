#!/bin/bash
set -euo pipefail

convert -size 800x500 xc:white -fill black -gravity center \
  -pointsize 30 -draw "text 0,0 'Pantalla principal (Index)'" screenshot-index.png

convert -size 800x500 xc:white -fill black -gravity center \
  -pointsize 30 -draw "text 0,0 'Panel de Log en vivo'" screenshot-log.png

convert -size 800x500 xc:white -fill black -gravity center \
  -pointsize 30 -draw "text 0,0 'Página de éxito (Descargas)'" screenshot-exito.png

echo "[OK] Placeholders generados en ./docs"
