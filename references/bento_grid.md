# Bento Grid Layout System

The Bento Grid (便當網格) is a flexible card-based layout system, originally inspired by Japanese bento boxes and popularized by Apple's product pages. It's the **base** layout language for content pages — used by default unless a page genuinely needs to express direction / alignment / topology / axis structure that bento would flatten, in which case Phase 3 switches to a diagram primitive (see [diagrams.md](diagrams.md)).

**Styling note**: the coordinates in this document are style-agnostic; the example fills are dark_apple (`#1A1A1A` / `#222222` cards on black). On `IT_prism` decks (the default style), keep the geometry but render cards as white rx=14 with the whisper shadow on the `#EFF0F3` canvas, per design_system.md → "IT prism family"; on `corporate_fresh` decks, white rx=14–16 on the `#F4F4F4` canvas per "Corporate fresh family".

Why Bento Grid?

1. **It holds a lot of info on one page** without feeling stuffed.
2. **Card count and size are flexible** — the Bento system as a whole can carry 6+ items across the deck via multiple layouts (mini_grid + hero_top + mixed_grid, etc.). **However, a single `mini_grid` layout caps at 5 cards** — 6+ goes to two `mini_grid` pages, or gets promoted to `hero_top` (1 hero + 4 supporting).
3. **It's easy for AI to design well.** Card boundaries give structure that prevents the "everything floating in space" failure mode.
4. **Size = importance** is intuitive for viewers.

## Core principles

| Principle | Rule |
|---|---|
| **Flexibility** | Card count is not fixed. Pick the count that best holds the content. |
| **Hierarchy** | The biggest card holds the most important info. Use size to express priority. |
| **Whitespace** | ≥20px gap between cards. ≥48px page outer margin. Don't fill every pixel. |
| **One motif** | Pick one card style (rounded corners + shadow, accent bar, etc.) and reuse on every page. |

---

## The eight layouts

In addition to the six base layouts, there are two patterns designed specifically for the dark_apple aesthetic that come from the linux.do "Xiaomi annual report" methodology:

- `stat_hero` — a single huge number dominates the slide.
- `mini_grid` — a main card containing a **3–5-column** grid of mini-cards. Each mini-card holds **one core point only**. (6+ cards is too dense — split into two pages.)

These two patterns are where the visual quality jump comes from. Use them whenever the content is data-dense (annual reports, financials, product specs, comparisons).



### 1. `single_focus` — one big card

```
+------------------------------------------+
|                                          |
|                                          |
|              [ one card ]                |
|                                          |
|                                          |
+------------------------------------------+
```

Card dimensions: ~1200×580 (full canvas minus margins).

**Use when**: one headline stat, one quote, one chart, one hero claim.

**Don't use when**: you have 2+ ideas of similar weight (use 2-col instead).

---

### 2. `two_col_50_50` — equal halves

```
+-----------------+  +----------------+
|                 |  |                |
|   [ card A ]    |  |  [ card B ]    |
|                 |  |                |
+-----------------+  +----------------+
```

**Use when**: before/after, pros/cons, two parallel ideas, side-by-side comparison.

**Light families (IT_prism / corporate_fresh)**: this layout is a per-page `card_variant` family — `balanced` (two co-equal ideas) / `before_after` (a transformation); triggers + geometry per design_system.md → "two_col_50_50 card_variant" (prism uses the `prism_2col*` templates).

---

### 3. `two_col_2_1` — asymmetric

```
+------------------------------+ +------------+
|                              | |            |
|       [ card A — big ]       | | [ card B ] |
|                              | |            |
+------------------------------+ +------------+
```

Wide card ~2/3, narrow ~1/3.

**Use when**: one main idea + one supporting detail (a sidebar, a stat callout, an image).

---

### 4. `three_col` — three equal columns

```
+----------+  +----------+  +----------+
|          |  |          |  |          |
| [card A] |  | [card B] |  | [card C] |
|          |  |          |  |          |
+----------+  +----------+  +----------+
```

**Use when**: three parallel pillars (values, steps, features, comparisons).

**Don't use when**: only 2 items (looks lonely) or 4+ (use mixed_grid).

**Light families (IT_prism / corporate_fresh)**: this layout is a per-page `card_variant` family — `icon_column` / `numbered_steps` / `axis_labeled` / `lead_plus_pair`; triggers + geometry per design_system.md → "three_col card_variant" (prism uses the `prism_3col*` templates).

---

### 5. `hero_top` — hero + grid below

```
+------------------------------------------+
|              [ hero card ]               |
+------------------------------------------+
+--------+  +--------+  +--------+  +-----+
| card B |  | card C |  | card D |  |  E  |
+--------+  +--------+  +--------+  +-----+
```

Top card spans full width. Below, 2–4 smaller equal-width cards.

**Use when**: one headline claim + 2–4 supporting details / stats / steps.

---

### 6. `mixed_grid` — asymmetric freeform

```
+----------+  +----------+----------+
|          |  |          |          |
| [ big A ]|  | [ med B ]| [ med C ]|
|          |  +----------+----------+
|          |  |       [ wide D ]   |
+----------+  +-----------+--------+
```

Combine sizes freely. Most flexibility, most design judgment required.

**Use when**: 4–6 items of varying importance.

**Caution**: easiest layout to overdo. If you have to think hard about it, use one of the simpler layouts.

---

### 7. `stat_hero` — one giant number takes the page

```
+------------------------------------------+
|  Page title                              |
|                                          |
|                                          |
|             142.5%                       |
|                                          |
|             同比增長 · YoY Growth          |
|                                          |
|                                          |
+------------------------------------------+
```

A single statistic dominates. The number is rendered at **80–120px font-size, font-weight 900**, in the highlight color. Below, a short caption (Chinese 16–18px + optional English subtitle 12–14px) explains what the number means.

**Use when**: a single number is the headline. Quarterly growth, market share, ARR, downloads, customers — anywhere "the number is the message".

**Don't use when**: 2+ stats compete for attention (use `mini_grid` instead).

**SVG geometry**:
- Page title: standard header band (y=48..120)
- Big number: centered around `(640, 380)`, font-size 100, anchored mid
- Caption (CN): centered at `(640, 450)`, font-size 18
- Caption (EN, optional): centered at `(640, 475)`, font-size 13, gray-500

---

### 8. `mini_grid` — main card containing a grid of mini-cards

```
+------------------------------------------+
|  Page title                              |
|                                          |
|  +--------------------------------------+|
|  |  Main card                           ||
|  |                                      ||
|  |  +-----+ +-----+ +-----+ +-----+    ||
|  |  | 42% | | 15M | | #1  | | 3.2 |    ||
|  |  | 增長  | | 用戶  | | 排名  | | 億   |    ||
|  |  +-----+ +-----+ +-----+ +-----+    ||
|  |                                      ||
|  +--------------------------------------+|
|                                          |
+------------------------------------------+
```

A main card holds **3–5 mini-cards** in a horizontal grid. Each mini-card carries **exactly one core point** (one number + one caption, or one short text-title + one caption). Each mini-card is its own discrete visual unit. This is the linux.do "Xiaomi report" pattern — and where data-dense content really sings.

**Use when**:
- 3–5 parallel stats / features / risks / steps that you want to feel like a coherent set
- An annual-report-style "key metrics" page
- Side-by-side comparison where each comparison item is short

**Don't use when**:
- 1–2 items (waste of structure — use single_focus or two_col)
- **6+ items** — too dense, mini-cards become cramped (≤190px wide). Split into two `mini_grid` pages with 3–4 cards each, OR promote 1–2 items to a `hero_top` layout with the rest as supports.
- Items are unequal in importance (the grid implies equality — use mixed_grid for unequal weight)

**SVG geometry**:
- Page title: standard header band (y=48..120)
- Main card: `x=48, y=140, w=1184, h=532, rx=20`, fill `#1A1A1A`, stroke `#333333`
- Mini-cards: arranged in a row inside the main card, with 24px gap. For 4 mini-cards:
  - Each `w = (1184 - 80 main-card padding - 3×24 gap) / 4 ≈ 257`
  - `h ≈ 360` (centered vertically inside main card)
  - Positions: x = 88, 369, 650, 931 (= 48 + 40 main-pad + i × (257 + 24))
  - `rx=12` (smaller than main card's 20)
- See `templates/bento_mini_grid.svg` for the ready-made starter.
- **Light families (IT_prism / corporate_fresh)**: `mini_grid` is a per-page `card_variant` family — `even_grid` / `ribbon_row` / `spotlight`; triggers + geometry per design_system.md → "mini_grid card_variant" (the KPI starters there are `templates/prism_mini_grid.svg` / `templates/fresh_mini_grid.svg`, not the dark_apple file above).

**Mini-card content rules** (this is the secret):
- Each mini-card: ONE big element on top, ONE supporting caption below.
- Big element = either a huge number (80–96px, highlight color) OR a 3–5 character Chinese phrase (32–40px, white or highlight).
- Caption = 16–18px gray-400, 1–2 short lines, no commas-breaking-sentences.
- Optional bilingual subtitle: 12–14px gray-500 English phrase ("YoY Growth", "Total Revenue"). Apply selectively, not on every card.
- **Never two long sentences on one mini-card** (presenting mode). If you can't fit it short, the content isn't extracted enough — go back to the planner.
- **Reading mode** (page's effective `delivery_mode` is `reading`): a mini-card may carry one claim + up to two supporting sentences — but only if the geometry gives every line ≥16px (the reading floor) at a sane measure. A 200px-wide 5-up mini-card cannot; prefer 3–4 cards (wider), or the `ribbon_row` variant, whose full-width rows are the natural slidedoc shape for a metric + its explanation.

---

## Quality over quantity — empty slots are a feature

A common visual mistake is padding a layout to fill every position. **A 4-card `mini_grid` with strong cards reads better than a 5-card `mini_grid` where the 5th is filler.**

Rule:
- If 5 candidates exist but only 3–4 truly defend the page claim → use 3-card or 4-card geometry. The cards get wider, the breathing room increases, and the deck reads more confident.
- The planner controls this — Phase 3 outputs the right number of cards, the designer just follows.
- **Never** render 5-card geometry with one slot left blank — that reads as "we forgot one", not "we chose four". The empty slot signals an error to the viewer.

Exception: if the slot count is **narratively meaningful** (5 quarters, 5 named pillars, 5 regions), keep all 5 even if one card is weaker — sequence integrity beats per-card strength.

The same principle applies to `three_col`: don't force a 3rd column to fill space. Two genuinely strong items go to `two_col_50_50`.

---

## Nested sub-cards — sub-grids inside any large card

Any **large** card on a whitelisted layout (`single_focus`, `two_col_2_1` wide slot, or `mixed_grid` big slot) may optionally contain a **2–3 mini-card sub-grid** via the planning schema's `sub_cards: []` field. This lets a hero claim carry quantitative evidence inline, without spending a separate page.

**Excluded layouts**: `hero_top` (240px hero too short to fit heading + body + sub-cards without overflow), `mini_grid`, `three_col` (cards too narrow). On these, use a separate page or move the evidence to `speaker_notes` (presenting decks; on a reading page evidence never lives only in speaker notes — use a separate page or the `reading_notes` strip).

```
+------------------------------------------+
|  Page title                              |
|                                          |
|  +------------------------------------+  |
|  | Hero card                          |  |
|  |                                    |  |
|  |   "從硬體製造商轉型生態服務商"           |  |
|  |   subtitle / body line              |  |
|  |                                    |  |
|  |   +------+ +------+ +------+       |  |
|  |   |+103% | | 27%  | |+45%  |       |  |
|  |   |三年增 | |佔比   | |AIoT增 |     |  |
|  |   +------+ +------+ +------+       |  |
|  +------------------------------------+  |
|                                          |
+------------------------------------------+
```

**Geometry (sub-cards inside a hero card)**:
- Sub-cards sit in the **bottom half** of the parent card.
- For a hero with inner area `W × H`, sub-cards take `W × ~140px` at the bottom (leaving the upper area for the parent's heading + body).
- 2 sub-cards: each `(W - gap) / 2` wide. 3 sub-cards: each `(W - 2×gap) / 3` wide.
- Gap between sub-cards: `20–24px`.
- Sub-card `rx = 10` (smaller than standalone mini-cards' `rx=12`, smaller still than main cards' `rx=20`).
- Sub-card fill: `#222222`, same as standalone mini-cards.
- Sub-card height: ~120–140px (shorter than standalone 360px mini-cards).

**Typography inside sub-cards**:
- Big element: 40–56px font-weight 900 (smaller than standalone mini-card 56–72px, because the sub-card is shorter).
- Caption: 12–13px gray-400.
- EN subtitle (optional): 10–11px gray-500. Apply to ~50–70% of sub-cards for rhythm.

**Rule of thumb**: never exceed 3 sub-cards in one parent card. If you need 4+, the page should be a `mini_grid` page instead, with the parent's claim becoming the page title.

---

## stat_hero — subtle highlight-color glow behind the number

A `stat_hero` slide can optionally place a **very subtle radial glow** behind the giant number to make it feel like it's lit from within. This is single-highlight-color discipline (same color as the number, just alpha gradient) — it does **not** introduce a second color.

```xml
<defs>
  <radialGradient id="statHeroGlow" cx="50%" cy="50%" r="50%">
    <stop offset="0%"   stop-color="<highlight>" stop-opacity="0.10"/>
    <stop offset="60%"  stop-color="<highlight>" stop-opacity="0.03"/>
    <stop offset="100%" stop-color="<highlight>" stop-opacity="0"/>
  </radialGradient>
</defs>

<!-- Glow rectangle, centered behind the number -->
<rect x="240" y="240" width="800" height="280" fill="url(#statHeroGlow)"/>

<!-- Giant number, on top of the glow -->
<text x="640" y="400" font-size="120" font-weight="900"
      fill="<highlight>" text-anchor="middle">142.5%</text>
```

The glow's max alpha is **0.10** — easily missed at a glance, which is the point. It's a polish layer, not a foreground element. If the glow is so visible that it competes with the number, dial it back to 0.06.

---

## Bento Grid 1-card-1-point discipline

This rule applies to ALL layouts, but mini-cards in particular:

> **One card, one point — mode-scaled.**
> **Presenting**: one big element + one short caption. If it can't fit, the planner hasn't extracted it correctly. Don't cram. Split.
> **Reading** (effective `delivery_mode: reading`): one card, one **argument** — one claim line plus the 2–4 sentences that complete it. The unit of splitting is still one: a card carrying *two claims* is exactly as broken as a presenting card carrying two points.

Symptoms of bad extraction (presenting):
- Card has 3+ bullets inside.
- Card has 2 paragraphs.
- Card heading and body talk about different things.
- Card has commas like ", "、" or "、" breaking what should have been separate cards.

In reading mode the symptoms move up a level: two claim lines in one card, a heading and a body that argue different things, 「另外」/「此外」 splicing a second argument on — split the card, not the sentence count.

When you see these symptoms, **rewrite the planning** to split that one card into multiple mini-cards.

## SVG card coordinates

All templates assume a `viewBox="0 0 1280 720"` canvas with **48px outer margin** and **20px gaps** between cards. Inner working area is therefore `1184 × 624` (or smaller after a header band).

Standard header band: title at `y=92` (font-size 40), subtitle at `y=124` (font-size 18). Bento area starts at `y=140` and ends at `y=672` (height = 532).

| Layout | Card rects (`x, y, w, h`) |
|---|---|
| `single_focus` | A: `48, 140, 1184, 532` |
| `two_col_50_50` | A: `48, 140, 582, 532` · B: `650, 140, 582, 532` |
| `two_col_2_1` | A: `48, 140, 775, 532` · B: `843, 140, 389, 532` |
| `three_col` | A: `48, 140, 381, 532` · B: `449, 140, 381, 532` · C: `850, 140, 381, 532` |
| `hero_top` | Hero: `48, 140, 1184, 240` · 4 support: `48 / 349 / 650 / 951, y=400, w=281, h=272` |
| `mixed_grid` | Free placement; the `bento_mixed.svg` template uses Big-left `48, 140, 582, 532` · Top-right `650, 140, 582, 256` · Bottom-right `650, 416, 582, 256` |

### Common SVG card pattern

```xml
<defs>
  <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur in="SourceAlpha" stdDeviation="12"/>
    <feOffset dx="0" dy="8"/>
    <feComponentTransfer><feFuncA type="linear" slope="0.06"/></feComponentTransfer>
    <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>

<!-- Card body: rounded rect with shadow -->
<rect x="48" y="140" width="582" height="532" rx="16" ry="16"
      fill="#FFFFFF" filter="url(#cardShadow)"/>

<!-- Card heading (in primary color) -->
<text x="80" y="200" font-size="22" font-weight="700" fill="#1E2761">卡片標題</text>

<!-- Card body text — manually wrap with <tspan> rows -->
<text x="80" y="240" font-size="15" fill="#1A1A2E">
  <tspan x="80" dy="0">第一行說明文字。</tspan>
  <tspan x="80" dy="1.55em">第二行繼續說明。</tspan>
</text>
```

The starter templates in `templates/` already include this skeleton plus the motif variants below.

### Typography sizes on the 1280×720 canvas

| Element | Size | Weight |
|---|---|---|
| Slide title | 36–48 | 700–800 |
| Subtitle | 18–22 | 400, opacity 0.7 |
| Card heading | 20–28 | 700 |
| Card body | 14–18 | 400, dy 1.55em between lines |
| Big stat (single number) | 56–96 | 800–900 |
| Caption | 11–13 | 400, opacity 0.6 |

Reading-mode pages floor every size at **16px** (the 12pt reading floor — captions rise to 16, the "quiet" is carried by color/opacity, not size); delta table in `references/design_system.md` → "Delivery mode — reading".

---

## When NOT to use a Bento Grid

- **Cover page**: hero text + bg. Skip the grid.
- **Section break**: huge title + tiny subtitle. Skip the grid.
- **Quote page**: a single oversized quote can use `single_focus` or just centered text.
- **End page**: simple "thank you" + contact. Skip the grid.

For these page types, use `single_focus` or no grid at all — see the templates folder.
