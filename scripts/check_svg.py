#!/usr/bin/env python3
"""Hard-invariant lint for DeckForge page/template SVGs — stdlib only, read-only.

Scripts the machine-checkable subset of the designer rules
(prompts/05_designer_svg.md → Hard constraints + Quality checklist). Only zero-false-positive
rules gate (errors); judgment calls (margins, contrast, palette, whether an
emoji is decorative or a functional icon) stay with the Phase 5 visual grader.

Errors (exit 1):
  - root viewBox is not exactly "0 0 1280 720"
  - no real <text> element (skipped for _base.svg — it's a defs library)
  - placeholder strings left in (Lorem / TBD / xxx)
  - external network reference (href/src/url() to http[s]://)
  - <script> element present
  - reading-mode 16px floor (rubric P4-13): in a file whose root <svg> carries
    data-delivery-mode="reading", any text run whose effective font-size
    (nearest self/ancestor font-size attr or style, × ancestor uniform scale
    transforms; pt converted at 96/72) resolves below 16px. Files without the
    attribute are never checked — presenting-mode sizes are legitimate.
Warnings (reported, never gate):
  - emoji codepoints in text content (decorative emoji are allowed;
    emoji-as-functional-icon is the grader's judgment, rubric P5-06)
  - reading-mode text with a non-px/pt font-size unit (em/%/rem) — not
    statically resolvable, left to the visual grader

Usage:  python3 scripts/check_svg.py <file.svg | dir> [...]
        (a directory expands to its *.svg files, non-recursive)
"""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

VIEWBOX = "0 0 1280 720"
PLACEHOLDER_RE = re.compile(r"\blorem\b|\bTBD\b|\bxxx\b", re.IGNORECASE)
EXTERNAL_RE = re.compile(r"""(?:href|src)\s*=\s*["']https?://|url\(\s*["']?https?://""")
EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF☀-➿️]"
)


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


# --- reading-mode 16px floor (rubric P4-13) ----------------------------------
READING_FLOOR_PX = 16.0
_FONT_SIZE_STYLE_RE = re.compile(r"font-size\s*:\s*([0-9.]+)\s*([a-z%]*)", re.IGNORECASE)
_SCALE_RE = re.compile(r"scale\(\s*(-?[0-9.]+)\s*(?:[, ]\s*(-?[0-9.]+))?\s*\)")
_MATRIX_RE = re.compile(
    r"matrix\(\s*(-?[0-9.]+)[, ]\s*(-?[0-9.]+)[, ]\s*(-?[0-9.]+)[, ]\s*"
    r"(-?[0-9.]+)[, ]\s*(-?[0-9.]+)[, ]\s*(-?[0-9.]+)\s*\)"
)


def _own_font_size(el: ET.Element) -> tuple[float, str] | None:
    """The element's own font-size as (value, unit), attr first then style."""
    raw = el.get("font-size")
    if raw:
        m = re.match(r"\s*([0-9.]+)\s*([a-z%]*)\s*$", raw, re.IGNORECASE)
        if m:
            return float(m.group(1)), m.group(2).lower()
    m = _FONT_SIZE_STYLE_RE.search(el.get("style") or "")
    if m:
        return float(m.group(1)), m.group(2).lower()
    return None


def _transform_scale(el: ET.Element) -> float:
    """Combined uniform scale factor of the element's transform attribute
    (scale() uses min of x/y; matrix() uses sqrt(|det|); rotate/translate = 1)."""
    t = el.get("transform") or ""
    factor = 1.0
    for m in _SCALE_RE.finditer(t):
        sx = abs(float(m.group(1)))
        sy = abs(float(m.group(2))) if m.group(2) else sx
        factor *= min(sx, sy)
    for m in _MATRIX_RE.finditer(t):
        a, b, c, d = (float(m.group(i)) for i in range(1, 5))
        det = abs(a * d - b * c)
        factor *= det ** 0.5
    return factor


def _effective_font_size(chain: list[ET.Element]) -> tuple[float | None, str | None]:
    """Effective rendered size for the innermost element of an ancestor chain
    (root → … → element). Returns (px_size, non_px_unit): px_size is None when
    nothing declares a size (SVG default 16 — passes) or when a non-px/pt unit
    makes it unresolvable (unit returned for the warning)."""
    size: float | None = None
    for el in reversed(chain):  # innermost declaration wins
        own = _own_font_size(el)
        if own:
            value, unit = own
            if unit in ("", "px"):
                size = value
            elif unit == "pt":
                size = value * 96.0 / 72.0
            else:
                return None, unit
            break
    if size is None:
        return None, None
    scale = 1.0
    for el in chain:  # every ancestor's (and self's) transform applies
        scale *= _transform_scale(el)
    return size * scale, None


def check_reading_floor(root: ET.Element) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if root.get("data-delivery-mode") != "reading":
        return errors, warnings

    def snippet(s: str) -> str:
        s = " ".join(s.split())
        return s[:14] + ("…" if len(s) > 14 else "")

    def visit(el: ET.Element, chain: list[ET.Element]) -> None:
        chain = chain + [el]
        if local_name(el.tag) in ("text", "tspan", "textPath"):
            runs: list[str] = []
            if el.text and el.text.strip():
                runs.append(el.text)
            # a child's tail renders with THIS element's style
            runs += [c.tail for c in el if c.tail and c.tail.strip()]
            for run in runs:
                size, unit = _effective_font_size(chain)
                if unit is not None:
                    warnings.append(
                        f'reading-mode text "{snippet(run)}" uses font-size unit '
                        f'"{unit}" — not statically resolvable, grader\'s call'
                    )
                elif size is not None and size < READING_FLOOR_PX:
                    errors.append(
                        f'reading-mode floor: text "{snippet(run)}" resolves to '
                        f"{size:g}px — minimum is 16px / 12pt (rubric P4-13)"
                    )
        for child in el:
            visit(child, chain)

    for child in root:
        visit(child, [root])
    return errors, warnings


def lint_file(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")

    try:
        root = ET.fromstring(text)
    except ET.ParseError as e:
        return [f"not well-formed XML: {e}"], []

    vb = " ".join((root.get("viewBox") or "").split())
    if vb != VIEWBOX:
        errors.append(f'viewBox is "{vb or "(missing)"}", must be "{VIEWBOX}"')

    tags = [local_name(el.tag) for el in root.iter()]
    if path.name != "_base.svg" and tags.count("text") == 0:
        errors.append("no real <text> element — text as paths breaks Convert-to-Shape editability")
    if "script" in tags:
        errors.append("<script> element present")

    m = PLACEHOLDER_RE.search(text)
    if m:
        errors.append(f'placeholder string left in ("{m.group(0)}")')
    if EXTERNAL_RE.search(text):
        errors.append("external network reference (http[s]:// in href/src/url)")

    emoji = sorted({c for c in text if EMOJI_RE.match(c)})
    if emoji:
        warnings.append(
            f"emoji codepoints present ({' '.join(emoji[:5])}) — fine if decorative; "
            f"emoji-as-icon is the visual grader's call (P5-06)"
        )

    floor_errors, floor_warnings = check_reading_floor(root)
    errors.extend(floor_errors)
    warnings.extend(floor_warnings)
    return errors, warnings


def expand(args: list[str]) -> list[Path]:
    files: list[Path] = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            files.extend(sorted(p.glob("*.svg")))
        else:
            files.append(p)
    return files


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: python3 scripts/check_svg.py <file.svg | dir> [...]", file=sys.stderr)
        return 2
    files = expand(argv)
    if not files:
        print("no .svg files found", file=sys.stderr)
        return 2

    failed = False
    for f in files:
        if not f.exists():
            print(f"❌ {f}: file not found")
            failed = True
            continue
        errors, warnings = lint_file(f)
        if errors:
            failed = True
            print(f"❌ {f}")
            for e in errors:
                print(f"   - {e}")
        else:
            print(f"✅ {f}")
        for w in warnings:
            print(f"   ⚠ {w}")

    if failed:
        print("\nSVG hard-invariant lint FAILED.")
        return 1
    print("\nAll SVG hard-invariant checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
