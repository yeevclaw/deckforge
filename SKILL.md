---
name: ppt-agent
description: "Build professional-grade PowerPoint presentations using a 5-phase expert workflow (research → outline → planning → design → produce) — not by stuffing content into templates. Use this skill whenever the user asks for a PPT, deck, slides, presentation, pitch deck, sales deck, business proposal, product introduction, company intro, kick-off deck, or anything similar — even if they don't say 'PowerPoint' explicitly. Especially preferred for any presentation that needs to actually look good (business proposals, sales pitches, executive briefings, product launches). Trigger on phrases like 'make me a deck about X', 'build a presentation', '幫我做一份簡報', '做個PPT', 'put together slides', or any request that ends in a .pptx file."
license: MIT
---

# PPT Agent — Expert PowerPoint Workflow

This skill turns Claude into a **PPT planning team + designer**, not a template-filler. It mirrors how top-tier PPT design agencies actually work: research the audience, plan content first, then design.

## Core philosophy

> **PPT 的靈魂是內容,不是皮囊。** (A PPT's soul is content, not its skin.)

Most AI PPT tools fail because they jump straight from "topic" to "designed slides" — same recycled template, generic bullets, no thought. This skill enforces a **5-phase workflow** that human experts use, then turns each finished page into a high-fidelity slide via HTML rendering.

The methodology is adapted from the "Strongest PPT Agent" essay shared on linux.do by author *sandun* (a 7-year PPT instructor + 3-year AI product builder). Credit where due.

---

## When to use this skill

Use whenever the user wants a presentation, deck, slides, or a `.pptx` file produced — especially for business proposals, sales decks, product intros, executive briefings, kick-off decks, or anything where "it has to look good". Don't use this skill if the user only wants to *read or extract text* from an existing `.pptx` — use the built-in `pptx` skill for that.

If the user already has a topic and just wants slides fast, you can compress phases 1–2, but **never skip the Planning Draft (phase 3)** — that's where AI-generated decks usually fall apart.

---

## The 5-phase workflow

| Phase | Name | Output | Don't skip when… |
|---|---|---|---|
| 1 | **Needs research** (需求調研) | Audience, purpose, tone, length, constraints | Always — but compress to one round of questions if user is in a hurry |
| 2 | **Outline architecture** (大綱規劃) | `outline.json` with cover / TOC / parts / pages | Always |
| 3 | **Planning draft** (策劃稿) | `planning.json` with layout intent per page | Always — this is the secret sauce |
| 4 | **Design** (設計稿) | One styled `.html` per page (1280×720) | Always |
| 5 | **Produce** (產出) | Final `.pptx` | Always |

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
      "layout": "single_focus" | "two_col_50_50" | "two_col_2_1" | "three_col" | "hero_top" | "mixed_grid",
      "cards": [
        { "heading": "...", "body": "...", "icon_hint": "lightbulb", "size_hint": "large" }
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

For each page in `planning.json`, generate **one self-contained HTML file** at 1280×720, styled with the Bento Grid system.

- Master prompt: [prompts/05_designer_html.md](prompts/05_designer_html.md)
- Bento Grid spec: [references/bento_grid.md](references/bento_grid.md)
- Color + typography system: [references/design_system.md](references/design_system.md)
- HTML templates to start from: [templates/](templates/) — `cover.html`, `toc.html`, `bento_2col.html`, `bento_3col.html`, `bento_hero.html`, `bento_mixed.html`

Key rules:
- **Pick a content-informed color palette ONCE** at the start of phase 4, then reuse it on every page. Don't re-pick per page.
- **Pick one visual motif** (rounded card corners + soft shadow, thick left accent bar, icon-in-circle, gradient mesh background) and repeat it everywhere.
- **Cards must have ≥20px gaps**, and use **size to express importance** (big card = important info).
- **Never** add accent underlines beneath page titles — it's the #1 AI-deck tell.
- **Avoid stock photos** unless the user provides them. Use CSS gradients, icon glyphs (inline SVG), or abstract shapes instead.

Save each page as `pages/page_01.html`, `pages/page_02.html`, …

### Phase 5 — Produce (產出)

Run the bundled converter:

```bash
python scripts/html_to_pptx.py \
  --pages-dir pages/ \
  --output presentation.pptx \
  --width 1280 --height 720
```

This script:
1. Renders each HTML to a 1920×1080 PNG via headless Chromium (Playwright).
2. Creates a 16:9 PPTX with one slide per page, full-bleed image at slide background.
3. Attaches speaker notes from `planning.json` if it's in the same directory.

If Playwright isn't installed, the script falls back to `weasyprint` (HTML → PDF → PNG). Either path produces the same final PPTX.

For users who need **editable** slides (text remains as PowerPoint text boxes, not pixels), pass `--mode editable` — see [references/editable_mode.md](references/editable_mode.md). The default `--mode image` gives perfect design fidelity; `--mode editable` trades fidelity for editability.

---

## QA — DO NOT SKIP

After producing `presentation.pptx`, convert it back to images and visually inspect — the same way the built-in `pptx` skill does:

```bash
soffice --headless --convert-to pdf presentation.pptx
pdftoppm -jpeg -r 100 presentation.pdf slide
ls -1 "$PWD"/slide-*.jpg
```

Then look at the slides yourself (or use a subagent if available) and check for:
- Text overflow / cutoff
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
│   ├── 01_needs_research.md          ← phase 1 question template
│   ├── 02_outline_architect.md       ← phase 2 master prompt
│   ├── 03_content_research.md        ← phase 2.5 (optional web research)
│   ├── 04_planning_draft.md          ← phase 3 master prompt
│   └── 05_designer_html.md           ← phase 4 master prompt
├── references/
│   ├── bento_grid.md                 ← Bento Grid layout system
│   ├── design_system.md              ← palettes, typography, motifs
│   ├── pyramid_principle.md          ← 金字塔原理 quick guide
│   └── editable_mode.md              ← --mode editable details
├── templates/                         ← HTML starting points (1280×720)
│   ├── _base.html
│   ├── cover.html
│   ├── toc.html
│   ├── bento_2col.html
│   ├── bento_3col.html
│   ├── bento_hero.html
│   └── bento_mixed.html
├── scripts/
│   ├── html_to_pptx.py               ← the converter
│   └── render_html.py                ← HTML→PNG helper
└── examples/
    ├── Claude-Enterprise-Pitch.pdf   ← rendered demo (6 pages)
    └── slide-1.jpg ... 6             ← preview thumbnails
```

---

## Dependencies

```bash
pip install python-pptx Pillow --break-system-packages
pip install playwright --break-system-packages && playwright install chromium
# Fallback if Playwright isn't available:
pip install weasyprint --break-system-packages
```

The converter handles missing dependencies gracefully — it'll tell you what to install.
