#!/usr/bin/env bash
set -euo pipefail

BR=main
REMOTE=origin

echo "==> Publicando en $REMOTE/$BR"
git fetch "$REMOTE"

# Guardar estado local
echo "==> Preparando commit local (si hay cambios)"
git add -A
if ! git diff --cached --quiet; then
  git commit -m "chore: publish snapshot $(date +%F\ %T)"
fi

# Intento 1: rebase + push normal
echo "==> Rebase sobre $REMOTE/$BR"
git pull --rebase "$REMOTE" "$BR" || {
  echo "==> Rebase con conflictos. Resuélvelos y ejecuta:"
  echo "    git add . && git rebase --continue"
  echo "    ./publish.sh"
  exit 1
}

echo "==> Push normal"
if git push "$REMOTE" "$BR"; then
  echo "✅ Publicado con rebase."
  exit 0
fi

# Si falla el push normal, ofrecer push forzado con copia de seguridad
read -rp "El push fue rechazado. ¿Sobrescribir remoto guardando backup? (YES/no): " OK
if [[ "$OK" == "YES" ]]; then
  TAG="backup-remote-main-$(date +%Y%m%d-%H%M%S)"
  echo "==> Guardando backup del remoto: $TAG"
  git tag "$TAG" "$REMOTE/$BR" || true
  git push "$REMOTE" "$TAG" || true

  echo "==> Force-push con protección"
  git push --force-with-lease "$REMOTE" "$BR"
  echo "✅ Publicado forzando (backup remoto: $TAG)"
else
  echo "❌ Cancelado."
  exit 1
fi
