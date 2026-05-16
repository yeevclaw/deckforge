# DeckForge setup — install the minimum dependency needed to run svg_to_pptx.py.
#
# Usage (PowerShell):
#   .\scripts\setup.ps1
#   .\scripts\setup.ps1 -WithRaster   # also install cairosvg for PNG fallback
#
# Phases 1–4 of the skill are pure Markdown and need no install.
# Only Phase 5 (the .pptx assembler) needs python-pptx.

param(
    [switch]$WithRaster
)

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

if ($WithRaster) {
    Write-Host "→ Installing cairosvg (for high-DPI PNG fallback) ..."
    try {
        & $py -m pip install cairosvg
    } catch {
        Write-Warning "cairosvg install failed. You can also install Inkscape (https://inkscape.org/release/) -- svg_to_pptx.py will detect it."
    }
}

Write-Host "✅ Done. Try:  $py scripts\svg_to_pptx.py --help"
