# DeckForge

**English** · [繁體中文](README.zh-TW.md)

> A Claude skill that produces **professional-grade PowerPoint decks** by following a 5-phase expert workflow (research → outline → planning → design → produce), rather than stuffing your topic into a generic template.

Inspired by the methodology shared by *sandun* on linux.do ("应该是目前最强的PPT Agent，附上完整思路分享"). Adapted to an HTML → PPTX pipeline for native Claude file output.

## Demo

A complete AcmeCloud Series B fundraising deck, produced end-to-end by this skill:

| | | |
|---|---|---|
| ![](examples/slide-1.jpg) | ![](examples/slide-2.jpg) | ![](examples/slide-3.jpg) |
| ![](examples/slide-4.jpg) | ![](examples/slide-5.jpg) | |

The rendered `.pptx` lives at [`examples/AcmeCloud_demo.pptx`](examples/AcmeCloud_demo.pptx).

## What's inside

```
DeckForge/
├── SKILL.md                ← skill entry — Claude reads this first
├── prompts/                ← 5 reusable expert prompts (one per phase)
│   ├── 01_needs_research.md
│   ├── 02_outline_architect.md
│   ├── 03_content_research.md
│   ├── 04_planning_draft.md
│   └── 05_designer_html.md
├── references/             ← detailed knowledge bases
│   ├── bento_grid.md       ← Bento Grid layout system (the secret sauce)
│   ├── design_system.md    ← 10 palettes + motifs + typography
│   ├── pyramid_principle.md
│   └── editable_mode.md
├── templates/              ← HTML starting points (1280×720)
│   ├── _base.html
│   ├── cover.html
│   ├── toc.html
│   ├── bento_2col.html
│   ├── bento_3col.html
│   ├── bento_hero.html
│   └── bento_mixed.html
├── scripts/
│   ├── html_to_pptx.py     ← the converter (HTML → PNG → PPTX)
│   └── render_html.py      ← HTML→PNG helper (Playwright primary, LibreOffice fallback)
└── examples/               ← live demo (AcmeCloud Series B deck)
    ├── example_outline.json
    ├── example_planning.json
    ├── pages/              ← 5 fully-styled HTML slides
    ├── AcmeCloud_demo.pptx ← the rendered output
    └── slide-1.jpg ... 5   ← preview of each page
```

## Install as a Claude skill

Drop this whole folder into your Claude skills directory, named so the path looks like:

```
~/.claude/skills/deckforge/        # standalone Claude Code
# or
~/.claude/skills/deckforge/        # Cowork
```

Then in Claude/Cowork ask:

> *幫我做一份簡報,主題是 XYZ*
> *Build me a deck about XYZ*

Claude reads `SKILL.md`, follows the 5-phase workflow, and produces a `.pptx`.

## Try the demo locally

```bash
git clone https://github.com/<your-username>/DeckForge.git
cd DeckForge
pip install python-pptx playwright Pillow --break-system-packages
playwright install chromium

# Re-render the included demo from its HTML sources:
python scripts/html_to_pptx.py \
  --pages-dir examples/pages \
  --output examples/AcmeCloud_demo.pptx \
  --planning examples/example_planning.json
```

## The 5 phases (overview)

| Phase | Output |
|---|---|
| 1 — Needs research | `brief.md` (audience, goal, length, tone) |
| 2 — Outline architecture | `outline.json` (pyramid principle, page titles as claims) |
| 3 — **Planning draft** | `planning.json` (actual content + layout intent per page) ← *the step most AI tools skip* |
| 4 — Design | `pages/page_NN.html` (one styled HTML page per slide) |
| 5 — Produce | `presentation.pptx` |

The skill is **NOT** a one-shot generator. It deliberately includes review checkpoints (after outline, after planning) so you can fix things cheaply before any design effort is spent.

## Why HTML → PPTX (not template-based)?

- Modern CSS (CSS Grid, gradients, mix-blend-mode) gives near-Figma design quality.
- Per-deck palette + motif consistency (the skill enforces this).
- Free to design *content-informed* layouts instead of forcing content into a template.
- Trade-off: the produced PPTX uses image slides (text isn't editable in PowerPoint). For editable text, see [`references/editable_mode.md`](references/editable_mode.md).

## Dependencies

- `python-pptx` — PPTX assembly
- `playwright` + Chromium — HTML rendering (primary)
- `libreoffice` + `poppler-utils` — fallback HTML rendering (limited CSS support)
- `Pillow` — image handling

## Credits

- Methodology: *sandun* @ linux.do — original article ("应该是目前最强的PPT Agent，附上完整思路分享")
- The "顶级的PPT结构架构师" and "便當網格" prompts in `prompts/02_outline_architect.md` and `references/bento_grid.md` are direct adaptations of his prompts, with extensions.
- Bento Grid design language: popularized by Apple product pages.
- Pyramid Principle: Barbara Minto.

## License

[MIT](LICENSE) — use freely, fork, modify. Attribution to the original article is appreciated when you share.
