---
name: deckforge
description: "Build professional-grade PowerPoint presentations using a 5-phase expert workflow (research → outline → planning → design → produce) — not by stuffing content into templates. Output is editable SVG slides assembled into a .pptx that PowerPoint 2016+ can Convert-to-Shape for full editing. Use this skill whenever the user asks for a PPT, deck, slides, presentation, pitch deck, sales deck, business proposal, product introduction, company intro, kick-off deck, or anything similar — even if they don't say 'PowerPoint' explicitly. Especially preferred for any presentation that needs to actually look good (business proposals, sales pitches, executive briefings, product launches). Trigger on phrases like 'make me a deck about X', 'build a presentation', '幫我做一份簡報', '做個PPT', 'put together slides', or any request that ends in a .pptx file."
license: MIT
---

# PPT Agent — Expert PowerPoint Workflow (SVG pipeline)

This skill turns Claude into a **PPT planning team + designer**, not a template-filler. It mirrors how top-tier PPT design agencies actually work: research the audience, plan content first, then design.

## Core philosophy

> **PPT 的靈魂是內容,不是皮囊。** (A PPT's soul is content, not its skin.)

Most AI PPT tools fail because they jump straight from "topic" to "designed slides" — same recycled template, generic bullets, no thought. This skill enforces a **5-phase workflow** that human experts use, then renders each finished page to **SVG** and assembles them into an editable `.pptx`.

The methodology is adapted from the "Strongest PPT Agent" essay shared on linux.do by author *sandun* (a 7-year PPT instructor + 3-year AI product builder). The choice of SVG as the final design format also comes from that essay: SVG is the only format that gives both Figma-level design control *and* native editability in PowerPoint 2016+.

---

## When to use this skill

Use whenever the user wants a presentation, deck, slides, or a `.pptx` file produced — especially for business proposals, sales decks, product intros, executive briefings, kick-off decks, or anything where "it has to look good". Don't use this skill if the user only wants to *read or extract text* from an existing `.pptx` — use the built-in `pptx` skill for that.

If the user already has a topic and just wants slides fast, you can compress phases 1–2, but **never skip the Planning Draft (phase 3)** — that's where AI-generated decks usually fall apart.

## Before starting — heads-up about Phase 5 dependencies

Phases 1–4 produce SVG files and need **zero Python packages**. Phase 5 (assembling the `.pptx`) needs **two Python packages, both pip-installable with zero system deps**:

1. **`python-pptx`** (required, ~1 MB) — builds the .pptx file.
2. **`resvg-py`** (strongly recommended, ~1 MB) — rasterizes each slide's SVG into a PNG fallback so the deck displays correctly in **Keynote, macOS Preview, Quick Look, and PowerPoint pre-2016**. Without it, those viewers show blank slides (only PowerPoint 2016+ renders correctly via the embedded SVG).

resvg-py is a pip wheel that ships a self-contained Rust binary — no Homebrew, no apt-get, no sudo needed. `cairosvg`, `inkscape`, and `rsvg-convert` also work if any of them is already on the user's system.

If this is the user's first time running the skill, mention this at the start of Phase 1 so they can install in parallel:

> *"This skill runs 5 phases. The first 4 don't need anything installed. The final .pptx assembly needs two pip packages: `python-pptx` and `resvg-py`. Easiest: `bash scripts/setup.sh` from inside the deckforge folder. Or run `pip install python-pptx resvg-py --break-system-packages` directly. While that runs, I'll start Phase 1."*

### Common errors and how to recover

- **`ModuleNotFoundError: No module named 'pptx'`** — user hasn't installed `python-pptx`. Have them run `pip install python-pptx --break-system-packages` and re-run Phase 5.
- **Slides display blank in Keynote / macOS Preview, fine in PowerPoint** — no SVG renderer installed. The script prints a clear warning during Phase 5. Easiest fix: `pip install resvg-py --break-system-packages`. Then re-run Phase 5.
- **Keynote refuses to open the .pptx entirely** — try re-running Phase 5 with `--no-svg` to skip the svgBlip extension. Slides become image-only but Keynote will open them. The trade-off: Convert-to-Shape editability in PowerPoint goes away.

### Where the deckforge folder lives

It may be in different places depending on install:
- **Claude Desktop**: `~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/<UUID>/<UUID>/skills/deckforge/` (Desktop manages this; don't write to it manually)
- **Claude Code CLI**: `~/.claude/skills/deckforge/`
- **Source clone**: wherever the user ran `git clone` (often `~/deckforge`)

Don't assume a path. Refer to "the deckforge folder" or run scripts via relative path from the skill folder.

---

## The workflow

The base workflow is 5 phases. Add a **Phase 0** when the user supplies a source document (PDF, annual report, transcript, whitepaper, etc.) — extract a structured analysis first, then run the rest.

| Phase | Name | Output | When to run |
|---|---|---|---|
| 0 | **Source analysis** (文件分析) | `analysis.md` — key metrics, claims, parallel sets, anomalies | Only when user gives a source document. See [prompts/00_source_analysis.md](prompts/00_source_analysis.md) |
| 1 | **Needs research** (需求調研) | Audience, purpose, tone, length, constraints | Always — compress to one round if user is in a hurry |
| 2 | **Outline architecture** (大綱規劃) | `outline.json` with cover / TOC / parts / pages | Always |
| 3 | **Planning draft** (策劃稿) | `planning.json` with per-page layout, cards, charts | Always — this is the secret sauce |
| 4 | **Design** (設計稿) | One `.svg` per page (`viewBox="0 0 1280 720"`) | Always |
| 5 | **Produce** (產出) | Final `.pptx` (vector SVG + PNG fallback) **and** companion `.pdf` (PNG pages) | Always |

### Phase 1 — Needs research

Don't grab the topic and run. Behave like a consultant. Ask a tight set of questions before doing anything. Use `AskUserQuestion` if available; otherwise ask inline. See [prompts/01_needs_research.md](prompts/01_needs_research.md) for the exact question template.

What you must extract before moving on:
- **Audience**: who will see this? (investors, customers, internal team, students…)
- **Purpose**: what should they think/feel/do after?
- **Length**: rough page count (10? 20? 40?)
- **Tone**: serious / playful / data-heavy / story-driven
- **Brand constraints**: any colors, fonts, logos, do-not-mention items?
- **Visual style hint**: clean minimal / bold corporate / tech-futuristic / warm humanistic / academic
- **Language**: 中文 / English / bilingual

If the user has uploaded reference material (e.g., a doc, a website URL, a previous deck), read it first.

### Phase 2 — Outline architecture (大綱規劃)

Use the **金字塔原理 (pyramid principle)** + 便利貼法 ("sticky-note method"): each page is one digital sticky note. Logic first, design later.

The exact prompt to feed into your reasoning is in [prompts/02_outline_architect.md](prompts/02_outline_architect.md). It enforces a JSON schema with this shape:

```json
{
  "ppt_outline": {
    "cover": { "title": "...", "sub_title": "...", "content": [] },
    "table_of_contents": { "title": "目錄", "content": ["第一部分標題", "..."] },
    "parts": [
      {
        "part_title": "第一部分:章節標題",
        "pages": [
          { "title": "頁面標題1", "content": [] },
          { "title": "頁面標題2", "content": [] }
        ]
      }
    ],
    "end_page": { "title": "總結與展望", "content": [] }
  }
}
```

Save the outline to `outline.json` in the working directory. Show it to the user for review (digital sticky notes — easy to add/remove/reorder before any design work happens).

### Phase 3 — Planning draft (策劃稿) — DO NOT SKIP

This is what most AI PPT tools miss. Before any design, decide for **each page**:
- What concrete content goes there (bullets, stats, quotes, charts — actual words, not placeholders)
- Which **Bento Grid layout** fits (see [references/bento_grid.md](references/bento_grid.md))
- What visual elements are needed (icons, images, charts, no-element)
- Speaker notes (1–2 sentences per page)

Use the prompt in [prompts/04_planning_draft.md](prompts/04_planning_draft.md). Output goes to `planning.json` with this shape:

```json
{
  "pages": [
    {
      "page_id": 1,
      "page_type": "cover" | "toc" | "content" | "section_break" | "end",
      "title": "...",
      "subtitle": "...",
      "layout": "single_focus" | "stat_hero" | "mini_grid" | "two_col_50_50" | "two_col_2_1" | "three_col" | "hero_top" | "mixed_grid",
      "cards": [
        { "is_number_first": true, "stat_value": "42%", "stat_caption": "三年複合成長率", "stat_caption_en": "CAGR", "size_hint": "small" },
        { "is_number_first": false, "heading": "服務優先", "body": "服務收入占比由 8% 升至 27%", "icon_hint": "trending-up", "size_hint": "small" }
      ],
      "visual_notes": "Use abstract gradient background, no stock photos",
      "speaker_notes": "..."
    }
  ]
}
```

Why this phase exists: top PPT agencies have a **Planner** role separate from the **Designer**. The Planner decides what + where; the Designer decides how it looks. Mixing these jobs produces the busy, cluttered slides that scream "AI generated".

If the deck is important, **let the user review `planning.json` before designing**. Cheap to fix here, expensive to fix later.

### Phase 4 — Design (設計稿)

For each page in `planning.json`, generate **one self-contained SVG file** with `viewBox="0 0 1280 720"`, styled with the Bento Grid system.

- Master prompt: [prompts/05_designer_svg.md](prompts/05_designer_svg.md)
- Bento Grid spec: [references/bento_grid.md](references/bento_grid.md)
- Color + typography system: [references/design_system.md](references/design_system.md)
- SVG templates to start from: [templates/](templates/) — `cover.svg`, `toc.svg`, `bento_2col.svg`, `bento_3col.svg`, `bento_hero.svg`, `bento_mixed.svg` (and `_base.svg` for shared filters/icons)

Key rules:
- **Default to the `dark_apple` palette family** unless the user explicitly asks for a light/brand look. Pure black bg + one highlight color is what produces the visual-quality jump (see [references/design_system.md](references/design_system.md)).
- **Pick the palette AND the single highlight color ONCE** at the start of phase 4 (auto-detect from brand if possible: Xiaomi `#FF6900`, Tesla `#E31937`, etc.). Reuse on every page. **Never use a second accent color.**
- **Pick one visual motif** (default `apple_dark_cards`) and repeat it everywhere.
- **Prefer `stat_hero` and `mini_grid` for data-dense pages.** A page that fits 4 KPI numbers should be a `mini_grid`, not 4 sentences in `two_col_50_50`.
- **One card, one core point.** If a card body has multiple sentences or a heading + 3 bullets, split it into a mini_grid.
- **Number-first cards beat text-first cards.** Whenever a key number captures the message, render it at 80–120px in the highlight color.
- **Bilingual title pattern.** Page titles render as Chinese (big, white) + small English subtitle (gray, decorative).
- **Dramatic typography contrast.** Hero number 80px / body 14px is correct. Title 32px / body 24px is not — too flat.
- **Cards must have ≥20px (main) or ≥24px (mini) gaps.** Use size to express importance.
- **Never** add accent underlines beneath page titles — it's the #1 AI-deck tell.
- **Never use emoji as functional icons.** Inline Lucide `<path>` or no icon.
- **Avoid stock photos.** Use SVG gradients, inline icon `<path>`s, or abstract shapes.
- **Every text run lives in a real `<text>` element** (not converted to path) — that's what keeps slides editable after Convert to Shape.

Save each page as `pages/page_01.svg`, `pages/page_02.svg`, …

### Phase 5 — Produce (產出) — DELIVERS MULTIPLE FILES

> ⚠️ **THE MOST COMMON BUG IN PHASE 5: only delivering the `.pptx`.** Read this entire section. Phase 5 produces 2–3 files and you must deliver every one of them.

Run the bundled converter:

```bash
python scripts/svg_to_pptx.py \
  --pages-dir pages/ \
  --output presentation.pptx
```

This script:
1. Renders each SVG to a high-DPI PNG via `resvg-py` (zero system deps).
2. Creates a 16:9 PPTX with one slide per page; each slide embeds the original SVG via the PowerPoint 2016+ `svgBlip` extension plus the PNG fallback.
3. Assembles the same PNGs into a companion `.pdf` (named after `--output` with the `.pdf` extension) via `img2pdf`.
4. If any page in `planning.json` has `speaker_notes`, writes them to a `<stem>.notes.md` sibling file (notes are NOT embedded in the .pptx — that breaks Keynote — they live in this Markdown file).

### Mandatory delivery checklist — do this every Phase 5

After the script runs successfully, you MUST do this BEFORE telling the user you're done:

**Step 1: Read the script's stdout footer.**

The last block the script prints looks like:

```
⚠️  IMPORTANT: 3 files were produced — ALL should be delivered to the user.
    • /path/to/deck.pptx
    • /path/to/deck.pdf
    • /path/to/deck.notes.md
```

The number `N files` is the count you must deliver. Anything less is a failed Phase 5.

**Step 2: List the output directory to confirm.**

Run `ls -la <output-directory>` or `Read` each path. Confirm every file the stdout listed actually exists. If a path is missing, the script failed silently — debug before declaring done.

**Step 3: Attach EVERY file to your reply to the user.**

Each file in the stdout list must be delivered, not just the `.pptx`. Common failure mode (please don't fall into it): "I attached the .pptx, that's the main thing, .pdf and .notes.md are bonus." **No.** They are part of the same deliverable set. The user expects all three from a single Phase 5 run.

If you're operating in Claude Desktop, this means attaching each file individually to the chat. If a tool / agent harness wraps your file output, attach each file as a separate response.

**Step 4: Mention every file in the prose of your reply.**

Tell the user explicitly what was produced. Example phrasing:

> "Phase 5 produced three files for you:
> - `deck.pptx` — open in PowerPoint to edit (right-click a slide → Convert to Shape).
> - `deck.pdf` — share with anyone, opens in any PDF reader / mobile / web.
> - `deck.notes.md` — speaker notes per slide, plain Markdown.
> All three are attached above."

If only 2 files exist (no speaker notes), say so explicitly. If only 1 exists (you passed `--no-pdf` or `--placeholder-only`), say so explicitly and explain why.

**Why this matters**: the .pdf and .notes.md sit in a Phase-5 working directory that Claude Desktop tears down at session end. If you don't actively attach them, they're permanently lost. This is the single most reported user complaint about DeckForge.

### Speaker notes — why they go to .notes.md, not into the .pptx

python-pptx's `slide.notes_slide.notes_text_frame.text = ...` mechanism injects `notesSlide` parts, a `notesMaster` part, a `theme2.xml`, and several Content_Types overrides into the PPTX. Keynote 14+ rejects the file outright with "檔案格式無效 / Invalid file format" when it encounters this combination — even though the file is valid OOXML and opens fine in PowerPoint.

Rather than ship a deck that's broken in Keynote, DeckForge **always writes speaker notes to a sibling `<stem>.notes.md` file** and post-processes the `.pptx` to strip the offending parts. The PPTX is then clean and opens in Keynote, PowerPoint, Preview, Quick Look, and Google Slides uniformly.

If the user truly needs in-PPTX notes for PowerPoint Presenter View (and accepts that Keynote will refuse the file), pass `--keep-notes` to `svg_to_pptx.py`. The default is the safe path.

### Heads-up: macOS may quarantine the .pptx

When Claude Desktop writes the produced PPTX into the user's Downloads (or anywhere outside its sandbox), macOS sometimes attaches the `com.apple.quarantine` extended attribute. Keynote will then **refuse to open the file** entirely. This is a Gatekeeper-related macOS behavior, not a problem with the PPTX itself. If the user reports "Keynote can't open the file", tell them:

```bash
xattr -d com.apple.quarantine /path/to/deck.pptx
```

This is a one-liner that strips the quarantine flag. PowerPoint typically handles quarantine more gracefully and isn't affected.

**Editing the result**: in PowerPoint 2016 or newer, right-click any slide's picture → **Convert to Shape**. The SVG decomposes into native PowerPoint shapes and text boxes — every card, title, and icon becomes editable.

**Flags worth knowing**:
- `--no-pdf` — skip the companion PDF (PPTX-only)
- `--pdf-output PATH` — explicit PDF path (defaults to `<pptx-stem>.pdf`)
- `--no-svg` — skip the svgBlip extension; PPTX becomes image-only. Use as escape hatch for viewers that choke on the SVG ext. Requires a working SVG renderer or the script aborts.
- `--placeholder-only` — force the 1×1 transparent placeholder PNG even if a real renderer is available. Smaller PPTX file but it only displays correctly in PowerPoint 2016+; the companion PDF is automatically skipped.

---

## QA — DO NOT SKIP

After producing `presentation.pptx`, convert it back to images and visually inspect — the same way the built-in `pptx` skill does:

```bash
soffice --headless --convert-to pdf presentation.pptx
pdftoppm -jpeg -r 100 presentation.pdf slide
ls -1 "$PWD"/slide-*.jpg
```

Then look at the slides yourself (or use a subagent if available) and check for:
- Text overflow / cutoff (especially: SVG doesn't auto-wrap, so missing `<tspan>` rows = clipped sentences)
- Card overlap or near-touching gaps
- Low-contrast text
- Inconsistent palette across slides
- Missing speaker notes where intended

Fix and re-render. Don't declare done until one full clean pass.

---

## Quick recipes

### Recipe A — Full enterprise deck (45 min)

User: "Make me an investor pitch deck for our SaaS product."

1. Phase 1: ask 4 questions (audience, ask amount, key traction stat, brand colors)
2. Phase 2: generate outline.json (probably 12–18 pages)
3. Phase 3: generate planning.json — show to user, get sign-off
4. Phase 4: render all pages with a chosen palette (e.g., Midnight Executive)
5. Phase 5: produce `pitch.pptx`
6. QA loop

### Recipe B — Quick one-pager / short deck (10 min)

User: "Quick deck on the Q4 results, 5 slides, internal team."

1. Compress phase 1 to one inline question
2. Outline + planning in one go (it's short)
3. Render + produce
4. Skip the sign-off — go straight to QA

### Recipe C — User has a draft

User: "I have this Word doc, turn it into slides."

1. Read the doc first
2. Skip phase 1 (audience is implied by content), generate outline from the doc
3. Continue from phase 3 as usual

---

## File map

```
deckforge/                            ← (or whatever you name the skill folder)
├── SKILL.md                          ← you are here
├── prompts/
│   ├── 00_source_analysis.md         ← phase 0 (when user supplies a document)
│   ├── 01_needs_research.md          ← phase 1 question template
│   ├── 02_outline_architect.md       ← phase 2 master prompt
│   ├── 03_content_research.md        ← phase 2.5 (optional web research)
│   ├── 04_planning_draft.md          ← phase 3 master prompt (with extraction examples)
│   └── 05_designer_svg.md            ← phase 4 master prompt (SVG output)
├── references/
│   ├── bento_grid.md                 ← Bento Grid layout system (8 layouts)
│   ├── chart_anatomy.md              ← SVG bar / line / donut charts
│   ├── design_system.md              ← palettes, typography, motifs
│   ├── pyramid_principle.md          ← 金字塔原理 quick guide
│   └── editable_mode.md              ← how Convert-to-Shape works in PowerPoint
├── templates/                         ← SVG starting points (viewBox 0 0 1280 720)
│   ├── _base.svg                     ← shared filters / gradients / 35 Lucide icons
│   ├── cover.svg
│   ├── toc.svg
│   ├── bento_2col.svg                ← 50/50 or 2:1 (switch widths)
│   ├── bento_3col.svg
│   ├── bento_hero.svg
│   ├── bento_mini_grid.svg           ← main card with 3–6 mini-cards (dark_apple)
│   ├── bento_mixed.svg
│   ├── chart_bar.svg                 ← vertical bar chart (single highlight color)
│   ├── chart_line.svg                ← line + area chart for trends
│   └── chart_donut.svg               ← donut chart with center label + legend
├── scripts/
│   ├── svg_to_pptx.py                ← SVG → PPTX assembler (with svgBlip ext)
│   ├── package.sh                    ← build deckforge.zip for Claude Desktop upload
│   ├── setup.sh                      ← one-line dependency installer (mac/linux)
│   └── setup.ps1                     ← same, for Windows PowerShell
└── examples/
    ├── DeckForge-demo.pdf            ← rendered demo (3 pages)
    ├── slide-1.jpg ... 3             ← preview thumbnails
    └── sample-deck/                  ← source SVG pages of the demo
```

---

## Dependencies

**Phases 1–4 are pure Markdown — no dependencies at all.** Only the Phase 5 converter (`svg_to_pptx.py`) needs three small pip packages:

```bash
bash scripts/setup.sh
# or
pip install python-pptx resvg-py img2pdf --break-system-packages
```

All three are pip wheels with zero system dependencies — works on macOS / Linux / Windows / PyPy without Homebrew, apt, or sudo. (`cairosvg`, `inkscape`, or `rsvg-convert` are also auto-detected if you happen to have them, but resvg-py covers the case.)
