#!/usr/bin/env python3
"""Hard-invariant lint for DeckForge page/template SVGs — stdlib only, read-only.

Scripts the machine-checkable subset of the designer self-check
(prompts/05_designer_svg.md → Quality checklist). Only zero-false-positive
rules gate (errors); judgment calls (margins, contrast, palette, whether an
emoji is decorative or a functional icon) stay with the Phase 5 visual grader.

Errors (exit 1):
  - root viewBox is not exactly "0 0 1280 720"
  - no real <text> element (skipped for _base.svg — it's a defs library)
  - placeholder strings left in (Lorem / TBD / xxx)
  - external network reference (href/src/url() to http[s]://)
  - <script> element present
Warnings (reported, never gate):
  - emoji codepoints in text content (decorative emoji are allowed;
    emoji-as-functional-icon is the grader's judgment, rubric P5-06)

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
