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

import json
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
# (8 bento + 10 chart + 9 diagram primitives = 27.)
CANONICAL_LAYOUTS = [
    "single_focus", "stat_hero", "mini_grid", "two_col_50_50", "two_col_2_1",
    "three_col", "hero_top", "mixed_grid",
    "chart_bar", "chart_line", "chart_donut",
    "chart_hbar", "chart_stacked_bar", "chart_waterfall", "chart_combo", "chart_mekko",
    "chart_radar", "chart_gantt",
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


# --- Check 8: evals fixtures stay valid ------------------------------------------
# evals/brief.md + evals/planning.json are the frozen golden inputs for the
# change-time verification loop (.claude/skills/deckforge-verify). Planning-schema
# churn (prompts/04) must break them loudly here, not rot them silently. Asserts
# only the fields the graders/converter actually read; the full schema lives in
# prompts/04_planning_draft.md.
CHART_LAYOUTS = {
    "chart_bar", "chart_line", "chart_donut",
    "chart_hbar", "chart_stacked_bar", "chart_waterfall", "chart_combo", "chart_mekko",
    "chart_radar", "chart_gantt",
}
PRIMITIVE_LAYOUTS = {
    "flow", "timeline", "cycle", "funnel", "compare_table",
    "quadrant_2x2", "venn", "hierarchy_tree", "pyramid",
}
BRIEF_SECTIONS = ["## Core thesis", "## Proof pillars", "## Belief shift"]


def _enum_values(name: str) -> list[str]:
    return next(values for n, values, _ in VARIANT_ENUMS if n == name)


def check_evals_fixtures() -> list[str]:
    errors: list[str] = []
    try:
        plan = json.loads(read("evals/planning.json"))
    except FileNotFoundError:
        return ["evals/planning.json is missing."]
    except json.JSONDecodeError as e:
        return [f"evals/planning.json: invalid JSON ({e})."]

    meta = plan.get("meta", {})
    missing = [k for k in ("topic", "page_count", "language") if k not in meta]
    if missing:
        errors.append(f"evals/planning.json: meta missing {missing}.")
    pages = plan.get("pages", [])
    if meta.get("page_count") != len(pages):
        errors.append(
            f"evals/planning.json: meta.page_count={meta.get('page_count')} "
            f"but pages has {len(pages)} entries."
        )

    db = plan.get("design_brief", {})
    missing = [k for k in ("palette_hint", "highlight_color", "motif_hint",
                           "typography_hint", "flow_variant") if k not in db]
    if missing:
        errors.append(f"evals/planning.json: design_brief missing {missing}.")
    if db.get("flow_variant") and db["flow_variant"] not in _enum_values("flow_variant"):
        errors.append(f"evals/planning.json: flow_variant '{db['flow_variant']}' not in enum.")

    for page in pages:
        pid = page.get("page_id", "?")
        missing = [k for k in ("page_id", "page_type", "layout", "title", "speaker_notes")
                   if k not in page]
        if missing:
            errors.append(f"evals/planning.json page {pid}: missing {missing}.")
        layout = page.get("layout")
        if layout not in CANONICAL_LAYOUTS:
            errors.append(f"evals/planning.json page {pid}: layout '{layout}' not in CANONICAL_LAYOUTS.")
        elif layout in CHART_LAYOUTS:
            if "chart_data" not in page:
                errors.append(f"evals/planning.json page {pid}: chart layout without chart_data.")
        elif layout in PRIMITIVE_LAYOUTS:
            if f"{layout}_data" not in page:
                errors.append(f"evals/planning.json page {pid}: primitive layout without {layout}_data.")
        elif not isinstance(page.get("cards"), list):
            errors.append(f"evals/planning.json page {pid}: card layout without cards[].")
        cv = page.get("card_variant")
        if cv:
            try:
                allowed = _enum_values(f"card_variant {layout}")
            except StopIteration:
                errors.append(
                    f"evals/planning.json page {pid}: card_variant set but layout "
                    f"'{layout}' has no card_variant enum."
                )
            else:
                if cv not in allowed:
                    errors.append(
                        f"evals/planning.json page {pid}: card_variant '{cv}' "
                        f"not in the {layout} enum."
                    )

    try:
        brief = read("evals/brief.md")
    except FileNotFoundError:
        errors.append("evals/brief.md is missing.")
        return errors
    for sec in BRIEF_SECTIONS:
        if sec not in brief:
            errors.append(f"evals/brief.md: section '{sec}' missing.")
    if "## Proof pillars" in brief:
        section = brief.split("## Proof pillars", 1)[1].split("##", 1)[0]
        pillars = re.findall(r"(?m)^\d+\.", section)
        if len(pillars) != 3:
            errors.append(f"evals/brief.md: expected exactly 3 proof pillars, found {len(pillars)}.")
    return errors


# --- Check 9: demo page count --------------------------------------------------
# Ground truth = number of page_*.svg in examples/sample-deck/ (the demo's source
# pages). The docs described it as "3 pages" long after it grew to 10 — same
# stale-number failure class as the template/icon counts, so guard it the same way.
DEMO_COUNT_PATTERNS = {
    "SKILL.md": [r"rendered demo \((\d+) pages\)"],
    "README.md": [r"(\d+)\s*頁完整產出", r"(\d+)\s*頁範例"],
    "README.en.md": [r"\((\d+) pages, full output\)", r"(\d+)-page example"],
}


def check_demo_page_count() -> list[str]:
    errors: list[str] = []
    truth = len(list((ROOT / "examples" / "sample-deck").glob("page_*.svg")))
    for rel, patterns in DEMO_COUNT_PATTERNS.items():
        text = read(rel)
        found = [int(m) for pat in patterns for m in re.findall(pat, text)]
        if not found:
            errors.append(
                f"{rel}: no demo page-count phrasing found — the wording likely "
                f"changed; update DEMO_COUNT_PATTERNS in check_docs.py."
            )
            continue
        bad = [n for n in found if n != truth]
        if bad:
            errors.append(
                f"{rel}: states demo page count {bad} but examples/sample-deck/ "
                f"has {truth} page_*.svg."
            )
    return errors


# --- Check 10: markdown table column integrity ---------------------------------
# A GFM table row with the wrong cell count silently corrupts which column a value
# lands in — exactly the crisis-comms row bug (a 4-cell row under a 3-col header
# mis-fed the coverage sweep). Assert every body row matches its header's width.
TABLE_GUARD_FILES = [
    "SKILL.md",
    "prompts/01_needs_research.md",
    "prompts/04_planning_draft.md",
    "prompts/05_designer_svg.md",
    "references/chart_anatomy.md",
    "references/design_system.md",
    "references/rubric.md",
]
_SEP_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")


def _cell_count(line: str) -> int:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    # Split on unescaped pipes only (GFM requires literal cell pipes as \|).
    return len(re.split(r"(?<!\\)\|", s))


def check_table_columns() -> list[str]:
    errors: list[str] = []
    for rel in TABLE_GUARD_FILES:
        lines = read(rel).splitlines()
        in_fence = False
        i = 0
        while i < len(lines):
            stripped = lines[i].lstrip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = not in_fence
                i += 1
                continue
            # A table = a header line immediately followed by a separator line.
            if (not in_fence and i + 1 < len(lines)
                    and "|" in lines[i] and _SEP_RE.match(lines[i + 1])):
                width = _cell_count(lines[i])
                header_lineno = i + 1
                j = i + 2
                while j < len(lines) and "|" in lines[j] and lines[j].strip():
                    if lines[j].lstrip().startswith(("```", "~~~")):
                        break
                    got = _cell_count(lines[j])
                    if got != width:
                        errors.append(
                            f"{rel}:{j + 1}: table row has {got} cells but its "
                            f"header (line {header_lineno}) has {width}."
                        )
                    j += 1
                i = j
                continue
            i += 1
    return errors


# --- Check 11: CLI flag parity -------------------------------------------------
# Every converter flag SKILL documents must exist in svg_to_pptx.py's argparse —
# so a renamed/removed flag can't leave the docs pointing at a flag that no longer
# works (--no-decompose was real-but-undocumented; this guards the reverse rot).
# Direction is docs ⊆ code, not one-to-one: SKILL curates a useful subset, so we
# do NOT force every argparse flag into the docs. Non-converter flags that appear
# in SKILL (pip / soffice) are excluded.
NON_CONVERTER_FLAGS = {"--break-system-packages", "--convert-to", "--headless"}


def check_cli_flag_parity() -> list[str]:
    converter = read("scripts/svg_to_pptx.py")
    real = set(re.findall(r'add_argument\("(--[a-z][a-z-]+)"', converter))
    if not real:
        return ["scripts/svg_to_pptx.py: no argparse long flags found — "
                "the add_argument phrasing likely changed; update check_docs.py."]
    documented = set(re.findall(r"(--[a-z][a-z-]+)", read("SKILL.md")))
    stale = sorted(documented - real - NON_CONVERTER_FLAGS)
    if stale:
        return [f"SKILL.md documents converter flag(s) {stale} that svg_to_pptx.py "
                f"argparse does not define (renamed or removed?)."]
    return []


CHECKS = [
    ("template count", check_template_count),
    ("layout enum", check_layout_enum),
    ("README parity", check_readme_parity),
    ("rubric back-refs", check_rubric_backrefs),
    ("variant/motion enums", check_variant_enums),
    ("icon count", check_icon_count),
    ("grader-verdict paths", check_qa_paths),
    ("evals fixtures", check_evals_fixtures),
    ("demo page count", check_demo_page_count),
    ("table columns", check_table_columns),
    ("CLI flag parity", check_cli_flag_parity),
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
