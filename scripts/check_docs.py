#!/usr/bin/env python3
"""Doc-drift guard for DeckForge — stdlib only, read-only.

DeckForge states the same rule in several files on purpose (CLAUDE.md: "Rules
are intentionally stated in multiple places ... Doc drift is the recurring bug
class here"). The cost of that intent is drift: a rule changes in one place and
the copies rot. This script asserts the cross-stated invariants that have
actually drifted, so a maintainer (or CI / a pre-commit hook) can catch them
mechanically instead of by grep-and-remember.

It runs every check, prints a line per check, and exits non-zero if any failed.

Usage (from anywhere):  python scripts/check_docs.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


# --- Check 1: template count -------------------------------------------------
# Ground truth = number of templates/*.svg (includes _base.svg). Every doc that
# states a "total" count must match it. We match only TOTAL-count phrasings and
# deliberately skip "starting templates" / "起始模板" wordings (those state the
# count minus _base, e.g. "26 SVG starting templates + _base = 27 files total").
TEMPLATE_COUNT_FILES = ["SKILL.md", "README.md", "README.en.md", "CLAUDE.md"]
TOTAL_CLAIM_PATTERNS = [
    r"(\d+)\s+files total",   # SKILL.md, CLAUDE.md
    r"(\d+)\s+SVG files",     # README.en.md
    r"(\d+)\s*個\s*viewBox",  # README.md (zh)
]


def check_template_count() -> list[str]:
    errors: list[str] = []
    truth = len(list((ROOT / "templates").glob("*.svg")))
    for rel in TEMPLATE_COUNT_FILES:
        text = read(rel)
        found = [int(m) for pat in TOTAL_CLAIM_PATTERNS for m in re.findall(pat, text)]
        if not found:
            errors.append(
                f"{rel}: no template 'total count' phrasing found — the wording "
                f"likely changed; update TOTAL_CLAIM_PATTERNS in check_docs.py or "
                f"restore a 'NN files total'-style claim."
            )
            continue
        bad = [n for n in found if n != truth]
        if bad:
            errors.append(
                f"{rel}: states template total {bad} but templates/*.svg = {truth}."
            )
    return errors


# --- Check 2: layout enum ----------------------------------------------------
# CANONICAL is the checker's expected layout set. When you add/remove a layout,
# update this list AND every doc below; the check then flags any doc you forgot.
# (8 bento + 3 chart + 9 diagram primitives = 20.)
CANONICAL_LAYOUTS = [
    "single_focus", "stat_hero", "mini_grid", "two_col_50_50", "two_col_2_1",
    "three_col", "hero_top", "mixed_grid",
    "chart_bar", "chart_line", "chart_donut",
    "flow", "timeline", "cycle", "funnel", "compare_table",
    "quadrant_2x2", "venn", "hierarchy_tree", "pyramid",
]
LAYOUT_ENUM_FILES = ["SKILL.md", "prompts/04_planning_draft.md"]


def check_layout_enum() -> list[str]:
    errors: list[str] = []
    for rel in LAYOUT_ENUM_FILES:
        text = read(rel)
        missing = [t for t in CANONICAL_LAYOUTS if t not in text]
        if missing:
            errors.append(f"{rel}: layout enum missing {missing}.")
    return errors


# --- Check 3: bilingual README parity ----------------------------------------
def check_readme_parity() -> list[str]:
    zh = len(re.findall(r"(?m)^## ", read("README.md")))
    en = len(re.findall(r"(?m)^## ", read("README.en.md")))
    if zh != en:
        return [f"README.md has {zh} '## ' sections but README.en.md has {en} — "
                f"the two are translations of each other; keep them in sync."]
    return []


# --- Check 4: rubric back-references resolve ----------------------------------
# Guards the loop-engineering work: the rubric is the single gradeable source of
# truth, and the grading prompts point at it. If either rots, graders mis-map.
RUBRIC_CITING_FILES = [
    "SKILL.md",
    "prompts/00_source_analysis.md",
    "prompts/02_outline_architect.md",
    "prompts/04_planning_draft.md",
    "prompts/05_designer_svg.md",
    "prompts/06_visual_grader.md",
    "prompts/07_content_grader.md",
]


def check_rubric_backrefs() -> list[str]:
    errors: list[str] = []
    rubric_path = ROOT / "references" / "rubric.md"
    if not rubric_path.exists():
        return ["references/rubric.md is missing."]
    rubric = rubric_path.read_text(encoding="utf-8")
    for phase in range(6):  # P0..P5 each define at least an -01 criterion
        if f"P{phase}-01" not in rubric:
            errors.append(f"references/rubric.md: no P{phase}-01 criterion found.")
    for rel in RUBRIC_CITING_FILES:
        if "references/rubric.md" not in read(rel):
            errors.append(f"{rel}: expected a reference to references/rubric.md, none found.")
    return errors


# --- Check 5: variant / motion value enums -------------------------------------
# Same shape as the layout-enum check. card_variant (per layout), flow_variant,
# and motion each state their allowed values in 4 files; a value renamed or added
# in one place silently strands the others.
SPEC_FILES = [
    "SKILL.md",
    "prompts/04_planning_draft.md",
    "prompts/05_designer_svg.md",
    "references/design_system.md",
]
VARIANT_ENUMS = [
    ("card_variant three_col",
     ["icon_column", "numbered_steps", "axis_labeled", "lead_plus_pair"], SPEC_FILES),
    ("card_variant mini_grid",
     ["even_grid", "ribbon_row", "spotlight"], SPEC_FILES),
    ("card_variant two_col_50_50",
     ["balanced", "before_after"], SPEC_FILES),
    ("flow_variant",
     ["terrace_ascent", "river_ribbon", "cascade_fall", "dome_arcade"], SPEC_FILES),
    ("motion",
     ["transit_rail", "orbit", "hub", "accent_bypass"],
     ["SKILL.md", "prompts/04_planning_draft.md", "prompts/05_designer_svg.md", "CLAUDE.md"]),
]


def check_variant_enums() -> list[str]:
    errors: list[str] = []
    for name, values, files in VARIANT_ENUMS:
        for rel in files:
            text = read(rel)
            missing = [v for v in values if v not in text]
            if missing:
                errors.append(f"{rel}: {name} enum missing {missing}.")
    return errors


# --- Check 6: _base.svg icon count ---------------------------------------------
# Ground truth = number of <symbol> defs in templates/_base.svg. The docs' claim
# ("NN Lucide icons") was stale for a year before anyone noticed — same failure
# class as the template count, so guard it the same way.
ICON_COUNT_FILES = ["SKILL.md", "README.md", "README.en.md"]
ICON_CLAIM_PATTERNS = [
    r"(\d+)\s+Lucide icons?",    # SKILL.md, README.en.md
    r"(\d+)\s*個\s*Lucide icon",  # README.md (zh)
]


def check_icon_count() -> list[str]:
    errors: list[str] = []
    truth = len(re.findall(r"<symbol\b", read("templates/_base.svg")))
    for rel in ICON_COUNT_FILES:
        text = read(rel)
        found = [int(m) for pat in ICON_CLAIM_PATTERNS for m in re.findall(pat, text)]
        if not found:
            errors.append(
                f"{rel}: no 'NN Lucide icons' claim found — wording likely changed; "
                f"update ICON_CLAIM_PATTERNS in check_docs.py or restore the claim."
            )
            continue
        bad = [n for n in found if n != truth]
        if bad:
            errors.append(
                f"{rel}: states {bad} Lucide icons but templates/_base.svg has {truth} <symbol> defs."
            )
    return errors


# --- Check 7: grader-verdict paths ---------------------------------------------
# SKILL.md tells the graders to persist verdicts to _qa/grade_p{3,5}.json, and the
# Loop-4 trace tooling (improvement_loop.md, collect_trace.sh, the /deckforge-improve
# skill) reads them back by the same names. A rename in one place silently breaks
# the trace corpus.
QA_PATH_FILES = [
    "SKILL.md",
    "references/improvement_loop.md",
    "scripts/collect_trace.sh",
    ".claude/skills/deckforge-improve/SKILL.md",
]
QA_PATHS = ["_qa/grade_p3.json", "_qa/grade_p5.json"]


def check_qa_paths() -> list[str]:
    errors: list[str] = []
    for rel in QA_PATH_FILES:
        text = read(rel)
        missing = [p for p in QA_PATHS if p not in text]
        if missing:
            errors.append(f"{rel}: grader-verdict path(s) missing {missing}.")
    return errors


CHECKS = [
    ("template count", check_template_count),
    ("layout enum", check_layout_enum),
    ("README parity", check_readme_parity),
    ("rubric back-refs", check_rubric_backrefs),
    ("variant/motion enums", check_variant_enums),
    ("icon count", check_icon_count),
    ("grader-verdict paths", check_qa_paths),
]


def main() -> int:
    failed = False
    for name, fn in CHECKS:
        errors = fn()
        if errors:
            failed = True
            print(f"❌ {name}")
            for e in errors:
                print(f"   - {e}")
        else:
            print(f"✅ {name}")
    if failed:
        print("\nDoc-drift check FAILED. Fix the above before committing.")
        return 1
    print("\nAll doc-drift checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
