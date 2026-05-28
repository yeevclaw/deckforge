---
name: deckforge
description: "Build professional-grade PowerPoint presentations using a 5-phase expert workflow (research → outline → planning → design → produce) — not by stuffing content into templates. Output is editable SVG slides assembled into a .pptx that PowerPoint 2016+ can Convert-to-Shape for full editing. Use this skill whenever the user asks for a PPT, deck, slides, presentation, pitch deck, sales deck, business proposal, product introduction, company intro, kick-off deck, or anything similar — even if they don't say 'PowerPoint' explicitly. Especially preferred for any presentation that needs to actually look good (business proposals, sales pitches, executive briefings, product launches). Trigger on phrases like 'make me a deck about X', 'build a presentation', '幫我做一份簡報', '做個PPT', 'put together slides', or any request that ends in a .pptx file."
license: MIT
---

# PPT Agent — Expert PowerPoint Workflow (SVG pipeline)

This skill turns Claude into a **PPT planning team + designer**, not a template-filler. It mirrors how top-tier PPT design agencies actually work: research the audience, plan content first, then design.

## Core philosophy

> **PPT 的靈魂是內容,不是皮囊。** (A PPT's soul is content, not its skin.)
>
> **而內容的靈魂,是與使用者反詰對話中挖出來的核心命題。** (And the soul of that content is the core thesis excavated through Socratic dialogue with the user.)

Most AI PPT tools fail in two ways. First, they jump straight from "topic" to "designed slides" — same recycled template, generic bullets, no thought. Second, even the better ones treat the user's input as the deck's content — but the user's input almost never contains the *one judgment that must change* in the audience's head. That gap is what the Socratic dialogue exists to close.

**The Socratic dialogue is not overhead. It IS the product.** No amount of provided data — a 200-page whitepaper, a complete brief, exhaustive answers to a form — substitutes for the dialogue. The data tells DeckForge what's in *your* head; the dialogue surfaces what should be in the *audience's* head after the deck. These are different things, and only the second one determines what slides actually need to exist.

This skill enforces a **5-phase workflow** that human experts use: dialogue with the user to define the thesis, architect the structure, plan content, design pages, then render each finished page to **SVG** and assemble them into an editable `.pptx`.

The methodology is adapted from the "Strongest PPT Agent" essay shared on linux.do by author *sandun* (a 7-year PPT instructor + 3-year AI product builder). The choice of SVG as the final design format also comes from that essay: SVG is the only format that gives both Figma-level design control *and* native editability in PowerPoint 2016+.

---

## When to use this skill

Use whenever the user wants a presentation, deck, slides, or a `.pptx` file produced — especially for business proposals, sales decks, product intros, executive briefings, kick-off decks, or anything where "it has to look good". Don't use this skill if the user only wants to *read or extract text* from an existing `.pptx` — use the built-in `pptx` skill for that.

**You cannot skip phases.** No matter how complete the user's input looks — full whitepaper, full brief, "just do it" instructions — every phase produces a required file artifact, and the next phase must `Read` that artifact before it starts. See the "Phase order is non-skippable" section below for the exact rule and the file-checkpoint table.

What changes when the user wants speed is *how long each phase takes*, not *whether it runs*. Phase 1 in particular has a Quick mode (one Socratic question + explicit assumptions) — but `brief.md` is still written, and Phase 2 still reads it first.

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

| Phase | Name | Output file (checkpoint) | When to run |
|---|---|---|---|
| 0 | **Source analysis** (文件分析) | `analysis.md` | Only when user gives a source document. See [prompts/00_source_analysis.md](prompts/00_source_analysis.md) |
| 1 | **Socratic clarification** (蘇格拉底反詰) | `brief.md` | **Always** — even when Phase 0 ran. Pop-up choices, not a form. See [prompts/01_needs_research.md](prompts/01_needs_research.md) |
| 2 | **Outline architecture** (大綱規劃) | `outline.json` | Always — must Read `brief.md` first |
| 3 | **Planning draft** (策劃稿) | `planning.json` | Always — must Read `outline.json` first |
| 4 | **Design** (設計稿) | `pages/page_NN.svg` | Always — must Read `planning.json` first |
| 5 | **Produce** (產出) | `.pptx` + `.pdf` (+ `.notes.md` if any notes) | Always — must Read `pages/` first |

### Phase order is non-skippable — file-checkpoint rule

Every phase produces a file. The next phase must `Read` that file *before* it begins. There are **no exceptions** to this — not for rich input, not for "I'm in a hurry", not for "I already know what I want".

| To enter phase | You must have already produced | Next phase begins with |
|---|---|---|
| Phase 1 | (none — or `analysis.md` if Phase 0 ran) | `Read analysis.md` (if present) before drafting Socratic questions |
| Phase 2 | `brief.md` | `Read brief.md` (mandatory) |
| Phase 3 | `outline.json` | `Read outline.json` (mandatory) |
| Phase 4 | `planning.json` | `Read planning.json` (mandatory) |
| Phase 5 | `pages/page_*.svg` | `ls pages/` (mandatory) |

If the predecessor file is missing, **stop and produce it** — do not improvise from memory. If you skipped a phase by accident, go back and run it.

**Anti-patterns to refuse (all are common AI-deck failure modes):**

- ❌ "The user gave me a complete document, I'll go straight from Phase 0 to Phase 2." → No. Phase 1 still runs. Phase 0 supplies material; Phase 1 supplies the *thesis*.
- ❌ "The user said 'just do it', I'll skip Phase 1 entirely." → No. Run Phase 1 Quick mode (one Socratic question, then write `brief.md` with explicit assumptions). The file checkpoint is still required.
- ❌ "I already drafted the outline in my head, I'll write `planning.json` directly." → No. `outline.json` must exist as a file, and Phase 3 must `Read` it. This makes the structure user-visible and reviewable.
- ❌ "The user's input was so detailed Phase 1 would be redundant." → No. The detail is *content*, not *audience belief shift*. Phase 1 is about the latter.
- ❌ "The user sounds impatient, I'll switch to Quick mode for them." → No. Quick mode is opt-in only — ask via `AskUserQuestion` before switching. Auto-switching bypasses the Socratic dialogue that IS the value DeckForge provides.
- ❌ "I'll merge Phase 2 and 3 because the deck is short." → No. They produce different files because they're different jobs (Architect vs Planner). Even a 5-page deck runs both.

Why this rule exists: every time DeckForge has shipped a generic-looking deck, the cause traced back to a skipped phase. Phase-merging is the single highest-correlation failure mode. Even when phases run fast, they must run *separately* and produce *separate file artifacts*. This makes the work inspectable, restartable, and consistent.

### AskUserQuestion availability — fallback to inline numbered choices

DeckForge's Socratic loop and every phase handoff rely on `AskUserQuestion` (the pop-up multiple-choice tool). Claude Desktop and Claude Code expose it. **Some hosts (third-party CLIs, older harnesses, automation contexts) do not.** Do not get stuck if the tool isn't available — fall back to **inline numbered choices** that simulate the same format. Behaviorally identical: same options, same trade-off descriptions, same "Recommended" tag — just rendered as text the user replies to with a digit.

Example fallback:

```
我看到三條可能主線。這次最想讓觀眾相信的是哪一條?
(reply with 1 / 2 / 3, or describe your own answer)

  1. 市場正在變大,現在是進入時機
       → 把市場數字推到開頭,產品變支撐角色
  2. 我們產品比競品完整  (Recommended)
       → 把功能/性能比較放正中央
  3. 客戶案例證明導入有效
       → 把 traction / case study 變主軸
```

The fallback applies everywhere `AskUserQuestion` is mandated: Socratic rounds in Phase 1, MECE check pop-ups, Forced Assumption mode warnings, all phase-handoff approvals, the title-only read pop-up at Phase 3→4. **The Socratic loop runs regardless of host capabilities; only the rendering changes.**

If you're unsure whether the host supports `AskUserQuestion`, try the tool once. If it errors or returns a not-available signal, switch to inline numbered choices for the rest of the session.

---

### Every phase handoff requires explicit user approval

Producing the checkpoint file is **not enough** to advance. After each phase's output file is written, you **MUST ask the user via `AskUserQuestion` whether to continue to the next phase**. No silent transitions. No "let me just keep going while I'm on a roll". The user needs the chance to fix things cheaply, *before* the next phase's effort is spent.

The handoff pop-up template:

```
Question: Phase <N> 完成（產出 <filename>）。要繼續進入 Phase <N+1> <name> 嗎？

  ○ 繼續進入 Phase <N+1> (Recommended)
       → <一句話描述下個 phase 要做什麼>
  ○ 我要先修改 Phase <N> 的內容
       → 告訴我哪裡要改，改完再回到這個 checkpoint
  ○ 暫停在這裡
       → 所有檔案都已存到 working directory，之後可以再回來繼續
```

Rules for the handoff pop-up:

1. **One pop-up per phase boundary.** Don't ask multiple questions at the handoff — that's for inside Phase 1's Socratic loop. The handoff itself is a single yes/revise/stop choice.
2. **Wait for the answer before doing any work on the next phase.** Reading the next phase's prompt file is fine; producing the next phase's output is not.
3. **If the user picks "我要先修改"**, ask one follow-up pop-up about what specifically to change, then iterate on the current phase's output file. After the revision, ask the handoff question again.
4. **If the user picks "暫停"**, summarize what files exist in the working directory and how to resume. Do not produce the next file.
5. **Phase 5 doesn't have a "next phase"** — its handoff question is the mandatory delivery step (Step 4 of the Phase 5 checklist below), where you tell the user every produced file and attach them all.

Approval is per-phase, not blanket. A user saying "go ahead" at the Phase 1→2 handoff does **not** authorize Phase 2→3 to proceed silently. Each boundary asks fresh.

---

### Phase 1 — Socratic Clarification Loop

Not a questionnaire. A loop that derives questions from the user's actual input, asks 1–3 high-leverage pop-up questions per round (via `AskUserQuestion`), and stops when the deck's thesis is "clear enough" to architect. See [prompts/01_needs_research.md](prompts/01_needs_research.md) for the full recipe and [references/socratic_loop.md](references/socratic_loop.md) for the reference taxonomy.

**Mandatory behavior:**

- **Use `AskUserQuestion` (pop-up choice) as the default question format.** 2–4 mutually-exclusive options per question. Each option label ≤ 5 words; description explains the *trade-off*, not the definition. Free-text inline only when no honest options exist.
- **Detect the scenario early** (fundraising / sales / internal sync / executive briefing / educational / strategy review / annual review / product launch / keynote / training / crisis comms). Each scenario needs a different spine surfaced — pop-up question them on which one fits if it isn't obvious.
- **Pick one question type per round** from: Definition / Consequence / Evidence / Objection / Tradeoff / Compression. Don't mix.
- **Max 3 questions per round, max 4 rounds.** After round 4, switch to **Forced Assumption mode** (distinct from user-chosen Quick mode) — document remaining unknowns in `brief.md` → `open_assumptions[]`, flag best-guess fields with `⚠️`, and surface them prominently in the Phase 1→2 handoff pop-up. See `prompts/01_needs_research.md` for the full procedure.
- **Tone is consultant, not interrogator.** Lead with "I currently understand…" / "There's a trade-off here…" — never "You contradicted yourself."

**Quick mode (opt-in only, never auto-switched)**: if the user shows impatience signals ("fast" / "quick" / "just do it" / "I gave you everything"), **do not auto-switch** — ask them via `AskUserQuestion` whether they want Quick mode or to stay in the full Socratic loop. Only switch if they explicitly pick it. Quick mode then asks **one** pop-up question (about the single highest-leverage gap) and proceeds with explicit assumptions written into `brief.md`. Quick mode reduces interview length; it does **not** skip Phase 1, the `brief.md` file checkpoint, or the Phase 1→2 handoff approval. The dialogue is the value DeckForge provides — auto-switching to Quick mode bypasses the product.

**Output checkpoint**: write `brief.md` to the working directory. Required fields: `scenario`, `audience.who`, `audience.current_belief`, `belief_shift.from/to`, `core_thesis`, `proof_pillars[]`, `likely_objections[]`, `desired_action`, `constraints`, `open_assumptions[]`. Schema and examples are in `prompts/01_needs_research.md`. Phase 2 must `Read brief.md` as its first action.

If the user has uploaded reference material, Phase 0 runs first and produces `analysis.md`; Phase 1 then runs with `analysis.md` as context (but `brief.md` is still produced — Phase 0 does **not** bypass Phase 1).

**Handoff checkpoint**: after writing `brief.md`, ask the user via `AskUserQuestion` whether to continue to Phase 2. Do not begin Phase 2 until they approve. (See "Every phase handoff requires explicit user approval" above.)

### Phase 2 — Outline architecture (大綱規劃)

Use the **金字塔原理 (pyramid principle)** + 便利貼法 ("sticky-note method"): each page is one digital sticky note. Logic first, design later.

Pyramid principle is one of DeckForge's two load-bearing methodologies (alongside Bento Grid). It runs end-to-end: `brief.md`'s `core_thesis` + `proof_pillars` (Phase 1, with MECE check), `outline.json` part/page titles (Phase 2), and `planning.json` cards that must defend each page's title-claim (Phase 3). See [references/pyramid_principle.md](references/pyramid_principle.md) for the cross-phase map.

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

Save the outline to `outline.json` in the working directory.

**Handoff checkpoint**: after writing `outline.json`, show it to the user (digital sticky notes — easy to add/remove/reorder before any design work happens) and ask via `AskUserQuestion` whether to continue to Phase 3. Do not begin Phase 3 until they approve.

### Phase 3 — Planning draft (策劃稿) — DO NOT SKIP

This is what most AI PPT tools miss. Before any design, decide for **each page**:
- What concrete content goes there (bullets, stats, quotes, charts — actual words, not placeholders)
- Which layout fits — **bento-first**: try a Bento Grid layout first (see [references/bento_grid.md](references/bento_grid.md)). Only switch to a diagram primitive when the bento attempt would lose structural information the audience needs (see [references/diagrams.md](references/diagrams.md))
- What visual elements are needed (icons, images, charts, no-element)
- Speaker notes (1–2 sentences per page)

Use the prompt in [prompts/04_planning_draft.md](prompts/04_planning_draft.md). Output goes to `planning.json`. Layout enum is:

```
"layout":
  // Bento Grid card layouts (default — try these first):
  "single_focus" | "stat_hero" | "mini_grid" | "two_col_50_50" |
  "two_col_2_1" | "three_col" | "hero_top" | "mixed_grid"
  // Chart layouts (use chart_data instead of cards):
  | "chart_bar" | "chart_line" | "chart_donut"
  // Diagram primitives (use only when bento loses information —
  // direction / alignment / topology / axis loss; see references/diagrams.md):
  | "flow" | "timeline" | "cycle" | "funnel"
  | "compare_table"
  | "hierarchy_tree" | "pyramid"
  | "quadrant_2x2" | "venn"
```

**Bento card page** — uses `cards: []`. Each card supports `is_number_first`, `stat_value`/`stat_caption`/`stat_caption_en`, `heading`/`body`/`icon_hint`/`size_hint`. **Optional `sub_cards: []`** can nest 2–3 mini-cards inside a hero card, but only on layouts with a tall hero region — `single_focus`, `two_col_2_1` (wide slot), or `mixed_grid` (big slot). **Not** allowed on `mini_grid`, `three_col`, or `hero_top` (these layouts don't have enough vertical room).

Mini_grid example (parallel KPIs, no nesting):

```json
{
  "page_id": 7,
  "page_type": "content",
  "layout": "mini_grid",
  "title": "AIoT 戰略推動營收三年翻倍",
  "title_en": "AIoT Drives 2× Revenue in Three Years",
  "cards": [
    { "is_number_first": true, "stat_value": "42%",     "stat_caption": "三年複合成長率", "stat_caption_en": "CAGR" },
    { "is_number_first": true, "stat_value": "NT$510億", "stat_caption": "2025 年總營收" },
    { "is_number_first": true, "stat_value": "+45%",    "stat_caption": "AIoT 業務年增" },
    { "is_number_first": true, "stat_value": "26%",     "stat_caption": "毛利率 (由 18%)" }
  ],
  "visual_notes": "Highlight color = #FF6900. 4 parallel KPIs, mini_grid 4-card geometry.",
  "speaker_notes": "..."
}
```

Single_focus + nested sub_cards example (claim + supporting evidence on one page):

```json
{
  "page_id": 12,
  "page_type": "content",
  "layout": "single_focus",
  "title": "服務優先戰略已交出三組關鍵指標",
  "title_en": "The Services-First Strategy: Three Proof Points",
  "cards": [
    {
      "is_number_first": false,
      "heading": "從硬體製造商轉型生態服務商",
      "body": "三年累計營收 NT$180億 → NT$365億,服務佔比躍升至 27%",
      "icon_hint": "trending-up",
      "sub_cards": [
        { "is_number_first": true, "stat_value": "+103%", "stat_caption": "三年累計增長", "stat_caption_en": "3Y Growth" },
        { "is_number_first": true, "stat_value": "27%",   "stat_caption": "AIoT 業務佔比" },
        { "is_number_first": true, "stat_value": "+45%",  "stat_caption": "AIoT 年增" }
      ]
    }
  ],
  "visual_notes": "Single hero card with 3 nested sub-cards as quantitative evidence.",
  "speaker_notes": "..."
}
```

**Chart page** — uses `chart_data: {...}` *instead* of `cards`:

```json
{
  "page_id": 8,
  "page_type": "content",
  "layout": "chart_bar",
  "title": "各業務板塊毛利率",
  "title_en": "Gross Margin by Business Segment",
  "chart_data": {
    "unit": "%",
    "items": [
      { "label": "智慧家居", "label_en": "SMART HOME", "value": 42 },
      { "label": "電動車", "label_en": "EV", "value": 75 },
      { "label": "服務", "label_en": "SERVICES", "value": 50 }
    ]
  },
  "visual_notes": "Single highlight color, no per-bar palette.",
  "speaker_notes": "..."
}
```

`chart_line` uses time-point labels; `chart_donut` items are composition segments (first item full saturation, others fade with alpha 0.55/0.25/0.12 of the same hue). See `prompts/04_planning_draft.md` for the full schema and `references/chart_anatomy.md` for the SVG geometry.

Why this phase exists: top PPT agencies have a **Planner** role separate from the **Designer**. The Planner decides what + where; the Designer decides how it looks. Mixing these jobs produces the busy, cluttered slides that scream "AI generated".

**Handoff checkpoint**: after writing `planning.json`, show it to the user — this is the highest-leverage review point in the whole workflow, because design effort hasn't started yet. The handoff pop-up **must include the title-only read** (all part_titles + page titles in sequence) so the user can confirm the pyramid argument reads top-down before any rendering happens. Do not begin Phase 4 until they approve. Fixing the content plan here is cheap; fixing it after 15 SVG pages have been rendered is expensive.

### Phase 4 — Design (設計稿)

For each page in `planning.json`, generate **one self-contained SVG file** with `viewBox="0 0 1280 720"`, styled with the Bento Grid system.

- Master prompt: [prompts/05_designer_svg.md](prompts/05_designer_svg.md)
- Bento Grid spec (base layout family): [references/bento_grid.md](references/bento_grid.md)
- Diagram primitives spec (information-loss layouts): [references/diagrams.md](references/diagrams.md)
- Chart anatomy: [references/chart_anatomy.md](references/chart_anatomy.md)
- Color + typography system: [references/design_system.md](references/design_system.md)
- SVG templates to start from: [templates/](templates/) — 20 files total:
  - **Shared assets**: `_base.svg` (filters / gradients / 35 Lucide icons used via `<use>`)
  - **Page-type starters**: `cover.svg`, `toc.svg`
  - **Bento layouts**: `bento_2col.svg` (two_col_50_50 / two_col_2_1), `bento_3col.svg`, `bento_hero.svg` (hero_top), `bento_mixed.svg` (mixed_grid), `bento_mini_grid.svg` (mini_grid — main card + 3–5 mini-cards, dark_apple)
  - **Chart layouts**: `chart_bar.svg`, `chart_line.svg`, `chart_donut.svg`
  - **Diagram primitives** (used only when bento would lose structural information — see [references/diagrams.md](references/diagrams.md)): `flow.svg`, `timeline.svg`, `cycle.svg`, `funnel.svg`, `compare_table.svg`, `quadrant_2x2.svg`, `venn.svg`, `hierarchy_tree.svg`, `pyramid.svg`
  - **No dedicated template for**: `single_focus` (just use `bento_hero.svg` and drop the bottom row), `stat_hero` (single huge text, no template needed — see designer prompt geometry), `section_break` / `end` (derive from `cover.svg` with smaller hero text). These page types are simple enough that a template would add no value.

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

**Handoff checkpoint**: after all pages are written, ask the user via `AskUserQuestion` whether to continue to Phase 5 (Produce). If you can preview a few pages inline or attach a quick QA render, do — it makes the approval informed. Do not begin Phase 5 until they approve.

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

> **All recipes still run every phase and produce every checkpoint file.** What changes is how long each phase takes, not whether it runs.

### Recipe A — Full enterprise deck (45 min)

User: "Make me an investor pitch deck for our SaaS product."

1. **Phase 1** (Socratic): 2–3 rounds, ~6 pop-up questions total. Detect scenario = fundraising, then ask about belief shift, traction stat, ask amount, and the strongest objection. Write `brief.md`.
2. **Phase 2**: Read `brief.md`. Generate `outline.json` (probably 12–18 pages). Show to user for sign-off.
3. **Phase 3**: Read `outline.json`. Generate `planning.json`. Show to user for sign-off.
4. **Phase 4**: Read `planning.json`. Render all pages with the dark_apple palette (or brand override).
5. **Phase 5**: Read `pages/`. Produce `pitch.pptx` + `pitch.pdf` + (if any notes) `pitch.notes.md`. Deliver all files.
6. QA loop.

### Recipe B — Quick short deck (10 min)

User: "Quick deck on the Q4 results, 5 slides, internal team."

1. **Phase 1 Quick mode**: one pop-up question (typical: "which audience: full team / leadership only / mixed?"), then write `brief.md` with explicit assumptions for everything else.
2. **Phase 2**: Read `brief.md`. Generate `outline.json` (5 pages, short).
3. **Phase 3**: Read `outline.json`. Generate `planning.json` quickly — for a 5-page deck this is fast but **still produced as a file**.
4. **Phase 4**: render.
5. **Phase 5**: produce + deliver all files.
6. QA: one quick pass.

Skipping any phase here would actually save no time — `brief.md`, `outline.json`, `planning.json` for a 5-page deck are each a handful of seconds. What you skip is *rounds* and *sign-offs*, not phases.

### Recipe C — User has a source document

User: "I have this Word doc, turn it into slides."

1. **Phase 0** (Source analysis): read the doc, produce `analysis.md` with metrics, parallel sets, anomalies.
2. **Phase 1** (Socratic, mandatory): first round usually a scenario / audience pop-up because the doc doesn't dictate that. Then 1–2 follow-up Socratic rounds. Write `brief.md`. *Phase 0 does not bypass Phase 1.*
3. **Phase 2**: Read `brief.md` + `analysis.md`. Generate `outline.json` grounded in the document's actual numbers and parallel sets.
4. **Phase 3** onward: as usual.

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
│   ├── bento_grid.md                 ← Bento Grid layout system (8 layouts — the default)
│   ├── diagrams.md                   ← 9 diagram primitives — used only when bento loses information
│   ├── chart_anatomy.md              ← SVG bar / line / donut charts
│   ├── design_system.md              ← palettes, typography, motifs
│   ├── pyramid_principle.md          ← 金字塔原理 quick guide
│   ├── socratic_loop.md              ← Phase 1 reference: question types + scenario taxonomy
│   └── editable_mode.md              ← how Convert-to-Shape works in PowerPoint
├── templates/                         ← SVG starting points (viewBox 0 0 1280 720)
│   ├── _base.svg                     ← shared filters / gradients / 35 Lucide icons
│   ├── cover.svg
│   ├── toc.svg
│   ├── bento_2col.svg                ← 50/50 or 2:1 (switch widths)
│   ├── bento_3col.svg
│   ├── bento_hero.svg
│   ├── bento_mini_grid.svg           ← main card with 3–5 mini-cards (dark_apple)
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
