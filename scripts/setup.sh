#!/usr/bin/env bash
# DeckForge setup — install the dependencies needed by Phase 5 (.pptx assembly).
#
# Usage:
#   bash scripts/setup.sh                 # install everything recommended
#   bash scripts/setup.sh --minimal       # only python-pptx (smaller, but
#                                         #  Keynote / macOS Preview will see
#                                         #  blank slides; only PowerPoint
#                                         #  2016+ will display correctly)
#   bash scripts/setup.sh --yes           # skip the confirmation prompt
#
# What gets installed:
#   - python-pptx (~1 MB)      — required. Builds the .pptx file.
#                                Transitively pulls in lxml and Pillow.
#   - An SVG → PNG renderer    — strongly recommended. The script tries
#                                cairosvg first (pip), then suggests
#                                librsvg / Inkscape via OS package manager
#                                if cairosvg can't be installed.
#                                Without one of these, the PPTX renders
#                                blank in Keynote / macOS Preview / older
#                                PowerPoint (only PowerPoint 2016+ works).
#
# Phases 1–4 of the skill are pure Markdown and need none of the above.

set -e

WITH_RASTER=1   # default ON now (renderer is needed for cross-app compatibility)
AUTO_YES=0
for arg in "$@"; do
  case "$arg" in
    --minimal|--no-raster) WITH_RASTER=0 ;;
    --yes|-y)              AUTO_YES=1 ;;
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

# Detect existing renderers
EXISTING_RENDERER=""
if command -v rsvg-convert >/dev/null 2>&1; then EXISTING_RENDERER="rsvg-convert"; fi
if command -v inkscape    >/dev/null 2>&1 && [ -z "$EXISTING_RENDERER" ]; then EXISTING_RENDERER="inkscape"; fi
if "$PY" -c "import cairosvg" 2>/dev/null && [ -z "$EXISTING_RENDERER" ]; then EXISTING_RENDERER="cairosvg"; fi

# Tell the user what we're about to do
echo "DeckForge setup — about to install:"
echo "  • python-pptx                              ← required (Phase 5)"
if [ "$WITH_RASTER" = "1" ]; then
  if [ -n "$EXISTING_RENDERER" ]; then
    echo "  • (SVG renderer already present: $EXISTING_RENDERER — skipping)"
  else
    echo "  • cairosvg                                 ← SVG → PNG renderer"
    echo "    (fallback: librsvg via brew/apt if cairosvg's system libs are missing)"
  fi
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

if [ "$WITH_RASTER" = "1" ] && [ -z "$EXISTING_RENDERER" ]; then
  echo "→ Installing cairosvg ..."
  if "$PY" -m pip install $EXTRA cairosvg; then
    # Test cairosvg actually works (libcairo C lib must be present)
    if "$PY" -c "import cairosvg; cairosvg.svg2png(bytestring=b'<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"1\" height=\"1\"/>')" 2>/dev/null; then
      echo "   cairosvg OK."
    else
      echo "⚠️  cairosvg installed but libcairo C library is missing. Installing librsvg via OS package manager instead..."
      if command -v brew >/dev/null 2>&1; then
        brew install librsvg
      elif command -v apt-get >/dev/null 2>&1; then
        sudo apt-get install -y librsvg2-bin
      else
        echo "❌ Could not auto-install a renderer. Please install one of:"
        echo "     macOS:  brew install librsvg"
        echo "     Linux:  apt-get install librsvg2-bin"
        echo "     Or install Inkscape: https://inkscape.org/release/"
      fi
    fi
  else
    echo "⚠️  cairosvg pip install failed. Trying OS package manager for librsvg..."
    if command -v brew >/dev/null 2>&1; then
      brew install librsvg
    elif command -v apt-get >/dev/null 2>&1; then
      sudo apt-get install -y librsvg2-bin
    fi
  fi
fi

echo ""
echo "✅ Done."
echo "   Try:  $PY scripts/svg_to_pptx.py --help"
