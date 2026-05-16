#!/usr/bin/env bash
# DeckForge setup — install the minimum dependency needed to run svg_to_pptx.py.
#
# Usage:  bash scripts/setup.sh
#
# What it does:
#   1. Picks a Python (python3 / python).
#   2. Installs python-pptx (transitively pulls in lxml + Pillow).
#   3. Optionally installs cairosvg if you pass --with-raster.
#
# That's all you need. The skill itself (Phase 1–4) is pure Markdown — no deps.

set -e

PY=""
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1; then
    PY="$candidate"
    break
  fi
done
if [ -z "$PY" ]; then
  echo "❌ Python not found. Install Python 3.9+ first." >&2
  exit 1
fi

echo "→ Using $($PY --version)"

# Detect if pip needs --break-system-packages (PEP 668 / Homebrew Python).
EXTRA=""
if "$PY" -m pip install --help 2>&1 | grep -q "break-system-packages"; then
  EXTRA="--break-system-packages"
fi

echo "→ Installing python-pptx ..."
"$PY" -m pip install $EXTRA python-pptx

if [ "${1:-}" = "--with-raster" ]; then
  echo "→ Installing cairosvg (for high-DPI PNG fallback) ..."
  "$PY" -m pip install $EXTRA cairosvg || {
    echo "⚠️  cairosvg install failed. You can also use Inkscape (brew install inkscape) "
    echo "    or librsvg2-bin (apt-get install librsvg2-bin) — svg_to_pptx.py will detect "
    echo "    whichever is available." >&2
  }
fi

echo "✅ Done. Try:  $PY scripts/svg_to_pptx.py --help"
