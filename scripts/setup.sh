#!/usr/bin/env bash
# DeckForge setup — install the minimum dependency for the Phase 5 .pptx assembler.
#
# Usage:
#   bash scripts/setup.sh                 # install python-pptx (minimum)
#   bash scripts/setup.sh --with-raster   # also install cairosvg (for PNG fallback)
#   bash scripts/setup.sh --yes           # skip the confirmation prompt
#
# What gets installed:
#   - python-pptx (~1 MB)      — required. Builds the .pptx file in Phase 5.
#                                Transitively pulls in lxml and Pillow.
#   - cairosvg    (~600 KB)    — optional. Only with --with-raster.
#                                Renders a high-DPI PNG fallback for older
#                                PowerPoint versions / PDF preview tools.
#
# Nothing else is needed. Phases 1–4 of the skill are pure Markdown.

set -e

# Parse args
WITH_RASTER=0
AUTO_YES=0
for arg in "$@"; do
  case "$arg" in
    --with-raster) WITH_RASTER=1 ;;
    --yes|-y)      AUTO_YES=1 ;;
    -h|--help)
      head -n 15 "$0" | tail -n 14 | sed 's/^# \{0,1\}//'
      exit 0
      ;;
  esac
done

# Locate Python
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

# Detect --break-system-packages support (PEP 668 / Homebrew Python)
EXTRA=""
if "$PY" -m pip install --help 2>&1 | grep -q "break-system-packages"; then
  EXTRA="--break-system-packages"
fi

# Tell the user what we're about to do
echo "DeckForge setup — about to install:"
echo "  • python-pptx                              ← required for Phase 5 (.pptx assembly)"
if [ "$WITH_RASTER" = "1" ]; then
  echo "  • cairosvg                                 ← optional --with-raster path"
fi
echo "Using:  $($PY --version) ($PY -m pip ${EXTRA:-no-flag})"
echo ""

if [ "$AUTO_YES" = "0" ]; then
  if [ -t 0 ]; then
    read -r -p "Proceed? [Y/n] " ans
    case "$ans" in
      n|N|no|No) echo "Aborted."; exit 1 ;;
    esac
  fi
fi

echo "→ Installing python-pptx ..."
"$PY" -m pip install $EXTRA python-pptx

if [ "$WITH_RASTER" = "1" ]; then
  echo "→ Installing cairosvg ..."
  "$PY" -m pip install $EXTRA cairosvg || {
    echo "⚠️  cairosvg install failed. As a system-package alternative:"
    echo "    macOS:  brew install librsvg     (provides rsvg-convert)"
    echo "    Linux:  apt-get install librsvg2-bin"
    echo "    svg_to_pptx.py auto-detects whichever is available." >&2
  }
fi

echo ""
echo "✅ Done."
echo "   Try:  $PY scripts/svg_to_pptx.py --help"
