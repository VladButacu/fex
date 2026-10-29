#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="$(python3 - <<'PY' "$ROOT/plugins/fex/plugin.json"
import json,sys
print(json.load(open(sys.argv[1]))['version'])
PY
)"
DIST="$ROOT/.dist"
rm -rf "$DIST"
mkdir -p "$DIST"
python3 "$ROOT/scripts/validate.py"
(
  cd "$ROOT/.."
  zip -qr "$DIST/frontend-excellence-v${VERSION}.zip" "$(basename "$ROOT")" \
    -x '*/.git/*' '*/.dist/*' '*/__pycache__/*' '*.pyc'
)
(
  cd "$ROOT/plugins"
  zip -qr "$DIST/fex-plugin-v${VERSION}.zip" fex -x '*/__pycache__/*' '*.pyc'
)
if command -v shasum >/dev/null 2>&1; then
  (cd "$DIST" && shasum -a 256 *.zip > SHA256SUMS)
else
  (cd "$DIST" && sha256sum *.zip > SHA256SUMS)
fi
printf 'Built release artifacts in %s\n' "$DIST"
