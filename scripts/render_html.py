"""
Render HTML files to high-DPI PNG images.

Primary path: Playwright + Chromium (best quality, modern CSS, web fonts).
Fallback path: LibreOffice headless (limited CSS support, but no extra deps).

Used as a library by html_to_pptx.py, but also runnable standalone.

Standalone usage:
    python render_html.py page.html page.png --width 1280 --height 720 --scale 2

The output PNG will be width*scale by height*scale pixels.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def render_with_playwright(html_path: Path, png_path: Path,
                           width: int = 1280, height: int = 720,
                           device_scale_factor: float = 2.0) -> bool:
    """Render with Playwright + Chromium. Returns True on success."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False

    abs_html = html_path.resolve()
    url = f"file://{abs_html}"

    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch(args=["--no-sandbox"])
        except Exception as e:
            print(f"[render_html] Chromium launch failed: {e}", file=sys.stderr)
            return False
        try:
            ctx = browser.new_context(
                viewport={"width": width, "height": height},
                device_scale_factor=device_scale_factor,
            )
            page = ctx.new_page()
            page.goto(url, wait_until="networkidle", timeout=15000)
            # Wait briefly for fonts (system fonts only, but harmless)
            page.wait_for_timeout(150)
            page.screenshot(path=str(png_path), full_page=False,
                            clip={"x": 0, "y": 0, "width": width, "height": height},
                            omit_background=False)
        finally:
            browser.close()
    return True


def render_with_libreoffice(html_path: Path, png_path: Path,
                            width: int = 1280, height: int = 720,
                            device_scale_factor: float = 2.0) -> bool:
    """
    Fallback: LibreOffice headless. Limited CSS support — Bento Grid pages
    will mostly NOT render correctly here. Provided as a last resort.
    """
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    pdftoppm = shutil.which("pdftoppm")
    if not soffice or not pdftoppm:
        return False

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        # html -> pdf
        try:
            subprocess.run(
                [soffice, "--headless", "--convert-to", "pdf",
                 "--outdir", str(tmpdir), str(html_path)],
                check=True, capture_output=True, timeout=60,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            print(f"[render_html] LibreOffice conversion failed: {e}", file=sys.stderr)
            return False
        pdf = tmpdir / (html_path.stem + ".pdf")
        if not pdf.exists():
            return False

        # pdf -> png (single page, target DPI)
        dpi = int(72 * device_scale_factor * 2)  # rough scale
        try:
            subprocess.run(
                [pdftoppm, "-png", "-r", str(dpi), "-f", "1", "-l", "1",
                 str(pdf), str(tmpdir / "out")],
                check=True, capture_output=True, timeout=30,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            print(f"[render_html] pdftoppm failed: {e}", file=sys.stderr)
            return False
        # pdftoppm output is "out-1.png" or "out-01.png" depending on count
        for cand in tmpdir.glob("out-*.png"):
            shutil.copy(cand, png_path)
            return True
    return False


def render(html_path: Path, png_path: Path,
           width: int = 1280, height: int = 720,
           device_scale_factor: float = 2.0,
           prefer: str = "auto") -> str:
    """
    Render html_path to png_path.

    prefer: "auto" | "playwright" | "libreoffice"

    Returns the name of the engine that succeeded, raises RuntimeError if none worked.
    """
    html_path = Path(html_path)
    png_path = Path(png_path)
    png_path.parent.mkdir(parents=True, exist_ok=True)

    if prefer in ("auto", "playwright"):
        if render_with_playwright(html_path, png_path, width, height, device_scale_factor):
            return "playwright"
        if prefer == "playwright":
            raise RuntimeError("Playwright requested but not available. Install with: "
                               "pip install playwright && playwright install chromium")

    if prefer in ("auto", "libreoffice"):
        if render_with_libreoffice(html_path, png_path, width, height, device_scale_factor):
            return "libreoffice"
        if prefer == "libreoffice":
            raise RuntimeError("LibreOffice fallback failed.")

    raise RuntimeError(
        "No HTML renderer available. Install one of:\n"
        "  - Playwright (recommended): pip install playwright && playwright install chromium\n"
        "  - LibreOffice + Poppler: apt-get install libreoffice poppler-utils"
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("html", help="Input HTML file")
    p.add_argument("png", help="Output PNG file")
    p.add_argument("--width", type=int, default=1280)
    p.add_argument("--height", type=int, default=720)
    p.add_argument("--scale", type=float, default=2.0,
                   help="Device scale factor — final image is width*scale by height*scale")
    p.add_argument("--engine", default="auto",
                   choices=["auto", "playwright", "libreoffice"])
    args = p.parse_args()

    engine = render(Path(args.html), Path(args.png),
                    args.width, args.height, args.scale, args.engine)
    print(f"Rendered with {engine}: {args.png}")


if __name__ == "__main__":
    main()
