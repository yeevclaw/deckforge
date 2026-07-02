# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

DeckForge's goal is not merely to produce good-looking, easy-to-read slides. It is to use Socratic dialogue with the AI to excavate scattered information and reassemble it into complete, structured content that precisely conveys what each deck needs to say — and through that, shift the audience's judgment — delivered as a `.pptx` the user can keep editing.

In practice, DeckForge doesn't start by drawing slides. It first treats the AI as a presentation consultant, using Socratic dialogue to draw out each deck's logic and key points — this dialogue is the core, not a preliminary step; a wrong thesis costs more the later it's caught, so every phase boundary waits for the user's approval. Once the key points are settled, it builds the story along the Pyramid Principle, then picks the most fitting visual structure for each page's content — card grid, flow, cycle, comparison, and hierarchy each have their place — and reins it in with disciplined, restrained color and typography. The strength isn't drawing many kinds, but picking the right one and never letting form overpower the message; when warranted, it can also break free of fixed layouts and let the AI design freely for the best presentation of the content. Finally, each page is saved as SVG and assembled into a `.pptx` — SVG because it's the only format that affords both design control and native PowerPoint editing: in PowerPoint 2016+, Convert to Shape leaves the overall visuals and background as one movable-but-uneditable image, while the content objects — text, cards, charts, lines, icons — can be freely repositioned and resized; what ships is a deck you can actually change, not a screenshot you can't.

**Implementation:** DeckForge is a Claude skill (github.com/yeevclaw/deckforge) that produces editable PowerPoint decks via a 5-phase workflow. The "code" is mostly Markdown prompts and SVG templates; the only executable code is `scripts/svg_to_pptx.py`. There is no test suite, linter, or build system beyond `scripts/package.sh`.

**Directory layout note**: sessions are often started from the outer wrapper directory `/Users/jeff_mini/Documents/DeckForge/` — the repo is its `DeckForge/` subdirectory (where this file lives), and the `deckforge.zip` at the outer level is build output from `package.sh`. Run git/script commands from the repo root.

This CLAUDE.md is `export-ignore`d in `.gitattributes`, so it never ships in the skill zip — treat any new non-runtime file the same way.

## Commands

All run from the repo root:

```bash
# Install the converter's dependencies (only scripts/svg_to_pptx.py needs them)
pip install python-pptx resvg-py img2pdf --break-system-packages

# Convert a directory of SVG slides to .pptx (+ companion .pdf + .notes.md)
python scripts/svg_to_pptx.py --pages-dir pages/ --output deck.pptx

# Build the distributable skill zip → ../deckforge.zip
bash scripts/package.sh

# Visual QA of a produced deck (render back to images and inspect)
soffice --headless --convert-to pdf deck.pptx && pdftoppm -jpeg -r 100 deck.pdf slide

# Regression-render the three example decks through the converter (run before a release)
bash scripts/golden_check.sh
```

The QA step needs `soffice` (LibreOffice) and `pdftoppm` (poppler) — these are NOT covered by requirements.txt, which only lists the three Phase-5 pip packages. On macOS: `brew install --cask libreoffice` and `brew install poppler`.

`package.sh` ships from `git archive HEAD`, **not** the working tree — uncommitted changes are silently excluded (it warns). Commit before packaging.

## Release / ship flow

Versions are tagged `vX.Y.Z`; commit subjects follow `vX.Y.Z: short subject`. Use `git add <specific files>`, never `git add -A` (scratch review docs sit in the working tree).

1. Commit → `git tag vX.Y.Z HEAD`
2. `git push origin main && git push origin vX.Y.Z`
3. `bash scripts/package.sh`
4. `gh release create vX.Y.Z ../deckforge.zip --title "..." --notes "..."` — pushing a tag does **not** create a GitHub Release; the install instructions in README depend on the release asset existing.

## Architecture

The skill is a phase pipeline where each phase reads the previous phase's file artifact:

```
(analysis.md) → brief.md → outline.json → planning.json → pages/page_NN.svg → .pptx + .pdf + .notes.md
   Phase 0       Phase 1      Phase 2        Phase 3           Phase 4              Phase 5
```

**The harness.** In the LangChain "loop engineering" sense, the *harness* is everything wrapping the model — for DeckForge that's `SKILL.md` + `prompts/*` + `references/*` + `templates/*` + `scripts/svg_to_pptx.py`. Its gradeable quality bar is `references/rubric.md`, scored independently by two fresh-eyes graders — the Phase 3 content grade (`prompts/07_content_grader.md`) and the Phase 5 visual verification loop (`prompts/06_visual_grader.md`); its hill-climbing improvement procedure is `references/improvement_loop.md`. The per-file breakdown:

- **`SKILL.md`** — the skill entry point Claude Desktop/Code reads; defines the phase rules, the no-phase-skipping/file-checkpoint contract, handoff approvals, and the Phase 5 delivery checklist. Its frontmatter `name:` is read by `package.sh` to name the zip's wrapper folder.
- **`prompts/00–05_*.md`** — the per-phase master prompts. **File numbers ≠ phase numbers**: `03_content_research.md` is an optional "Phase 2.5" (writes `research.md` when the topic needs factual grounding), so `04_planning_draft.md` = Phase 3 and `05_designer_svg.md` = Phase 4. The `planning.json` schema and the layout enum live in `prompts/04_planning_draft.md`. `06_visual_grader.md` is **not** a phase prompt — it's the independent visual-QA grader sub-agent spawned in the Phase 5 verification loop (SKILL.md → "QA"). `07_content_grader.md` is its Phase 3 counterpart — the independent content-QA grader (ids P3-11/P3-12/P3-13) spawned before the Phase 3→4 handoff (SKILL.md → "Phase 3 content grade").
- **`references/`** — knowledge bases the prompts cite: `bento_grid.md` (8 base layouts, the default), `diagrams.md` (9 diagram primitives, used only when bento loses structural information), `chart_anatomy.md`, `design_system.md` (palettes/typography; **`corporate_fresh` is the default** style, `dark_apple` on request), `socratic_loop.md`, `pyramid_principle.md`, `editable_mode.md` (the two-layer editability model — what Convert-to-Shape can and can't edit; load-bearing for `svg_to_pptx.py`), `rubric.md` (the gradeable quality bar — stable-id criteria the Phase 5 grader and `scripts/check_docs.py` score against).
- **`templates/`** — 34 SVG starting templates + `_base.svg` (shared filters/gradients + the Lucide icon set referenced via `<use>`) = **35 files total**, all `viewBox="0 0 1280 720"`. Includes the `corporate_fresh` family (`fresh_*`), whose four `fresh_flow*` files are the glass-flow variants and whose `fresh_3col*` (4), `fresh_mini_grid*` (3), and `fresh_2col*` (2) files are the per-page `card_variant` families for `three_col` / `mini_grid` / `two_col_50_50`.
- **`scripts/svg_to_pptx.py`** — assembles a `pages/` dir of SVGs into the `.pptx` (+ a companion `.pdf` via img2pdf; speaker notes go to a sibling `.notes.md` and are stripped from the pptx because embedded `notesSlide` parts make Keynote reject the file). How each slide is embedded has two modes:
  - **Default — two-layer decomposition** (v0.10.0): a rasterized PNG *background image* carries the atmosphere PowerPoint can't vectorize (gradients, glass, shadows/filters), and a transparent *content layer* embeds a **stripped** SVG (atmosphere removed, card-shadow filters dropped, `<use>`/`<symbol>` icons inlined) via the PowerPoint 2016+ `svgBlip` extension. Convert-to-Shape on the content layer makes text/cards/lines/icons individually editable; the background stays a movable-but-uneditable picture. `--no-decompose` reverts to the old single-picture model (full render + `svgBlip`). What is / isn't vector-editable: `references/editable_mode.md`.
  - **Motion pages — animated GIF** (v0.9.0 flow-anim pipeline): a page whose SVG marks dashed edges with `class="flow-anim"` + `stroke-dasharray` is embedded as a looping GIF (dashes flow in slideshow mode) instead of the two-layer split, so that slide is **not** Convert-to-Shape editable. `--no-anim` disables it; motion types (`transit_rail`/`orbit`/`hub`/`accent_bypass`) come from the planner, recipes in `prompts/05_designer_svg.md` Step 5.7.
- **`.gitattributes`** — `export-ignore` entries control what ships in the zip. Runtime assets (SKILL.md, prompts/, references/, templates/, svg_to_pptx.py, setup scripts) ship; READMEs, examples/, package.sh, CLAUDE.md don't. New non-runtime files should be export-ignored.

## Editing rules specific to this repo

- **Doc drift is the recurring bug class here.** Rules are intentionally stated in multiple places (e.g. the layout enum appears in SKILL.md, `prompts/04_planning_draft.md`, and the references; design constraints appear in SKILL.md and `prompts/05_designer_svg.md`). Several past releases exist solely to fix drift. When changing a rule, grep for every other file that states it and update them together. The **template count** (currently 35 files incl. `_base.svg`) is one such drift point — it appears in SKILL.md, both READMEs, and the `templates/` bullet above; reconcile with `ls templates/*.svg | wc -l` when adding or removing templates. `scripts/check_docs.py` now asserts the mechanical ones (template count, layout enum, README parity, rubric back-refs, variant/motion enums, icon count) — run it before committing.
- The two README files (`README.md` Chinese, `README.en.md` English) are translations of each other — change both.
- Core invariants the content enforces (don't weaken them when editing prompts/templates): 1280×720 viewBox; single highlight color per deck, never a second accent; every text run in a real `<text>` element (keeps Convert-to-Shape editability); no accent underline below page titles; no emoji as icons; bento-first, diagram primitives only on information loss.
- The two Chinese-named `DeckForge_*.md` files in the working tree are gitignored reviewer/scratch docs — leave them alone.
