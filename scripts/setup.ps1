# DeckForge setup — install the three Phase 5 dependencies for svg_to_pptx.py.
#
# Usage (PowerShell):
#   .\scripts\setup.ps1
#
# What gets installed:
#   - python-pptx           ← required, builds the .pptx file
#   - resvg-py              ← SVG → PNG renderer (zero system deps)
#   - img2pdf               ← PNG → PDF (companion .pdf alongside .pptx)
#
# Phases 1–4 of the skill are pure Markdown and need none of these.

$ErrorActionPreference = "Stop"

$py = $null
foreach ($cand in @("python", "python3", "py")) {
    if (Get-Command $cand -ErrorAction SilentlyContinue) {
        $py = $cand
        break
    }
}
if (-not $py) {
    Write-Error "Python not found. Install Python 3.9+ first (https://www.python.org/downloads/)."
    exit 1
}

Write-Host "→ Using $(& $py --version)"

Write-Host "→ Installing python-pptx ..."
& $py -m pip install python-pptx

Write-Host "→ Installing resvg-py (SVG → PNG renderer) ..."
try {
    & $py -m pip install resvg-py
} catch {
    Write-Warning "resvg-py install failed. As a fallback install Inkscape (https://inkscape.org/release/) -- svg_to_pptx.py will detect it."
}

Write-Host "→ Installing img2pdf (companion .pdf assembler) ..."
try {
    & $py -m pip install img2pdf
} catch {
    Write-Warning "img2pdf install failed -- the companion .pdf will be skipped."
}

Write-Host "✅ Done. Try:  $py scripts\svg_to_pptx.py --help"
