"""
Convert a directory of SVG slide pages to a PPTX deck.

Each .svg file in --pages-dir becomes one slide (16:9, 1280×720 viewBox).
Pages are ordered by filename (so name them page_01.svg, page_02.svg, ...).

If a planning.json sits next to the pages dir (or is passed via --planning),
speaker_notes are attached to each slide.

Each slide's picture is embedded as:
  1. A rasterized PNG fallback (so Keynote, macOS Preview, Quick Look,
     PowerPoint <2016, web-mail previewers, etc. all display the slide
     correctly).
  2. The original SVG via the PowerPoint 2016+ svgBlip OOXML extension
     (so PowerPoint 2016+ renders the vector and the user can
     right-click → "Convert to Shape" to edit every text run).

The PNG fallback is rendered using whichever SVG renderer is available:
cairosvg → inkscape → rsvg-convert. If none is installed, a 1×1
transparent placeholder PNG is used (sufficient for PowerPoint 2016+ but
will look blank in Keynote / macOS Preview) and a warning is printed.

Required dependency:    python-pptx       (pip install python-pptx)
Strongly recommended:   cairosvg (or)     pip install cairosvg
                        rsvg-convert      brew install librsvg
                        inkscape          brew install inkscape

Flags:
  --no-svg            Skip the svgBlip extension; PPTX becomes image-only.
                      Use this if a viewer chokes on the SVG ext (some
                      older Keynote versions).
  --placeholder-only  Force the 1×1 transparent placeholder PNG even when
                      a real renderer is available. Smaller file, but the
                      slide only displays in PowerPoint 2016+.
  --png-width N       Width (px) of the PNG fallback. Default 2560 (2× DPI).

Examples:
  python svg_to_pptx.py --pages-dir pages/ --output deck.pptx
  python svg_to_pptx.py --pages-dir pages/ --output deck.pptx --no-svg
  python svg_to_pptx.py --pages-dir pages/ --output deck.pptx --planning planning.json
"""
from __future__ import annotations

import argparse
import base64
import json
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from pptx import Presentation
    from pptx.util import Emu
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT
    from pptx.opc.package import Part
    from pptx.opc.packuri import PackURI
    from pptx.oxml.ns import qn
    from lxml import etree
except ImportError as e:
    sys.stderr.write(
        f"Missing dependency: {e}\n"
        "Install: pip install python-pptx --break-system-packages\n"
        "(python-pptx pulls in lxml + Pillow automatically.)\n"
    )
    sys.exit(1)

SVG_EXT_URI = "{96DAC541-7B7A-43D3-8B79-37D633B846F1}"
SVG_NS = "http://schemas.microsoft.com/office/drawing/2016/SVG/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

# 16:9 standard slide @ 96 dpi == 1280×720 logical
SLIDE_W_EMU = Emu(int(13.333 * 914400))
SLIDE_H_EMU = Emu(int(7.5 * 914400))

# A valid 1×1 fully-transparent PNG. PowerPoint stretches it to fill the slide;
# since it's transparent, the SVG vector layer above is what the viewer sees.
# This satisfies the OOXML requirement that <a:blip> reference an image.
_PLACEHOLDER_PNG_BYTES = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlE"
    "QVR42mNk+P+/HgAFhAJ/wlseKgAAAABJRU5ErkJggg=="
)


# ---------- Optional SVG → PNG rendering (only when --with-raster) ----------

def _render_with_cairosvg(svg_path: Path, png_path: Path, width: int) -> bool:
    try:
        import cairosvg
    except ImportError:
        return False
    cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), output_width=width)
    return True


def _render_with_inkscape(svg_path: Path, png_path: Path, width: int) -> bool:
    ink = shutil.which("inkscape")
    if not ink:
        return False
    try:
        subprocess.run(
            [ink, "--export-type=png", f"--export-filename={png_path}",
             f"--export-width={width}", str(svg_path)],
            check=True, capture_output=True, timeout=30,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"[svg_to_pptx] inkscape failed: {e}", file=sys.stderr)
        return False
    return png_path.exists()


def _render_with_rsvg(svg_path: Path, png_path: Path, width: int) -> bool:
    rsvg = shutil.which("rsvg-convert")
    if not rsvg:
        return False
    try:
        subprocess.run(
            [rsvg, "-w", str(width), "-o", str(png_path), str(svg_path)],
            check=True, capture_output=True, timeout=30,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"[svg_to_pptx] rsvg-convert failed: {e}", file=sys.stderr)
        return False
    return png_path.exists()


def render_real_png(svg_path: Path, png_path: Path, width: int = 2560):
    """Render a high-DPI PNG fallback. Returns engine name, or None if no renderer."""
    png_path.parent.mkdir(parents=True, exist_ok=True)
    for name, fn in (
        ("cairosvg", _render_with_cairosvg),
        ("inkscape", _render_with_inkscape),
        ("rsvg-convert", _render_with_rsvg),
    ):
        if fn(svg_path, png_path, width):
            return name
    return None


# ---------- PPTX assembly ----------

def collect_pages(pages_dir: Path) -> list[Path]:
    pages = sorted(p for p in pages_dir.iterdir() if p.suffix.lower() == ".svg")
    if not pages:
        raise FileNotFoundError(f"No .svg files found in {pages_dir}")
    return pages


def load_planning(planning_path: Path | None, pages_dir: Path) -> dict:
    if planning_path and planning_path.exists():
        return json.loads(planning_path.read_text(encoding="utf-8"))
    default = pages_dir.parent / "planning.json"
    if default.exists():
        return json.loads(default.read_text(encoding="utf-8"))
    return {}


def speaker_notes_for(idx: int, planning: dict) -> str:
    pages = planning.get("pages") or []
    if 0 <= idx < len(pages):
        return pages[idx].get("speaker_notes", "") or ""
    return ""


def _next_partname(package, base: str, ext: str) -> PackURI:
    existing = {p.partname for p in package.iter_parts()}
    n = 1
    while True:
        candidate = PackURI(f"/ppt/media/{base}{n}.{ext}")
        if candidate not in existing:
            return candidate
        n += 1


def _add_svg_part(slide_part, svg_bytes: bytes) -> str:
    package = slide_part.package
    partname = _next_partname(package, "image", "svg")
    svg_part = Part(
        partname=partname,
        content_type="image/svg+xml",
        blob=svg_bytes,
        package=package,
    )
    return slide_part.relate_to(svg_part, RT.IMAGE)


def _inject_svg_ext(pic_elem, svg_rId: str):
    """Append <a:extLst><a:ext uri=...><asvg:svgBlip r:embed=svg_rId/></a:ext></a:extLst>
    to the <a:blip> inside the picture, so Office 2016+ renders the SVG vector."""
    blip = pic_elem.find('.//' + qn('a:blip'))
    if blip is None:
        return
    existing = blip.find(qn('a:extLst'))
    if existing is not None:
        blip.remove(existing)
    extLst = etree.SubElement(blip, qn('a:extLst'))
    ext = etree.SubElement(extLst, qn('a:ext'))
    ext.set('uri', SVG_EXT_URI)
    svgBlip = etree.SubElement(ext, f'{{{SVG_NS}}}svgBlip', nsmap={'asvg': SVG_NS})
    svgBlip.set(f'{{{R_NS}}}embed', svg_rId)


def add_svg_slide(prs, svg_path: Path, png_path: Path, embed_svg: bool):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    pic = slide.shapes.add_picture(
        str(png_path), 0, 0,
        width=prs.slide_width, height=prs.slide_height,
    )
    if embed_svg:
        svg_bytes = svg_path.read_bytes()
        svg_rId = _add_svg_part(slide.part, svg_bytes)
        _inject_svg_ext(pic._element, svg_rId)
    return slide


def build(pages: list[Path], out_path: Path, planning: dict,
          workdir: Path, png_width: int,
          placeholder_only: bool, embed_svg: bool):
    workdir.mkdir(parents=True, exist_ok=True)
    prs = Presentation()
    prs.slide_width = SLIDE_W_EMU
    prs.slide_height = SLIDE_H_EMU

    placeholder_path = workdir / "_placeholder.png"
    if not placeholder_path.exists():
        placeholder_path.write_bytes(_PLACEHOLDER_PNG_BYTES)

    engine_reported = False
    used_placeholder_anywhere = False
    for i, svg_path in enumerate(pages):
        if placeholder_only:
            png_path = placeholder_path
            used_placeholder_anywhere = True
        else:
            png_path = workdir / f"{svg_path.stem}.png"
            engine = render_real_png(svg_path, png_path, width=png_width)
            if engine is None:
                if not engine_reported:
                    print("⚠️  No SVG renderer found (cairosvg / inkscape / rsvg-convert). "
                          "Falling back to a 1×1 transparent placeholder PNG.",
                          file=sys.stderr)
                    print("    The .pptx will look BLANK in Keynote / macOS Preview / "
                          "older PowerPoint. To fix, install one of:",
                          file=sys.stderr)
                    print("      pip install cairosvg --break-system-packages", file=sys.stderr)
                    print("      brew install librsvg                          (mac)", file=sys.stderr)
                    print("      apt-get install librsvg2-bin                  (linux)", file=sys.stderr)
                    engine_reported = True
                png_path = placeholder_path
                used_placeholder_anywhere = True
            elif not engine_reported:
                print(f"PNG fallback engine: {engine} ({png_width}px wide)")
                engine_reported = True

        print(f"[{i+1}/{len(pages)}] {svg_path.name} → slide", flush=True)
        slide = add_svg_slide(prs, svg_path, png_path, embed_svg=embed_svg)

        notes = speaker_notes_for(i, planning)
        if notes:
            slide.notes_slide.notes_text_frame.text = notes

    prs.save(str(out_path))
    print(f"Wrote {out_path}")
    if embed_svg:
        print("In PowerPoint 2016+: right-click any slide picture → Convert to Shape "
              "to edit text and shapes.")
    if used_placeholder_anywhere and not placeholder_only:
        print("⚠️  Some slides used the 1×1 placeholder because no SVG renderer was "
              "available. Re-run after installing one for proper Keynote / Preview display.")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--pages-dir", required=True, help="Directory containing page_*.svg files")
    p.add_argument("--output", required=True, help="Output .pptx path")
    p.add_argument("--planning", default=None, help="planning.json path (auto-detected if omitted)")
    p.add_argument("--no-svg", action="store_true",
                   help="Skip the svgBlip extension; slides become image-only. "
                        "Use this for viewers that choke on the SVG ext.")
    p.add_argument("--placeholder-only", action="store_true",
                   help="Force the 1×1 transparent placeholder PNG fallback even "
                        "when a real renderer is available. Smaller file but only "
                        "displays correctly in PowerPoint 2016+.")
    p.add_argument("--png-width", type=int, default=2560,
                   help="Width (px) of the PNG fallback. Default 2560 (2× DPI).")
    p.add_argument("--workdir", default=None,
                   help="Directory for intermediate files (default: <pages-dir>/_renders)")
    args = p.parse_args()

    pages_dir = Path(args.pages_dir).resolve()
    out_path = Path(args.output).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    planning_path = Path(args.planning).resolve() if args.planning else None
    workdir = Path(args.workdir).resolve() if args.workdir else pages_dir / "_renders"

    pages = collect_pages(pages_dir)
    planning = load_planning(planning_path, pages_dir)
    build(pages, out_path, planning, workdir, args.png_width,
          placeholder_only=args.placeholder_only,
          embed_svg=not args.no_svg)


if __name__ == "__main__":
    main()
