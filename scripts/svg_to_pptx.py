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

The PNG fallback is rendered using whichever SVG renderer is available,
in this preference order:
  resvg-py → cairosvg → inkscape → rsvg-convert

resvg-py is the only one with **zero system dependencies** — it ships a
pure Rust binary inside a pip wheel, available for Python 3.9+ on
macOS / Linux / Windows. That's why setup.sh installs it by default.

If none of these is installed, a 1×1 transparent placeholder PNG is used
(sufficient for PowerPoint 2016+ but will look blank in Keynote /
macOS Preview) and a warning is printed.

Required dependency:    python-pptx       (pip install python-pptx)
Strongly recommended:   resvg-py          (pip install resvg-py)
                        img2pdf           (pip install img2pdf)
                                          enables the companion .pdf alongside the .pptx
Alternatives:           cairosvg          pip install cairosvg + libcairo
                        rsvg-convert      brew install librsvg / apt librsvg2-bin
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

# img2pdf is optional — used to also emit a .pdf alongside the .pptx.
try:
    import img2pdf  # type: ignore
    _HAS_IMG2PDF = True
except ImportError:
    _HAS_IMG2PDF = False

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


# ---------- SVG → PNG rendering ----------

def _render_with_resvg_py(svg_path: Path, png_path: Path, width: int) -> bool:
    try:
        import resvg_py
    except ImportError:
        return False
    svg_data = svg_path.read_text(encoding="utf-8")
    try:
        png_bytes = resvg_py.svg_to_bytes(svg_string=svg_data, width=width)
    except Exception as e:
        print(f"[svg_to_pptx] resvg-py failed on {svg_path.name}: {e}", file=sys.stderr)
        return False
    png_path.write_bytes(bytes(png_bytes))
    return True


def _render_with_cairosvg(svg_path: Path, png_path: Path, width: int) -> bool:
    try:
        import cairosvg
    except ImportError:
        return False
    try:
        cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), output_width=width)
    except Exception as e:
        # cairosvg installs cleanly but fails at runtime if libcairo C lib is missing.
        print(f"[svg_to_pptx] cairosvg failed on {svg_path.name}: {e}", file=sys.stderr)
        return False
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
        ("resvg-py", _render_with_resvg_py),     # pure-pip, no system deps
        ("cairosvg", _render_with_cairosvg),     # needs libcairo
        ("inkscape", _render_with_inkscape),     # separate binary
        ("rsvg-convert", _render_with_rsvg),     # native lib
    ):
        if fn(svg_path, png_path, width):
            return name
    return None


def verify_renderer_works(test_svg: Path) -> str | None:
    """Do one real render to confirm at least one renderer actually works
    (catches cairosvg-installed-but-libcairo-missing-style failures up front)."""
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        return render_real_png(test_svg, tmp_path, width=64)
    finally:
        tmp_path.unlink(missing_ok=True)


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


def strip_notes_infrastructure(pptx_path: Path) -> None:
    """python-pptx's notes_text_frame mechanism leaves Content_Types overrides
    and slide rels that Keynote refuses to parse — it shows "invalid file
    format" and won't open the file at all.

    We strip ALL notes-related parts and references after python-pptx saves,
    leaving a clean image-based PPTX that opens in Keynote / PowerPoint /
    Preview / Quick Look uniformly. Notes content is preserved in a sibling
    `<stem>.notes.md` file by save_notes_sidecar() — not in the .pptx itself.

    Skipped when --keep-notes is set (PowerPoint-only workflows).
    """
    import re
    import tempfile
    import shutil
    import zipfile

    tmp_path = pptx_path.with_suffix(".tmp.pptx")
    with zipfile.ZipFile(pptx_path) as zin, \
         zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.namelist():
            # Drop notes-related parts entirely
            if ("notesSlide" in item or
                "notesMaster" in item or
                item.endswith("theme2.xml")):
                continue
            data = zin.read(item)
            if item == "[Content_Types].xml":
                text = data.decode("utf-8")
                text = re.sub(r"<Override[^>]*notesSlide[^>]*/>", "", text)
                text = re.sub(r"<Override[^>]*notesMaster[^>]*/>", "", text)
                # Also drop the theme2 override since we drop the file
                text = re.sub(r'<Override[^>]*PartName="/ppt/theme/theme2\.xml"[^>]*/>',
                              "", text)
                data = text.encode("utf-8")
            if item.endswith(".rels"):
                text = data.decode("utf-8")
                text = re.sub(r"<Relationship[^>]*notesSlide[^>]*/>", "", text)
                text = re.sub(r"<Relationship[^>]*notesMaster[^>]*/>", "", text)
                data = text.encode("utf-8")
            zout.writestr(item, data)
    shutil.move(tmp_path, pptx_path)


def save_notes_sidecar(pptx_path: Path, planning: dict) -> Path | None:
    """Write speaker notes as a sibling `.notes.md` file so the planner's
    speaker_notes aren't lost when we strip notes from the .pptx for Keynote
    compatibility. Returns the sidecar path, or None if there were no notes."""
    pages = planning.get("pages") or []
    notes = [(i + 1, p.get("speaker_notes", "")) for i, p in enumerate(pages)
             if p.get("speaker_notes")]
    if not notes:
        return None
    out = pptx_path.with_suffix(".notes.md")
    lines = [f"# Speaker notes — {pptx_path.stem}", ""]
    for idx, note in notes:
        lines.append(f"## Slide {idx}")
        lines.append("")
        lines.append(note.strip())
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def build(pages: list[Path], out_path: Path, planning: dict,
          workdir: Path, png_width: int,
          placeholder_only: bool, embed_svg: bool,
          also_pdf: bool, pdf_path: Path | None,
          keep_notes: bool):
    workdir.mkdir(parents=True, exist_ok=True)
    prs = Presentation()
    prs.slide_width = SLIDE_W_EMU
    prs.slide_height = SLIDE_H_EMU

    placeholder_path = workdir / "_placeholder.png"
    if not placeholder_path.exists():
        placeholder_path.write_bytes(_PLACEHOLDER_PNG_BYTES)

    real_pngs = []   # ordered list of per-slide PNG paths used for the optional PDF
    slide_objs = []  # ordered list of slide objects, for the notes second-pass
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
                    print("⚠️  No SVG renderer found. "
                          "Falling back to a 1×1 transparent placeholder PNG.",
                          file=sys.stderr)
                    print("    The .pptx will look BLANK in Keynote / macOS Preview / "
                          "older PowerPoint. Easiest fix:",
                          file=sys.stderr)
                    print("      pip install resvg-py --break-system-packages",
                          file=sys.stderr)
                    print("    (zero system deps; prebuilt wheels for all major platforms.)",
                          file=sys.stderr)
                    engine_reported = True
                png_path = placeholder_path
                used_placeholder_anywhere = True
            elif not engine_reported:
                print(f"PNG fallback engine: {engine} ({png_width}px wide)")
                engine_reported = True

        real_pngs.append(png_path)
        print(f"[{i+1}/{len(pages)}] {svg_path.name} → slide", flush=True)
        slide = add_svg_slide(prs, svg_path, png_path, embed_svg=embed_svg)
        slide_objs.append(slide)

    # Speaker notes — only if --keep-notes is set. By default we strip notes
    # entirely from the .pptx and save them to a sibling .notes.md, because
    # python-pptx's notes infrastructure makes Keynote reject the file.
    if keep_notes:
        for i, slide in enumerate(slide_objs):
            notes = speaker_notes_for(i, planning)
            if notes:
                slide.notes_slide.notes_text_frame.text = notes

    prs.save(str(out_path))

    if not keep_notes:
        # Always strip after save — python-pptx may have added stray notes
        # infrastructure (notesMaster, theme2) even when no notes were set.
        strip_notes_infrastructure(out_path)

    print(f"✅ Wrote PPTX: {out_path}")
    if embed_svg:
        print("   (In PowerPoint 2016+: right-click a slide → Convert to Shape to edit.)")

    # Save sidecar notes file (regardless of --keep-notes, so notes are always
    # recoverable from a human-readable source).
    notes_md = save_notes_sidecar(out_path, planning)
    if notes_md:
        print(f"📝 Wrote notes: {notes_md}")
    if used_placeholder_anywhere and not placeholder_only:
        print("⚠️  Some slides used the 1×1 placeholder because no SVG renderer was "
              "available. Re-run after installing one for proper Keynote / Preview display.")

    # Emit the companion PDF if requested.
    if also_pdf:
        if not _HAS_IMG2PDF:
            print("⚠️  Skipping PDF: img2pdf not installed. To enable, run:",
                  file=sys.stderr)
            print("      pip install img2pdf --break-system-packages",
                  file=sys.stderr)
            return
        if placeholder_only:
            # User explicitly chose 1×1 transparent placeholders — a PDF built
            # from those would be entirely blank, so skip rather than mislead.
            print("⚠️  Skipping PDF: --placeholder-only mode produces no real "
                  "PNG renders, so the PDF would be blank.", file=sys.stderr)
            return
        if used_placeholder_anywhere:
            # Some slides fell back to placeholder because the renderer failed
            # mid-stream — PDF would be partly blank, skip it.
            print("⚠️  Skipping PDF: no real PNG renders are available "
                  "(no SVG renderer installed).", file=sys.stderr)
            return
        pdf_out = pdf_path or out_path.with_suffix(".pdf")
        write_pdf(real_pngs, pdf_out)
        print(f"✅ Wrote PDF:  {pdf_out}")
        print()
        # Aggregate the deliverables — exact count depends on whether speaker
        # notes were extracted. Notes sidecar is reported separately above.
        notes_sidecar = out_path.with_suffix(".notes.md")
        deliverables = [out_path, pdf_out]
        if notes_sidecar.exists():
            deliverables.append(notes_sidecar)
        print()
        print("=" * 70)
        print(f"⚠️  CRITICAL: {len(deliverables)} files produced. DELIVER ALL OF THEM.")
        print(f"   The user expects every one of these in their chat / Downloads:")
        for p in deliverables:
            print(f"     • {p}")
        print("   Delivering only the .pptx and dropping the .pdf/.notes.md")
        print("   is the #1 DeckForge bug. Do not do this.")
        print("=" * 70)


def write_pdf(png_paths: list[Path], pdf_path: Path) -> None:
    """Assemble per-slide PNGs into a single multi-page PDF via img2pdf."""
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    # img2pdf accepts a list of file paths or bytes; paths is simpler.
    paths_str = [str(p) for p in png_paths]
    # Set page size to match a standard 16:9 slide so the PDF previews at the
    # right aspect on any reader. img2pdf computes from image DPI by default;
    # we override via layout_fun for an exact 13.333" × 7.5" page.
    layout = img2pdf.get_layout_fun(
        pagesize=(img2pdf.in_to_pt(13.333), img2pdf.in_to_pt(7.5)),
    )
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(paths_str, layout_fun=layout))


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
    p.add_argument("--no-pdf", action="store_true",
                   help="Skip the companion .pdf (by default, a PDF with the same "
                        "stem as --output is written alongside the .pptx).")
    p.add_argument("--pdf-output", default=None,
                   help="Explicit PDF path. If omitted, derived from --output by "
                        "swapping .pptx → .pdf.")
    p.add_argument("--keep-notes", action="store_true",
                   help="Embed speaker notes inside the .pptx via python-pptx. "
                        "Default is OFF because python-pptx's notes infrastructure "
                        "makes Keynote refuse the file. Notes are always written "
                        "to a sibling <stem>.notes.md regardless of this flag.")
    p.add_argument("--workdir", default=None,
                   help="Directory for intermediate files (default: <pages-dir>/_renders)")
    args = p.parse_args()

    pages_dir = Path(args.pages_dir).resolve()
    out_path = Path(args.output).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    planning_path = Path(args.planning).resolve() if args.planning else None
    workdir = Path(args.workdir).resolve() if args.workdir else pages_dir / "_renders"
    pdf_path = Path(args.pdf_output).resolve() if args.pdf_output else None

    pages = collect_pages(pages_dir)
    planning = load_planning(planning_path, pages_dir)

    # Fail fast: --no-svg requires a working SVG renderer. Without one, every
    # slide would be just the 1×1 transparent placeholder PNG → an all-blank
    # PPTX in every viewer. That's the worst kind of silent failure.
    if args.no_svg and not args.placeholder_only:
        engine = verify_renderer_works(pages[0])
        if engine is None:
            print("❌ --no-svg requires an SVG renderer, but none is available.",
                  file=sys.stderr)
            print("   Without one, every slide will be a 1×1 transparent PNG "
                  "(blank everywhere).", file=sys.stderr)
            print("   Pick one of these fixes:", file=sys.stderr)
            print("     pip install resvg-py --break-system-packages",
                  file=sys.stderr)
            print("     brew install librsvg          (macOS)", file=sys.stderr)
            print("     apt-get install librsvg2-bin  (Linux)", file=sys.stderr)
            print("   Or remove --no-svg — the default svgBlip mode embeds "
                  "the SVG so modern PowerPoint can render it directly.",
                  file=sys.stderr)
            sys.exit(2)

    build(pages, out_path, planning, workdir, args.png_width,
          placeholder_only=args.placeholder_only,
          embed_svg=not args.no_svg,
          also_pdf=not args.no_pdf,
          pdf_path=pdf_path,
          keep_notes=args.keep_notes)


if __name__ == "__main__":
    main()
