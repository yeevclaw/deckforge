#!/usr/bin/env bash
# DeckForge setup — install the two Python packages Phase 5 needs.
#
# Usage:
#   bash scripts/setup.sh         # install python-pptx + resvg-py
#   bash scripts/setup.sh --yes   # skip the confirmation prompt
#   bash scripts/setup.sh --minimal   # only python-pptx (decks render blank
#                                      # in Keynote / macOS Preview without
#                                      # a renderer; only PowerPoint 2016+ works)
#
# What gets installed:
#   - python-pptx (~1 MB)   ← required. Builds the .pptx file.
#                              Transitively pulls in lxml + Pillow.
#   - resvg-py    (~1 MB)   ← strongly recommended. Pure-pip Rust SVG renderer
#                              with zero system dependencies. Produces the PNG
#                              fallback that makes the deck display correctly
#                              in Keynote, macOS Preview, Quick Look, and older
#                              PowerPoint. Prebuilt wheels for Python 3.9+ on
#                              macOS / Linux / Windows.
#
# Phases 1–4 of the skill are pure Markdown and need none of the above.

set -e

WITH_RENDERER=1
AUTO_YES=0
for arg in "$@"; do
  case "$arg" in
    --minimal|--no-renderer) WITH_RENDERER=0 ;;
    --yes|-y)                AUTO_YES=1 ;;
    -h|--help)
      head -n 22 "$0" | tail -n 21 | sed 's/^# \{0,1\}//'
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

echo "DeckForge setup — about to install:"
echo "  • python-pptx                              ← required (.pptx assembly)"
if [ "$WITH_RENDERER" = "1" ]; then
  echo "  • resvg-py                                 ← SVG → PNG renderer"
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

if [ "$WITH_RENDERER" = "1" ]; then
  echo "→ Installing resvg-py ..."
  if "$PY" -m pip install $EXTRA resvg-py; then
    echo "   resvg-py OK."
  else
    echo "⚠️  resvg-py install failed. If your platform has no prebuilt wheel," >&2
    echo "    try a system renderer instead:" >&2
    echo "      brew install librsvg          (macOS)" >&2
    echo "      apt-get install librsvg2-bin  (Linux)" >&2
    echo "    or install Inkscape: https://inkscape.org/release/" >&2
  fi
fi

echo ""
echo "✅ Done."
echo "   Try:  $PY scripts/svg_to_pptx.py --help"
