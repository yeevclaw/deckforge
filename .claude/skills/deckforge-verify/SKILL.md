---
name: deckforge-verify
description: Verify a DeckForge harness change before committing — classify the working-tree diff, run the matching verification ladder (doc-drift, SVG hard-invariant lint, render smoke, grader passes, phase-isolated evals against evals/ fixtures), iterate fixes up to 2 LLM grading rounds, and report a two-bit verdict (regression bar × intended direction). Use after editing templates, prompts, references, or the converter. Maintainer dev tool; requires a repo-root session.
---

# DeckForge change-time verification (dev-time Loop 2)

You verify a harness edit the same way the runtime verifies a deck: independent
graders against `references/rubric.md`, fix-and-regrade, a hard round cap, and
no silent shipping. The subject is the working-tree diff instead of a deck.
`references/improvement_loop.md` holds the surrounding picture (traces →
analysis → proposal → **this skill escorts the edit in** → ship → traces).

## Step 0 — Pre-register the direction (before running anything)

Write one literal block, first:

```
EXPECTED EFFECT: <observable thing> should <change how>, checkable by <rung / rubric_id>
```

or `EXPECTED EFFECT: none intended (refactor) — regression bar only`
or `EXPECTED EFFECT: not offline-observable — direction deferred to Loop-4 traces`.

This is written **before** any rung runs and repeated verbatim in the verdict.
A direction invented after seeing the results is not a direction.

## Step 1 — Classify the diff

`git status --short` + `git diff HEAD --name-only`, then map **by which phase's
rules the change touches** (SKILL.md spans all phases — classify its diff hunks,
not its filename). Union when multiple classes match.

| Change touches | Rungs (free → LLM) |
|---|---|
| anything | `python3 scripts/check_docs.py` |
| a script under `scripts/` | run the changed script itself green |
| `templates/` or any page SVG | `python3 scripts/check_svg.py <changed files>` → `bash scripts/render_smoke.sh <out> <changed files>` → **one visual-grade pass** over the PNGs (fresh 06 sub-agent; P5-01..P5-08, plus P5-11 on chart pages, skip P5-10 — no plan) |
| `scripts/svg_to_pptx.py` or `examples/` | `bash scripts/golden_check.sh`; **plus**, only if the change is to render/decompose logic AND the expected effect is pixel-visible: render 3 `examples/sample-deck` pages via render_smoke → one 06 pass |
| `prompts/04_planning_draft.md`, `references/pyramid_principle.md`, SKILL.md Phase-3 rules | **Phase-3 eval**: fresh sub-agent runs the planner per 04 on `evals/brief.md` → fresh 07 sub-agent grades the produced plan against `evals/brief.md` + rubric (P3-11/12/13) |
| `prompts/05_designer_svg.md`, design references (`design_system` / `bento_grid` / `diagrams` / `chart_anatomy`), template-family rules | **Phase-4 eval**: fresh sub-agent runs the designer per 05 on the **relevant subset** of `evals/planning.json` pages → render_smoke → fresh 06 pass. Subset map: flow/glass rules → flow page; chart_anatomy → chart_bar page; global card/typography rules → three_col + mini_grid; unmappable → three_col alone. **Never all 5 pages.** |
| `prompts/06` / `prompts/07` / `references/rubric.md` (the measuring instruments) | **Calibration rung**: run the changed grader once on a known-good input (06 → render_smoke over 3 `examples/sample-deck` pages; 07 → the `evals/` fixtures) and assert (a) known-good still passes, (b) the output JSON has the exact schema keys |
| `prompts/00–03` (Socratic / outline — no offline oracle) | check_docs + read-through; the report must state: **"direction deferred to Loop-4 traces"** — do not fake an eval |
| docs / READMEs only | check_docs |

## Step 2 — Run and iterate

Run the rungs free-first. LLM rungs run automatically — no per-round asking.
On failure: fix **the change under verify** (never the measuring set — see hard
rules), re-run only the failing rung.

**Caps**: ≤2 LLM grading rounds per verify; Phase-4 eval additionally ≤3
designer page-generations total. Cap hit with failures left → stop and report
the unresolved `rubric_id`s. Never loop past the cap; never hide a known defect.

## Step 3 — Two-bit verdict

```
REGRESSION: GREEN|RED — <each rung: name + result, one line each>
DIRECTION:  GREEN|RED|DEFERRED — <the step-0 block, verbatim> →
            <the quoted rung-output line(s) that confirm or refute it>
```

Both bits GREEN (or DIRECTION legitimately DEFERRED) = pass, proceed to commit.
Anything else = report honestly and stop for the maintainer.

## Hard rules

1. **The measuring set is read-only during a verify**: `evals/`,
   `references/rubric.md`, `prompts/06_visual_grader.md`,
   `prompts/07_content_grader.md`, `scripts/check_docs.py`,
   `scripts/check_svg.py`. Fixes go into the change under verify, never into
   the instruments. If you believe a fixture or rubric line is itself wrong:
   stop, report `verify blocked: fixture dispute`, and let the maintainer
   change it in a **separate commit** — fixture edits touch `evals/brief.md` +
   `evals/planning.json` only together and re-baseline with one 07 pass
   (must pass) before anything else is verified against them.
2. **Mechanical tooth**: the last action of every verify is
   `git diff HEAD --name-only` — if any measuring-set path is modified in the
   same working tree as the change under verify, the verdict is **RED**
   regardless of green rungs. (Editing the instruments *as the change itself*
   is legitimate — that's the calibration rung's case, where the instrument is
   the declared subject, not a bystander edit.)
3. **Independence**: planner / designer / grader runs are always **fresh
   sub-agents** — the session that made the change never grades its own output.
4. Grader I/O contracts: 06 needs the rendered PNGs (+ `evals/planning.json`
   only when P5-10 is in scope) + rubric; 07 needs the plan + `evals/brief.md`
   + rubric. Both return the strict JSON shapes defined in their prompt files.
