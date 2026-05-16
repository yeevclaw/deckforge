# DeckForge

**English** · [繁體中文](README.md)

> A Claude skill that produces **professional, editable PowerPoint decks** by following a 5-phase expert workflow (research → outline → planning → design → produce), rather than stuffing your topic into a generic template.

Inspired by the methodology shared by *sandun* on linux.do ("应该是目前最强的PPT Agent，附上完整思路分享"). Output format is **SVG** — the key choice that essay makes — because PowerPoint 2016+ recognizes SVG as native vector graphics, and any user can right-click → *Convert to Shape* to edit every text run and shape.

## Demo

A 3-page **DeckForge self-intro** mini-deck, produced directly through this skill's SVG pipeline:

| | | |
|---|---|---|
| ![](examples/slide-1.jpg) | ![](examples/slide-2.jpg) | ![](examples/slide-3.jpg) |

- Combined PDF: [`examples/DeckForge-demo.pdf`](examples/DeckForge-demo.pdf)
- Source SVGs (peek at the Bento Grid coordinates): [`examples/sample-deck/`](examples/sample-deck/)

## What's inside

```
DeckForge/
├── SKILL.md                ← skill entry — Claude reads this first
├── prompts/                ← 5 reusable expert prompts (one per phase)
│   ├── 01_needs_research.md
│   ├── 02_outline_architect.md
│   ├── 03_content_research.md
│   ├── 04_planning_draft.md
│   └── 05_designer_svg.md
├── references/             ← detailed knowledge bases
│   ├── bento_grid.md       ← Bento Grid layout system (the secret sauce)
│   ├── design_system.md    ← 10 palettes + motifs + typography
│   ├── pyramid_principle.md
│   └── editable_mode.md    ← how Convert-to-Shape editing works
├── templates/              ← 7 SVG starting points (viewBox 0 0 1280 720)
│   ├── _base.svg           ← shared filters / gradients / Lucide icons
│   ├── cover.svg
│   ├── toc.svg
│   ├── bento_2col.svg
│   ├── bento_3col.svg
│   ├── bento_hero.svg
│   └── bento_mixed.svg
├── scripts/
│   ├── svg_to_pptx.py      ← SVG → PPTX (embeds svgBlip ext, vectors preserved)
│   ├── package.sh          ← build deckforge.zip for Claude Desktop upload
│   ├── setup.sh            ← one-line dependency installer (mac / linux)
│   └── setup.ps1           ← same, for Windows PowerShell
└── examples/               ← DeckForge self-intro mini-deck (3 pages)
    ├── DeckForge-demo.pdf  ← combined rendered PDF
    ├── slide-1.jpg ... 3   ← preview thumbnails
    └── sample-deck/        ← source SVG pages (drag into PowerPoint to inspect)
```

## Install (Claude Desktop)

Two steps:

### 1. Download the zip + install two Python packages

```bash
# Download the latest release zip
curl -L -o ~/Downloads/deckforge.zip \
  https://github.com/yeevclaw/deckforge/releases/latest/download/deckforge.zip

# Install the two Phase 5 dependencies (same line on macOS / Linux / Windows)
pip install python-pptx resvg-py --break-system-packages
```

> Don't use a terminal? Visit the [releases page](https://github.com/yeevclaw/deckforge/releases/latest), download `deckforge.zip` directly, and run only the `pip install` line in a terminal.

Just those two packages — **zero system dependencies**. `resvg-py` bundles a Rust SVG renderer as a pip wheel; no Homebrew, no apt-get, no sudo needed.

Phases 1–4 (research / outline / planning / design) are pure Markdown and need no packages. Only Phase 5 (assembling the `.pptx`) uses the two packages above.

### 2. Import the zip in Claude Desktop

1. Open Claude Desktop → **Customize** (top-right).
2. Left nav **Skills** → click **`+`** → **Create skill** → **Upload a skill**.
3. Pick `~/Downloads/deckforge.zip`.
4. `deckforge` appears under *Personal skills*.

Done. Just ask Claude:

> *Build me a deck about XYZ*
> *幫我做一份簡報，主題是 XYZ*

> **Updating to a new version**: download the new zip from the releases page, delete the old `deckforge` in Customize → Skills, and Upload a skill again.

## The 5 phases (overview)

| Phase | Output |
|---|---|
| 1 — Needs research | `brief.md` (audience, goal, length, tone) |
| 2 — Outline architecture | `outline.json` (pyramid principle, page titles as claims) |
| 3 — **Planning draft** | `planning.json` (actual content + layout intent per page) ← *the step most AI tools skip* |
| 4 — Design | `pages/page_NN.svg` (one vector page per slide) |
| 5 — Produce | `presentation.pptx` (with SVG embeds — fully editable in PowerPoint 2016+) |

The skill is **NOT** a one-shot generator. It deliberately includes review checkpoints (after outline, after planning) so you can fix things cheaply before any design effort is spent.

## Why SVG → PPTX (not template-based, not raster)?

- SVG is natively supported by PowerPoint 2016+. Right-click any slide → *Convert to Shape* and the SVG decomposes into editable text boxes and shapes — **every text run, every color, every icon is editable**.
- Layouts can be designed around the *content*, not crammed into a fixed template.
- Per-deck palette + motif consistency (the skill enforces this).
- See [`references/editable_mode.md`](references/editable_mode.md) for the editing details.

## Dependencies

**Phases 1–4 are pure Markdown — no install at all.** Only Phase 5 (producing the `.pptx`) needs a Python package:

```bash
# One line. python-pptx pulls in lxml + Pillow automatically.
pip install python-pptx --break-system-packages

# Or use the bundled setup script:
bash scripts/setup.sh                   # macOS / Linux
.\scripts\setup.ps1                     # Windows (PowerShell)
```

**Optional** — only if you need a high-DPI PNG fallback (for pre-2016 Office or PDF preview tools):

```bash
pip install cairosvg --break-system-packages
# or: brew install inkscape         (macOS)
# or: apt-get install librsvg2-bin  (Linux)

# Usage
python scripts/svg_to_pptx.py --pages-dir pages/ --output deck.pptx --with-raster
```

Without `--with-raster`, the script embeds a 1×1 transparent placeholder PNG as the OOXML-required fallback and lets PowerPoint 2016+ render the SVG vector directly — which is the right path for 90% of use cases.

## Credits

- Methodology: *sandun* @ linux.do — original article ("应该是目前最强的PPT Agent，附上完整思路分享")
- SVG as the deliverable format: also from that article — the choice preserves editability inside PowerPoint.
- The "顶级的PPT结构架构师" and "便當網格" prompts in `prompts/02_outline_architect.md` and `references/bento_grid.md` are direct adaptations of his prompts, with extensions.
- Bento Grid design language: popularized by Apple product pages.
- Pyramid Principle: Barbara Minto.

## For developers / forks

If you want to modify the skill, contribute upstream, or use Claude Code CLI:

```bash
# Clone the full source
git clone https://github.com/yeevclaw/deckforge.git ~/deckforge
cd ~/deckforge

# After editing, repackage into a zip for Claude Desktop
bash scripts/package.sh
# Produces ~/deckforge.zip — import it in Customize → Skills.

# Or: use Claude Code CLI
git clone https://github.com/yeevclaw/deckforge.git ~/.claude/skills/deckforge
bash ~/.claude/skills/deckforge/scripts/setup.sh
```

`scripts/package.sh` reads `name:` from SKILL.md so the zip's wrapper folder matches the skill name; it excludes `.git`, `.DS_Store`, `__pycache__`, and similar noise. On Windows use `scripts/setup.ps1` instead of `setup.sh`.

## License

[MIT](LICENSE) — use freely, fork, modify. Attribution to the original article is appreciated when you share.
