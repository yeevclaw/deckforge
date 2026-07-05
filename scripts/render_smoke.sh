#!/usr/bin/env bash
# Render one or more page/template SVGs to full-render PNGs — the shared render
# primitive for template smoke tests and Phase-4 eval output checks
# (.claude/skills/deckforge-verify). Every DeckForge template is a self-contained
# 1280×720 page, so any of them renders standalone.
#
# Usage:  bash scripts/render_smoke.sh <out-dir> <svg-file> [<svg-file>...]
# PNGs land in <out-dir>/<stem>.png. The cheap converter flags live here and
# only here (--no-pdf --no-decompose) so they can't drift across callers.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [ $# -lt 2 ]; then
  echo "usage: bash scripts/render_smoke.sh <out-dir> <svg-file>..." >&2
  exit 1
fi

OUT="$1"; shift
PAGES="$(mktemp -d)"
trap 'rm -rf "$PAGES"' EXIT

for f in "$@"; do
  [ -f "$f" ] || { echo "error: not a file: $f" >&2; exit 1; }
  cp "$f" "$PAGES/"
done

mkdir -p "$OUT"
python3 "$ROOT/scripts/svg_to_pptx.py" --pages-dir "$PAGES" \
  --output "$PAGES/smoke.pptx" --no-pdf --no-decompose --workdir "$OUT" >/dev/null

ls "$OUT"/*.png | grep -v '_placeholder\.png$'
