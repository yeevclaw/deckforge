# DeckForge Rubric — the gradeable quality bar

This is the **single source of truth** for "is this phase's output good enough". Each
phase prompt still carries its own inline checklist (kept there because Claude only
reads that one prompt while executing the phase); **this file is the gradeable,
stably-numbered mirror** that an independent grader or a script can score against
without re-reading six prompts.

Every criterion has a **stable id** (`P<phase>-<nn>`). Ids never get renumbered —
graders, `prompts/06_visual_grader.md`, and `scripts/check_docs.py` reference them by
id, so reusing a retired number would silently mis-map. Add new criteria with the
next free number; never recycle.

## How to use it — two modes

- **Self-check (every phase, before emitting).** The same context that produced the
  artifact runs its inline checklist. Fast, but weak: a context rationalizes its own
  output. This is the floor, not the ceiling.
- **Independent grade (Phase 5 visual + Phase 3 content).** A *fresh* sub-agent that
  did **not** produce the artifact scores it against the relevant section here and
  returns pass/fail + a fix per failure. Independent grading is what closes the
  verification loop — see `prompts/06_visual_grader.md` (Phase 5, the rendered slides)
  and `prompts/07_content_grader.md` (Phase 3, the content plan: ids P3-11/P3-12/P3-13),
  wired in SKILL.md "QA" and "Phase 3 content grade".

The **Checker** column says who can decide each criterion:
- `self` — judgement call, run during the phase's own self-check.
- `grader` — an independent sub-agent looking at the rendered slide images.
- `machine` — mechanically decidable (regex / count / parse); `scripts/check_docs.py`
  or a simple SVG scan can assert it without a model.

---

## Phase 0 — `analysis.md`

Mirrors `prompts/00_source_analysis.md` → "Quality checklist".

| id | Criterion | How to check | Checker |
|---|---|---|---|
| P0-01 | ≥6 specific metrics, each with CN **and** EN caption | count `<value> · <CN> · <EN>` lines | self |
| P0-02 | Named entities (products, people, regions, dates) quoted verbatim, not paraphrased | spot-check against source | self |
| P0-03 | ≥2 parallel sets, each 3+ comparable items | count labelled sets | self |
| P0-04 | ≥1 anomaly / surprising finding flagged | present in "Anomalies" section | self |
| P0-05 | Numbers quoted exactly, never rounded or paraphrased | compare to source | self |
| P0-06 | Source tone recorded | "Source tone" line present | self |

## Phase 1 — `brief.md`

Phase 1's checks are interwoven with the Socratic loop's control flow (between-round
reflection, coverage sweep, MECE revision, Forced Assumption mode). **The authoritative
definition lives in `prompts/01_needs_research.md`** — this table is the stop-condition
mirror, not a replacement. Do not grade Phase 1 from this file alone.

| id | Criterion | How to check | Checker |
|---|---|---|---|
| P1-01 | Audience named + current belief + room/context | `audience.*` fields filled | self |
| P1-02 | Belief shift articulated `from → to` | `belief_shift.from/to` filled | self |
| P1-03 | Core thesis fits one sentence | single-sentence `core_thesis` | self |
| P1-04 | 2–4 proof pillars, each with a concrete evidence anchor or `needs-research` tag | each pillar has anchor/tag | self |
| P1-05 | Most likely objection identified | `likely_objections[]` non-empty | self |
| P1-06 | Desired audience action named | `desired_action` filled | self |
| P1-07 | Page count, tone, language, brand sketched | `constraints` filled | self |
| P1-08 | The four non-negotiables are **user-confirmed**, not merely `[inferred]`: `audience.current_belief`, `belief_shift`, `core_thesis`, `desired_action` | no `[inferred]` left on these four | self |
| P1-09 | `proof_pillars` are MECE (no overlap, collectively defend the thesis) | run the MECE check in `01_needs_research.md` | self |

## Phase 2 — `outline.json`

Mirrors `prompts/02_outline_architect.md` → "Quality checklist".

| id | Criterion | How to check | Checker |
|---|---|---|---|
| P2-01 | Every page title is a **claim**, not a topic label | read each title | self |
| P2-02 | Same-level items are MECE | inspect each level | self |
| P2-03 | `part_titles` map to `brief.md` `proof_pillars` (usually 1:1) | compare to brief | self |
| P2-04 | Title-only read forms a coherent argument | read all titles in order | self |
| P2-05 | Page count == `meta.target_pages` | count vs target | machine |
| P2-06 | TOC consistent with part titles | compare TOC ↔ parts | machine |
| P2-07 | Grounded in research, no invented facts | check claims vs `research.md`/source | self |
| P2-08 | Each part has 2–6 pages | count pages per part | machine |
| P2-09 | Strict JSON: no comments, no trailing commas | parse it | machine |

## Phase 3 — `planning.json`

Mirrors `prompts/04_planning_draft.md` → "Quality checklist" + "Title-only read QA".
**P3-11 / P3-12 / P3-13 are independently graded** at the Phase 3→4 handoff by
`prompts/07_content_grader.md` (the content analogue of the Phase 5 visual grader); the
rest stay self-checks.

| id | Criterion | How to check | Checker |
|---|---|---|---|
| P3-01 | Each card holds exactly one core point | read each card | self |
| P3-02 | Multi-point cards split into mini-cards | inspect cards | self |
| P3-03 | `is_number_first` set correctly on every card | inspect cards | self |
| P3-04 | Number-first `stat_value` is a concrete number (not "many"/"several") | inspect values | self |
| P3-05 | Data-dense pages use `stat_hero` / `mini_grid` (independent numbers) or the matching `chart_*` layout (related numbers) | inspect layouts | self |
| P3-06 | Layout follows content shape, never switched to a primitive for visual variety | inspect layout choices | self |
| P3-07 | Real speaker notes, not "TBD" | inspect `speaker_notes` | self |
| P3-08 | `design_brief` palette consistent with `brief.md` tone | compare to brief | self |
| P3-09 | `design_brief.highlight_color` is ONE concrete hex | parse field | machine |
| P3-10 | Zero placeholders ("Lorem", "xxxx", "TBD", "Insert here") | regex scan | machine |
| P3-11 | Content authenticity: no AI filler (賦能/無縫/顛覆 · seamless/elevate/leverage), source precision kept, no exclamation marks in claims | regex + read | self + grader |
| P3-12 | Pyramid alignment: every card materially defends its page `title` claim (on-topic ≠ load-bearing) | per-page card test | self + grader |
| P3-13 | Title-only read forms a coherent argument (re-run at Phase 3→4 handoff) | read titles in order | self + grader |
| P3-14 | Bento-first: every primitive-layout page names its information-loss signal | inspect each primitive page | self |
| P3-15 | Primitive-layout share of content pages ≤ ~40% | count primitive vs total | machine |
| P3-16 | `flow_variant` set (corporate_fresh static flow) with a one-sentence story-shape reason | inspect `design_brief.flow_variant` | self |
| P3-17 | `card_variant` set per corporate_fresh card-variant page (`three_col` / `mini_grid` / `two_col_50_50`) with a one-sentence content-substructure reason; a same-structure parallel series assigns variants by each page's substructure, never for variety | inspect `card_variant` choices | self |
| P3-18 | Chart trigger (the relationship test): related numbers (trend / mix shift / A→B bridge / ranking / volume+rate / 2-D share) are planned as the matching `chart_*` layout, never scattered into cards; each chart clears its minimum shape; a quantitative page-title claim is carried by `chart_data.annotations[]` (≤2, labels pre-computed) | inspect data-bearing pages vs `prompts/04_planning_draft.md` → "The chart trigger" | self |

## Phase 4 — `pages/page_NN.svg`

Mirrors `prompts/05_designer_svg.md` → "Quality checklist". Several are mechanically
decidable from the SVG source — a grader or a small scan can assert them directly.

| id | Criterion | How to check | Checker |
|---|---|---|---|
| P4-01 | Root is `<svg viewBox="0 0 1280 720" …>`, nothing drawn outside it | regex on root | machine |
| P4-02 | Cards ≥20px gap (mini ≥24px), outer margin ≥48px | geometry scan | self |
| P4-03 | No accent underline beneath the page title (#1 AI-deck tell) | inspect title area | self |
| P4-04 | Palette matches the global `design_brief` | compare colors | self |
| P4-05 | Motif applied consistently within the page | inspect motif | self |
| P4-06 | No external network requests (no remote `href`, no remote font, no `http`/`xlink:href`) | regex scan | machine |
| P4-07 | Text contrast ≥ 4.5:1 (WCAG AA) | contrast calc | self |
| P4-08 | At least one visual element (icon / chart-shape / motif) besides text | inspect | self |
| P4-09 | No leftover placeholders (Lorem, xxx, TBD) | regex scan | machine |
| P4-10 | Every text run lives in a real `<text>` element (not path-converted) | scan for `<text>`, no text-as-path | machine |
| P4-11 | Motion page only: `flow-anim` on open `<line>`/`<path>` only, one `stroke-dasharray`, ≤3 animated paths (or one closed system) | `svg_to_pptx.py` flow-anim lint | machine |
| P4-12 | Single highlight-color discipline (dark_apple: only highlight for emphasis; corporate_fresh: role-locked green/blue/orange) | color-role scan | self |

## Phase 5 — VISUAL (the rendered slide)

**New in the loop-engineering work.** SKILL.md's old "QA — DO NOT SKIP" was prose; this
is its gradeable form. The grader sub-agent (`prompts/06_visual_grader.md`) reads each
rendered `_renders/page_NN.png` and scores against this section. These are defects you
can only see *after* rasterization — they are invisible in the SVG source.

| id | Criterion | How to check | Checker |
|---|---|---|---|
| P5-01 | No text overflow / clipping (SVG never auto-wraps; a missing `<tspan>` row clips the sentence) | look at each rendered slide | grader |
| P5-02 | No card overlap or near-touching gaps | look at each slide | grader |
| P5-03 | No low-contrast text against its background | look at each slide | grader |
| P5-04 | Palette consistent across all slides (one highlight, one motif deck-wide) | scan the deck's images | grader |
| P5-05 | No accent underline beneath any page title (visual re-confirm of P4-03) | look at each slide | grader |
| P5-06 | No emoji used as a functional icon | look at each slide | grader |
| P5-07 | Chart / diagram labels are readable and not clipped | look at chart slides | grader |
| P5-08 | Each slide has visible hierarchy (hero number / icon / motif) — not a text wall | look at each slide | grader |
| P5-09 | Speaker notes present where `planning.json` intended (not visual — confirmed against metadata at delivery, not by the image grader) | compare `.notes.md` to planning | self |
| P5-10 | No bottom takeaway line that restates the page title (a closing sentence paraphrasing the assertion title is the title said twice; most pages should have no bottom line) | look at each slide, compare to the title | grader |
| P5-11 | Chart pages: the chart visually asserts the page title's quantitative claim — at least one analytical element (reference line / difference bracket / CAGR arrow / emphasized bar, segment, or series) marks the claim on the chart; a bare data dump under an assertion title fails. Ink-voice discipline: annotation strokes in neutral ink, ≤2 annotations, decreases gray never red | look at chart slides, compare to the rendered title | grader |

---

## Stop rule for the Phase 5 verification loop

The grader returns `{deck_pass, slides:[{n, pass, failures:[{rubric_id, where, fix}]}]}`.
Re-render only the failing pages (back to Phase 4 with the `fix` notes), re-run the
converter for those, re-grade. Stop when `deck_pass` is true **or after 2 iterations** —
whichever comes first. If the cap is hit with failures remaining, **do not silently
ship**: list the unresolved `rubric_id`s to the user in the delivery message. Verification
costs latency + tokens; the cap bounds it. Apply it here because Phase 5 is the visible
deliverable where quality outweighs speed.

The Phase 3 content loop (`prompts/07_content_grader.md`, ids P3-11/P3-12/P3-13) uses the
same shape — `plan_pass` + per-page `failures` + a deck-level `title_read` — and the same
≤2-round cap, run before the Phase 3→4 handoff instead of before delivery.
