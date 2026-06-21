# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

DeckForge is a **Claude skill** (github.com/yeevclaw/deckforge) that produces editable PowerPoint decks via a 5-phase workflow. The "code" is mostly Markdown prompts and SVG templates; the only executable code is `scripts/svg_to_pptx.py`. There is no test suite, linter, or build system beyond `scripts/package.sh`.

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

- **`SKILL.md`** — the skill entry point Claude Desktop/Code reads; defines the phase rules, the no-phase-skipping/file-checkpoint contract, handoff approvals, and the Phase 5 delivery checklist. Its frontmatter `name:` is read by `package.sh` to name the zip's wrapper folder.
- **`prompts/00–05_*.md`** — the per-phase master prompts. **File numbers ≠ phase numbers**: `03_content_research.md` is an optional "Phase 2.5" (writes `research.md` when the topic needs factual grounding), so `04_planning_draft.md` = Phase 3 and `05_designer_svg.md` = Phase 4. The `planning.json` schema and the layout enum live in `prompts/04_planning_draft.md`.
- **`references/`** — knowledge bases the prompts cite: `bento_grid.md` (8 base layouts, the default), `diagrams.md` (9 diagram primitives, used only when bento loses structural information), `chart_anatomy.md`, `design_system.md` (palettes/typography; **`corporate_fresh` is the default** style, `dark_apple` on request), `socratic_loop.md`, `pyramid_principle.md`, `editable_mode.md`.
- **`templates/`** — 26 SVG starting templates + `_base.svg` (shared filters/gradients + the Lucide icon set referenced via `<use>`) = **27 files total**, all `viewBox="0 0 1280 720"`. Includes the `corporate_fresh` family (`fresh_*`), whose four `fresh_flow*` files are the glass-flow variants.
- **`scripts/svg_to_pptx.py`** — embeds each SVG twice per slide: a rasterized PNG fallback (via resvg-py, for Keynote/Preview/old PowerPoint) plus the original SVG via the PowerPoint 2016+ `svgBlip` OOXML extension (for Convert-to-Shape editability). Speaker notes are written to a sibling `.notes.md` and stripped from the pptx — embedded `notesSlide` parts make Keynote reject the file. A companion `.pdf` is assembled via img2pdf.
- **`.gitattributes`** — `export-ignore` entries control what ships in the zip. Runtime assets (SKILL.md, prompts/, references/, templates/, svg_to_pptx.py, setup scripts) ship; READMEs, examples/, package.sh, CLAUDE.md don't. New non-runtime files should be export-ignored.

## Editing rules specific to this repo

- **Doc drift is the recurring bug class here.** Rules are intentionally stated in multiple places (e.g. the layout enum appears in SKILL.md, `prompts/04_planning_draft.md`, and the references; design constraints appear in SKILL.md and `prompts/05_designer_svg.md`). Several past releases exist solely to fix drift. When changing a rule, grep for every other file that states it and update them together. The **template count** (currently 27 files incl. `_base.svg`) is one such drift point — it appears in SKILL.md, both READMEs, and the `templates/` bullet above; reconcile with `ls templates/*.svg | wc -l` when adding or removing templates.
- The two README files (`README.md` Chinese, `README.en.md` English) are translations of each other — change both.
- Core invariants the content enforces (don't weaken them when editing prompts/templates): 1280×720 viewBox; single highlight color per deck, never a second accent; every text run in a real `<text>` element (keeps Convert-to-Shape editability); no accent underline below page titles; no emoji as icons; bento-first, diagram primitives only on information loss.
- The two Chinese-named `DeckForge_*.md` files in the working tree are gitignored reviewer/scratch docs — leave them alone.
