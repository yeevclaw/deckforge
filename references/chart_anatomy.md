# Chart Anatomy — SVG charts for data-heavy slides

Cards with numbers are great for hero stats. But when numbers **relate to each other** — a trend, a composition, a ranking, a bridge from A to B — a chart communicates the relationship faster than any grid of mini-cards. This reference shows how to draw the ten chart types DeckForge supports directly as SVG primitives — no external libraries, fully editable in PowerPoint after Convert to Shape:

- **Basic three**: `chart_bar` (category comparison), `chart_line` (trend), `chart_donut` (composition of a whole)
- **Consulting five** (the think-cell-style vocabulary): `chart_hbar` (ranking), `chart_stacked_bar` (composition across categories/time), `chart_waterfall` (A→B bridge), `chart_combo` (volume + rate), `chart_mekko` (two-dimensional market map)
- **Two specialized**: `chart_radar` (multi-axis assessment profile — one entity rated across 3–8 criteria), `chart_gantt` (project schedule / roadmap — task durations across a time grid)

What separates a consulting-grade chart from a default chart is not prettier geometry — it's that **the chart carries its own analysis**. The page title states a claim; the chart visually asserts that claim with an analytical mark: a CAGR arrow, a difference bracket, a reference line, an emphasized segment. See [Annotation layer](#annotation-layer--圖表自帶分析) below. A bare data dump under an assertion title is a half-finished chart.

## When to use a chart vs cards — the relationship test

> **Numbers that relate to each other get a chart. Only independently meaningful, parallel numbers get cards.**

Ask of any group of numbers on a page: does the *relationship between them* carry the message (change over time, share of a whole, gap between items, cause of a delta)? If yes, splitting them into cards destroys exactly the information the audience needs — chart it. If each number stands alone (four unrelated KPIs), cards remain the stronger, more flexible form.

| Data shape | Best representation |
|---|---|
| 3–5 parallel numbers, each **independently** meaningful | `mini_grid` (cards) |
| 1 dominant number | `stat_hero` (card) |
| **Trend over time** (4+ time points) | **`chart_line`** |
| **Comparison across categories** (4+ items) | **`chart_bar`** |
| **Ranking / long category labels** ("who leads") | **`chart_hbar`** |
| **Composition** (parts of one whole) | **`chart_donut`** |
| **Composition across categories or time** (mix shift, 結構變化) | **`chart_stacked_bar`** |
| **Bridge / build-up** (what explains the change from A to B) | **`chart_waterfall`** |
| **Two coupled metrics** (volume + rate: 營收+毛利率, users + churn) | **`chart_combo`** |
| **Two-dimensional share map** (segment size × player share) | **`chart_mekko`** |
| **Multi-axis assessment** — one entity rated across 3–8 criteria (or 2–3 profiles overlaid) | **`chart_radar`** |
| **Project schedule** — task durations across a time grid (start/end per workstream) | **`chart_gantt`** |
| Single proportion (1 vs total) | `stat_hero` with percent, or `chart_donut` with 1 segment |
| 2 items contrasting | `two_col_50_50` cards |

The old heuristic "if you can fit it in cards, prefer cards" applies **only after** the relationship test says the numbers are independent. A mix shift written as three cards ("8% → 27%…") passes the fit test and still fails the audience — the *shift* is the message, and only a chart shows it.

## Common rules (all charts)

- **Single highlight color discipline.** All foreground/data fill uses the deck's `highlight_color`. No multi-color palettes inside the chart. Multiple data series / segments? Use varying alpha (`1.0`, `0.45`, `0.18`) of the same hue, with the **story-bearing series at full saturation** (the `emphasis` field, or the first series when unset). One hue, many weights — the chart stays on-palette and the emphasis does the arguing.
- **Two visual voices: data in color, analysis in ink.** Data marks (bars, segments, lines, dots) speak in the highlight hue. Analytical marks (annotation arrows, difference brackets, reference lines, totals, connectors) speak in the neutral ink stack — `#FFFFFF`/`#CCCCCC` on dark, `#383838` on light. The reader learns to parse the two layers instantly: color = what happened, ink = so what.
- **Negative / decrease values are neutral gray, never red.** Waterfall decreases, declining deltas: `#6E6E73` on dark, `#AEB4BA` on light. A red would be a second accent — the single-color invariant outranks the red-means-down convention, and gray-means-down reads fine once the deck is consistent.
- **Bars start at zero. Always.** A truncated value axis exaggerates differences — consulting-grade means the geometry never lies. If one bar dwarfs the rest so much that labels choke, break *that bar* with an axis-break squiggle (two parallel tilted lines interrupting the bar, value label intact) — or rethink the chart.
- **Background**: same dark gray card (`#1A1A1A`) or pure black slide bg.
- **Axes / gridlines**: thin (1px) `#333333`. Subtle, not assertive. When every data point carries a direct value label, gridlines may be dropped entirely (keep the baseline) — labels beat grids.
- **Labels**: `#A0A0A0` 12–14px. Axis labels in English, data labels in CN.
- **`corporate_fresh` decks (on request)**: same geometry, swap the neutrals and the data hue — white card on `#F4F4F4` canvas, gridlines `#DDE2DF`, labels `#6B7178` (values `#383838`; **EN decorative sub-labels stay at `#6B7178` too — never a lighter tertiary gray, because on the white card anything lighter than ~`#757575` drops below WCAG AA 4.5:1; the 10px size + letter-spacing already makes the EN recede**), and the data series uses the family's **structure green `#3DB377`** with the same alpha tiers (donut segments: alphas of that green). Ink voice = `#383838`; decreases = `#AEB4BA`; totals = `#383838`. Orange `#E8872E` stays reserved for inline text emphasis — never as chart fill, and **not for chart annotation labels either**: orange on the white card is ≈2.65:1 and fails AA. On fresh charts every annotation label speaks ink `#383838` (bold for the claim-bearing one); orange keeps to its sanctioned role — bold inline runs inside body text.
- **`IT_prism` decks (the default style)**: same geometry — white card on the `#EFF0F3` canvas, gridlines `#DFE2E9`, labels `#6B7686` (values `#344252`; EN decorative sub-labels stay `#6B7686` — the same AA floor as fresh), data series in the family's **accent green `#58D494`** with the standard alpha tiers. Ink voice = `#344252`; decreases = `#AEB4BA`; totals = `#344252`. Chart fills are the one sanctioned large-area use of the accent green (data IS the pointing); green still never appears as a text fill — every value/annotation label speaks ink `#344252`, and no cover hue (lavender/cyan/indigo/sky) ever enters a chart.
- **Title sits OUTSIDE the chart**, as the page title. The chart itself has no internal title — the page title carries it.
- **Numbers on bars / points**: optional. If shown, render at 14–16px in highlight color, above each data point. Add `style="font-variant-numeric: tabular-nums"` so values align across bars/points and axis ticks.
- **Labels sitting ON a full-hue fill flip to near-black ink `#111111`.** White text on the highlight color fails WCAG AA (~2.6:1 on `#FF6900`, worse on the fresh green) — so in-segment/in-bar labels on a full-saturation fill use `#111111`, while light grays (`#E8E8E8` / `#C8C8C8`) stay on the low-alpha and dark-neutral fills. AA contrast outranks the ink-is-white convention.
- **Series labeling stays complete.** If a series' values are labeled, label *every* member: a segment too thin for an inside label (<24px) gets its value just outside with a 2–4px leader line (12px, muted gray) — never silently omit one value while its siblings are labeled, and never squeeze text into a segment that can't hold it.
- **Direct labels beat legends.** Single series: no legend ever. Multi-series lines: label each line at its right end, no legend. Stacked bars / mekko: series names sit left of the first column, aligned to each segment's mid-height. The legend proper (12px `#A0A0A0`, top-right) is the fallback for the cases direct labels can't serve — e.g. `chart_combo`'s two different-unit metrics.

## Chart canvas

A chart layout (any of the ten types) takes the full slide content area below the title:
- Chart area: `x=88, y=160, width=1104, height=480` (inside a 48-padding canvas)
- Plot area (inside axes): leave ~64px gutter for axis labels on left & bottom

**One chart per page.** Two-column charts (chart inside a `two_col_50_50` half) are **not supported** — the 510×480 area chokes both axes and labels. If you need two charts on the same topic, use two pages. See `prompts/04_planning_draft.md` for the planning-side rule.

---

## `chart_bar` — vertical bars for category comparisons

Use when comparing 4–10 categories on one metric. Examples: revenue by region, downloads by channel, customers by segment.

### SVG anatomy

```xml
<!-- Plot area, no fill, optional very faint grid lines -->
<g transform="translate(152, 200)">
  <!-- Y-axis labels (right-aligned at x=-12, every 25%) -->
  <text x="-12" y="0"   font-size="12" fill="#A0A0A0" text-anchor="end">100%</text>
  <text x="-12" y="100" font-size="12" fill="#A0A0A0" text-anchor="end">75%</text>
  <text x="-12" y="200" font-size="12" fill="#A0A0A0" text-anchor="end">50%</text>
  <text x="-12" y="300" font-size="12" fill="#A0A0A0" text-anchor="end">25%</text>
  <text x="-12" y="400" font-size="12" fill="#A0A0A0" text-anchor="end">0%</text>

  <!-- Horizontal gridlines (thin gray) -->
  <line x1="0" y1="0"   x2="1000" y2="0"   stroke="#333333" stroke-width="1"/>
  <line x1="0" y1="100" x2="1000" y2="100" stroke="#333333" stroke-width="1"/>
  <line x1="0" y1="200" x2="1000" y2="200" stroke="#333333" stroke-width="1"/>
  <line x1="0" y1="300" x2="1000" y2="300" stroke="#333333" stroke-width="1"/>

  <!-- Bars: 5 bars at x=0, 200, 400, 600, 800 (width 100 each, gap 100)
       y is plot-area top (0), height = data-value × scale, so bar grows DOWN from
       value to 400 (baseline). For a 42% bar: y=400-(42/100)*400=232, h=400-232=168 -->
  <rect x="0"   y="232" width="100" height="168" fill="#FF6900" rx="6"/>
  <rect x="200" y="160" width="100" height="240" fill="#FF6900" rx="6"/>
  <rect x="400" y="100" width="100" height="300" fill="#FF6900" rx="6"/>
  <rect x="600" y="280" width="100" height="120" fill="#FF6900" rx="6"/>
  <rect x="800" y="200" width="100" height="200" fill="#FF6900" rx="6"/>

  <!-- Value labels on top of each bar -->
  <text x="50"  y="220" font-size="14" font-weight="700" fill="#FF6900" text-anchor="middle">42%</text>
  <text x="250" y="148" font-size="14" font-weight="700" fill="#FF6900" text-anchor="middle">60%</text>
  <text x="450" y="88"  font-size="14" font-weight="700" fill="#FF6900" text-anchor="middle">75%</text>
  <text x="650" y="268" font-size="14" font-weight="700" fill="#FF6900" text-anchor="middle">30%</text>
  <text x="850" y="188" font-size="14" font-weight="700" fill="#FF6900" text-anchor="middle">50%</text>

  <!-- X-axis category labels -->
  <text x="50"  y="430" font-size="12" fill="#A0A0A0" text-anchor="middle">智慧家居</text>
  <text x="250" y="430" font-size="12" fill="#A0A0A0" text-anchor="middle">智慧穿戴</text>
  <text x="450" y="430" font-size="12" fill="#A0A0A0" text-anchor="middle">電動車</text>
  <text x="650" y="430" font-size="12" fill="#A0A0A0" text-anchor="middle">配件</text>
  <text x="850" y="430" font-size="12" fill="#A0A0A0" text-anchor="middle">服務</text>
</g>
```

See `templates/chart_bar.svg` for the starter.

---

## `chart_line` — line chart for trends

Use when tracking 4+ time points (quarters, years, months). Single line + dots, single highlight color.

### SVG anatomy

```xml
<g transform="translate(152, 200)">
  <!-- Y-axis labels & gridlines (same as bar) -->
  <!-- … -->

  <!-- X-axis tick labels (time points) -->
  <text x="0"    y="430" font-size="12" fill="#A0A0A0" text-anchor="middle">Q1 2024</text>
  <text x="250"  y="430" font-size="12" fill="#A0A0A0" text-anchor="middle">Q2</text>
  <text x="500"  y="430" font-size="12" fill="#A0A0A0" text-anchor="middle">Q3</text>
  <text x="750"  y="430" font-size="12" fill="#A0A0A0" text-anchor="middle">Q4</text>
  <text x="1000" y="430" font-size="12" fill="#A0A0A0" text-anchor="middle">Q1 2025</text>

  <!-- The line itself: polyline through the 5 data points -->
  <polyline
    points="0,280  250,200  500,160  750,100  1000,40"
    fill="none" stroke="#FF6900" stroke-width="3"
    stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Dots at each data point -->
  <circle cx="0"    cy="280" r="6" fill="#FF6900"/>
  <circle cx="250"  cy="200" r="6" fill="#FF6900"/>
  <circle cx="500"  cy="160" r="6" fill="#FF6900"/>
  <circle cx="750"  cy="100" r="6" fill="#FF6900"/>
  <circle cx="1000" cy="40"  r="6" fill="#FF6900"/>

  <!-- Value labels above each dot -->
  <text x="0"    y="260" font-size="13" font-weight="700" fill="#FF6900" text-anchor="middle">30%</text>
  <text x="250"  y="180" font-size="13" font-weight="700" fill="#FF6900" text-anchor="middle">50%</text>
  <text x="500"  y="140" font-size="13" font-weight="700" fill="#FF6900" text-anchor="middle">60%</text>
  <text x="750"  y="80"  font-size="13" font-weight="700" fill="#FF6900" text-anchor="middle">75%</text>
  <text x="1000" y="20"  font-size="13" font-weight="700" fill="#FF6900" text-anchor="middle">90%</text>
</g>
```

Optional fill under the line for area emphasis:
```xml
<path d="M0,280 L250,200 L500,160 L750,100 L1000,40 L1000,400 L0,400 Z"
      fill="#FF6900" fill-opacity="0.12"/>
```
Place this **before** the `<polyline>` so the line draws on top.

**Multi-series lines (2–3 max)**: the story-bearing line keeps full hue + 3px + dots; secondary lines drop to `stroke-opacity="0.45"`, 2px, no dots, no area fill. No legend — label each line directly at its right end (14px, the line's own color/opacity, `text-anchor="start"` at `x = last_point_x + 14`). Four or more lines is spaghetti: split pages or rethink.

See `templates/chart_line.svg` for the starter.

---

## `chart_donut` — donut chart for composition

Use when showing parts of a whole, 2–5 segments. Single dominant segment highlighted in the brand color; remaining segments in muted alphas of the same color.

### SVG anatomy (using arcs)

A donut is conceptually a ring made of arc segments. For a chart centered at (260, 260) with outer radius 200 and inner radius 130 (giving a 70px-thick ring), each segment is an arc that sweeps `angle = (value / total) × 360°`.

```xml
<g transform="translate(640, 400)">
  <!-- Background ring (subtle) -->
  <circle cx="0" cy="0" r="165" fill="none" stroke="#222222" stroke-width="70"/>

  <!-- Segments — use stroke-dasharray on a circle to draw partial arcs.
       Circumference = 2 × π × 165 ≈ 1037
       Segment 60%: dash = 622, gap = 415 (1037 - 622)
       Each segment starts where the previous ended via stroke-dashoffset.

       Transform rotate(-90) to start at top instead of right. -->

  <circle cx="0" cy="0" r="165" fill="none"
          stroke="#FF6900" stroke-width="70"
          stroke-dasharray="622 415"
          stroke-dashoffset="0"
          transform="rotate(-90)"/>

  <!-- Second segment at 25% -->
  <circle cx="0" cy="0" r="165" fill="none"
          stroke="#FF6900" stroke-width="70" stroke-opacity="0.55"
          stroke-dasharray="259 778"
          stroke-dashoffset="-622"
          transform="rotate(-90)"/>

  <!-- Third segment at 15% -->
  <circle cx="0" cy="0" r="165" fill="none"
          stroke="#FF6900" stroke-width="70" stroke-opacity="0.25"
          stroke-dasharray="155 882"
          stroke-dashoffset="-881"
          transform="rotate(-90)"/>

  <!-- Center text: highlight number + caption -->
  <text x="0" y="-6" font-size="56" font-weight="900" fill="#FFFFFF" text-anchor="middle">60%</text>
  <text x="0" y="32" font-size="14" fill="#A0A0A0" text-anchor="middle">智慧家居佔比</text>
</g>

<!-- Legend (right side, vertical) -->
<g transform="translate(900, 280)" font-size="14" fill="#FFFFFF">
  <rect x="0"  y="0"  width="14" height="14" fill="#FF6900"/>
  <text x="24" y="12">智慧家居 · 60%</text>

  <rect x="0"  y="36" width="14" height="14" fill="#FF6900" fill-opacity="0.55"/>
  <text x="24" y="48">智慧穿戴 · 25%</text>

  <rect x="0"  y="72" width="14" height="14" fill="#FF6900" fill-opacity="0.25"/>
  <text x="24" y="84">其他 · 15%</text>
</g>
```

See `templates/chart_donut.svg` for the starter.

---

## Computing segments for the donut

For each segment:
1. `circumference = 2 × π × radius` (here `2 × π × 165 ≈ 1037`)
2. `segment_length = (value_percent / 100) × circumference`
3. `dasharray = "<segment_length> <circumference - segment_length>"`
4. `dashoffset = -sum_of_previous_segment_lengths`

That's it. The math is mechanical, just keep the running offset.

---

## `chart_hbar` — horizontal bars for rankings

Use when the message is **who leads** — market share ranking, channel revenue ranking, feature adoption ordering — or when category labels are too long for vertical-bar x-axis labels. 4–8 items, sorted descending (the planner pre-sorts; keep natural order only when the sequence itself matters, e.g. funnel stages already covered by `funnel`).

### SVG anatomy

```xml
<g transform="translate(300, 190)">
  <!-- Baseline (x=0 axis) -->
  <line x1="0" y1="-10" x2="0" y2="386" stroke="#333333" stroke-width="1"/>

  <!-- Rows: bar height 48, row gap 34 → row pitch 82. Scale: 800px = max value.
       Values 142 / 98 / 76 / 41 / 22 → widths 800 / 552 / 428 / 231 / 124 -->
  <rect x="0" y="0"   width="800" height="48" fill="#FF6900" rx="6"/>
  <rect x="0" y="82"  width="552" height="48" fill="#FF6900" fill-opacity="0.45" rx="6"/>
  <rect x="0" y="164" width="428" height="48" fill="#FF6900" fill-opacity="0.45" rx="6"/>
  <rect x="0" y="246" width="231" height="48" fill="#FF6900" fill-opacity="0.45" rx="6"/>
  <rect x="0" y="328" width="124" height="48" fill="#FF6900" fill-opacity="0.45" rx="6"/>

  <!-- Value labels at each bar's end -->
  <text x="814" y="31"  font-size="16" font-weight="700" fill="#FF6900" style="font-variant-numeric: tabular-nums">142</text>
  <!-- … one per bar, x = bar width + 14, y = row_y + 31 -->

  <!-- Category labels, right-aligned against the baseline -->
  <text x="-18" y="30"  font-size="15" fill="#FFFFFF" text-anchor="end">線上商城</text>
  <text x="-18" y="47"  font-size="10" fill="#666666" text-anchor="end" letter-spacing="1">ONLINE STORE</text>
  <!-- … one pair per row -->
</g>
```

- **Emphasis discipline**: the ranked leader (or whichever bar the title's claim is about) at full hue; the rest at `fill-opacity="0.45"`. If the claim is about the *gap* rather than the leader, add a `diff_arrow` annotation instead.
- Left gutter: the `translate` x (300) leaves ~250px for right-aligned CN + EN labels — widen it if labels run long, and shrink plot width to match (`x_plot + width ≤ 1040` inside the translate).
- No horizontal gridlines — every bar carries its value.

See `templates/chart_hbar.svg` for the starter.

---

## `chart_stacked_bar` — composition across categories or time

Use when the message is a **mix shift**: revenue structure across 3 years, cost composition across business units. Each column is a whole; segments are its parts. 2–5 columns, **2–4 segments** (5+ segments → merge the smallest into 其他, or split into two charts).

Two modes, decided by the data: **absolute** (columns have different totals — totals labeled on top; the shape of the total line is part of the story) and **100%** (`unit: "%"`, every column sums to 100 — no totals labeled; the moving boundary *is* the story).

### The three signature marks — what makes it think-cell-grade

1. **Totals above each column** (absolute mode): 16px bold, ink voice (`#FFFFFF` dark / `#383838` fresh), `y = column_top − 12`.
2. **Segment connectors**: thin 1px lines (`#555555` dark / `#C8CDD2` fresh) joining every segment boundary from one column's right edge to the next column's left edge. They turn four separate columns into one readable flow — the eye follows a segment's growth without re-measuring each column.
3. **Emphasis series**: the segment the argument is about at full hue; the rest at `0.45` / `0.18` alphas. Series names sit **left of the first column**, right-aligned at each segment's mid-height (13px, `#A0A0A0`).

### SVG anatomy (absolute mode, 3 columns × 3 segments)

```xml
<g transform="translate(152, 200)">
  <!-- Data: 2023 total 180 (硬體140/服務25/其他15) · 2024 total 240 (165/55/20)
       · 2025 total 310 (190/95/25). Scale: 1.25px per unit, baseline y=400.
       Columns w=160 at x = 130 / 420 / 710. Stack bottom-up: 硬體, 服務, 其他. -->

  <!-- 2023 column -->
  <rect x="130" y="225" width="160" height="175" fill="#FF6900" fill-opacity="0.45"/>
  <rect x="130" y="194" width="160" height="31"  fill="#FF6900"/>
  <rect x="130" y="175" width="160" height="19"  fill="#FF6900" fill-opacity="0.18"/>
  <!-- 2024: heights 206 / 69 / 25 → y 194 / 125 / 100 · 2025: 238 / 119 / 31 → y 162 / 43 / 12 -->

  <!-- Totals (ink voice) -->
  <text x="210" y="163" font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="middle" style="font-variant-numeric: tabular-nums">180</text>
  <text x="500" y="88"  font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="middle" style="font-variant-numeric: tabular-nums">240</text>
  <text x="790" y="0"   font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="middle" style="font-variant-numeric: tabular-nums">310</text>

  <!-- Segment connectors: one line per boundary, adjacent columns -->
  <line x1="290" y1="225" x2="420" y2="194" stroke="#555555" stroke-width="1"/>
  <line x1="290" y1="194" x2="420" y2="125" stroke="#555555" stroke-width="1"/>
  <line x1="290" y1="175" x2="420" y2="100" stroke="#555555" stroke-width="1"/>
  <!-- … same three between columns 2 and 3 -->

  <!-- Series labels, left of first column at segment mid-heights -->
  <text x="112" y="316" font-size="13" fill="#A0A0A0" text-anchor="end">硬體</text>
  <text x="112" y="214" font-size="13" fill="#A0A0A0" text-anchor="end">服務</text>
  <text x="112" y="188" font-size="13" fill="#A0A0A0" text-anchor="end">其他</text>

  <!-- Segment value labels: centered inside segments ≥24px tall (#111111 ink on the
       full-hue segments); thinner segments labeled just outside with a 2–4px leader -->
  <!-- Category labels at y=430 (CN) / y=452 (EN 10px #666666), centered per column -->
</g>
```

- Segment value labels go inside the segment only when it is ≥24px tall — `#111111` ink on the full-hue emphasis segments (AA rule above), `#E8E8E8`/`#C8C8C8` on the low-alpha ones. A thinner segment gets its value just outside the column with a 2–4px leader (series labeling stays complete — see Common rules).
- Baseline `<line>` at y=400 in `#333333`; y-axis labels optional in absolute mode (totals carry the scale).

See `templates/chart_stacked_bar.svg` for the starter.

---

## `chart_waterfall` — the A→B bridge

The think-cell signature. Use when the message is **what explains the change**: 2023 → 2025 revenue bridge by driver, cost delta decomposition, headcount build-up. The first and last items are **totals** (full columns from zero); items between are **floating deltas** stacked cumulatively.

### Data → geometry (the running-level math)

Keep one running level `c`, starting at the first total. Each delta bar spans `[c, c + delta]`; then `c += delta`. Scale so the *highest* cumulative level (not the end total — the peak may be mid-bridge) fits the 400px plot with headroom.

```
Items: 2023營收 180 (total) · 智慧家居 +55 · 訂閱服務 +70 · 海外市場 +30 · 配件調整 −25 · 2025營收 310 (total)
Scale 1.15 px/unit, baseline y=400. Peak level = 335.
levels: 180 → 235 → 305 → 335 → 310
```

### SVG anatomy

```xml
<g transform="translate(152, 200)">
  <!-- 6 bars, w=110, x = 0 / 178 / 356 / 534 / 712 / 890 -->

  <!-- Start total: full column, ink-neutral fill -->
  <rect x="0" y="193" width="110" height="207" fill="#3A3A3C"/>
  <!-- Increases: float from previous level, highlight fill -->
  <rect x="178" y="130" width="110" height="63" fill="#FF6900"/>
  <rect x="356" y="49"  width="110" height="81" fill="#FF6900"/>
  <rect x="534" y="15"  width="110" height="34" fill="#FF6900"/>
  <!-- Decrease: neutral gray, NEVER red -->
  <rect x="712" y="15"  width="110" height="29" fill="#6E6E73"/>
  <!-- End total -->
  <rect x="890" y="44"  width="110" height="356" fill="#3A3A3C"/>

  <!-- Level connectors: dashed 1px from each bar's closing level to the next bar -->
  <line x1="110" y1="193" x2="178" y2="193" stroke="#555555" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="288" y1="130" x2="356" y2="130" stroke="#555555" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="466" y1="49"  x2="534" y2="49"  stroke="#555555" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="644" y1="15"  x2="712" y2="15"  stroke="#555555" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="822" y1="44"  x2="890" y2="44"  stroke="#555555" stroke-width="1" stroke-dasharray="3 3"/>

  <!-- Value labels: totals in ink bold; deltas signed, in their bar's color -->
  <text x="55"  y="181" font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="middle">180</text>
  <text x="233" y="118" font-size="15" font-weight="700" fill="#FF6900" text-anchor="middle">+55</text>
  <text x="411" y="37"  font-size="15" font-weight="700" fill="#FF6900" text-anchor="middle">+70</text>
  <text x="589" y="3"   font-size="15" font-weight="700" fill="#FF6900" text-anchor="middle">+30</text>
  <text x="767" y="3"   font-size="15" font-weight="700" fill="#9A9AA0" text-anchor="middle">−25</text>
  <text x="945" y="32"  font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="middle">310</text>

  <!-- Category labels at y=430 / EN at y=452, centered per bar -->
</g>
```

- **Colors**: totals `#3A3A3C` (dark) / `#383838` (fresh); increases = highlight; decreases `#6E6E73` (dark) / `#AEB4BA` (fresh).
- Subtotal columns mid-bridge (e.g. a regional subtotal) are allowed: same treatment as totals, `role: "total"` in the data.
- **Emphasis follows the claim.** When the title singles out specific drivers, only those delta bars stay full hue — background drivers drop to `fill-opacity 0.45` (their signed labels to muted gray `#9A9AA0`). All increases full-orange under a "these two drivers did it" title contradicts the claim.
- **The annotation states the title's number.** The classic is a **`diff_arrow` bracket** at the right edge (start-total top → end-total top, "+72%") — but only when the title claims the *total* change. If the title claims a *contribution share* ("兩項驅動貢獻近八成"), bracket the claim-bearing bars instead and label the share ("+100 · 佔增長77%"). Only one annotation label takes the hue; the other stays ink.

See `templates/chart_waterfall.svg` for the starter.

---

## `chart_combo` — bars + line for two coupled metrics

Use when two metrics **must be read together** to make the point: 營收 (bars) + 毛利率 (line), users (bars) + churn (line), volume + rate. This is the one sanctioned two-metric chart — anything beyond volume-plus-rate on one canvas is two pages.

### SVG anatomy

```xml
<g transform="translate(152, 200)">
  <!-- Bars: 營收 120/180/240/310 NT$億 · scale 1.2px/unit · w=120 at x=60/300/540/780 -->
  <rect x="60"  y="256" width="120" height="144" fill="#FF6900" rx="6"/>
  <rect x="300" y="184" width="120" height="216" fill="#FF6900" rx="6"/>
  <rect x="540" y="112" width="120" height="288" fill="#FF6900" rx="6"/>
  <rect x="780" y="28"  width="120" height="372" fill="#FF6900" rx="6"/>

  <!-- Line: 毛利率 18/21/24/26% on its own scale (15–30% → y 400–0), ink voice.
       Points at bar centers: (120,320) (360,240) (600,160) (840,107) -->
  <polyline points="120,320 360,240 600,160 840,107"
            fill="none" stroke="#FFFFFF" stroke-width="3"
            stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="120" cy="320" r="6" fill="#FFFFFF"/>
  <circle cx="360" cy="240" r="6" fill="#FFFFFF"/>
  <circle cx="600" cy="160" r="6" fill="#FFFFFF"/>
  <circle cx="840" cy="107" r="6" fill="#FFFFFF"/>

  <!-- Direct labels: bar values in hue above bars; line values in ink above dots
       (#111111 where they sit ON a full-hue bar — the AA rule); line NAME at the
       line's right end, fully clear of the last bar (back on black → white) -->
  <text x="120" y="244" font-size="15" font-weight="700" fill="#FF6900" text-anchor="middle">120</text>
  <!-- … -->
  <text x="120" y="304" font-size="13" font-weight="700" fill="#111111" text-anchor="middle">18%</text>
  <!-- … -->
  <text x="914" y="112" font-size="14" font-weight="600" fill="#FFFFFF" text-anchor="start">毛利率</text>
</g>
```

- **No right axis.** Two axes invite mis-reading; direct value labels on both series carry the scales. A small top-right legend names the two units (the combo exception from Common rules — the one case direct labels can't serve); the line is also named at its right end — placed fully clear of the last bar (a name that straddles the bar edge splits across two backgrounds and one half vanishes).
- Line always in **ink** (`#FFFFFF` dark / `#383838` fresh), never a second hue. Bars own the color. Where the line's value labels (or its name) land on the full-hue bars, they flip to near-black `#111111` (the AA rule in Common rules).
- The classic annotation here is a **`cagr_arrow`** over the bars — growth claim on the bars, margin trend told by the line.

See `templates/chart_combo.svg` for the starter.

---

## `chart_mekko` — the two-dimensional market map

Use when **both** dimensions carry the message: column width = segment size (share of total market), column stacking = player share within the segment. "Who owns what, and how big is what" on one canvas. 2–4 columns × 2–4 series.

### Data → geometry

- Column widths: `width_pct` of each category × 1000px plot width, columns adjacent (2px breathing inset per edge, no gaps — the full width IS the whole).
- Within each column: segments are a 100% vertical stack of the plot height (420px), top-down in `series[]` order.

### SVG anatomy

```xml
<g transform="translate(152, 190)">
  <!-- Columns 智慧家居 45% / 智慧穿戴 30% / 訂閱服務 25% → x-spans 0–450 / 450–750 / 750–1000
       Series 公司A (emphasis) / 公司B / 其他. Col heights = pct × 4.2px. -->

  <!-- Column 1: A 52% / B 28% / 其他 20% → h 216 / 114 / 82 (2px gaps) -->
  <rect x="2" y="0"   width="446" height="216" fill="#FF6900"/>
  <rect x="2" y="220" width="446" height="114" fill="#FF6900" fill-opacity="0.45"/>
  <rect x="2" y="338" width="446" height="82"  fill="#FF6900" fill-opacity="0.18"/>
  <!-- Columns 2 & 3: same pattern at x=452 (w=296) and x=752 (w=246) -->

  <!-- Column headers ABOVE the plot: category + its width share -->
  <text x="225" y="-22" font-size="15" font-weight="700" fill="#FFFFFF" text-anchor="middle">智慧家居 · 45%</text>
  <!-- … -->

  <!-- In-segment share labels (only where segment height ≥30px) -->
  <text x="225" y="115" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle">52%</text>
  <text x="225" y="284" font-size="15" font-weight="600" fill="#E8E8E8" text-anchor="middle">28%</text>
  <text x="225" y="386" font-size="14" fill="#C8C8C8" text-anchor="middle">20%</text>

  <!-- Series labels left of column 1, right-aligned at segment mid-heights -->
  <text x="-14" y="112" font-size="13" fill="#A0A0A0" text-anchor="end">公司A</text>
  <text x="-14" y="281" font-size="13" fill="#A0A0A0" text-anchor="end">公司B</text>
  <text x="-14" y="383" font-size="13" fill="#A0A0A0" text-anchor="end">其他</text>
</g>
```

- Text contrast per alpha tier: near-black `#111111` on the full hue (white on the highlight fails AA — Common rules), `#E8E8E8` on 0.45, `#C8C8C8` on 0.18 (dark theme). Fresh theme: `#111111` on full green, `#383838` ink on the light tiers.
- A mekko is dense by nature — it earns its place only when *both* axes matter. If column widths would be near-equal, use `chart_stacked_bar` (100% mode); if there's only one column, use `chart_donut`.

See `templates/chart_mekko.svg` for the starter.

---

## `chart_radar` — multi-axis assessment profile

Use when **one entity is rated across several criteria** and the *shape of the profile* is the message: a satisfaction survey (解決問題/回應速度/介面易用…), a capability assessment, a maturity model. 3–8 axes. Radar is hard to scan quickly, so it earns its place only when the multi-axis profile genuinely is the point — for a single ranking use `chart_bar`/`chart_hbar`, and beyond 8 axes the polygon turns to mush (split the criteria or rank them). Overlay **at most 3** profiles (us vs competitor vs benchmark); more is spaghetti.

### Data → geometry

A regular N-gon centered at `(640, 410)`, outer radius `R = 205`. Axis `k` points at angle `θ_k = −90° + k·(360°/N)` (first axis straight up, then clockwise). A value `v` on a `0…max` scale sits at radius `r = (v / max) · R` along its axis: `(640 + r·cosθ, 410 + r·sinθ)`. Draw 4–5 concentric grid N-gons at even fractions of R, plus one spoke per axis — all in gridline gray.

### SVG anatomy (6 axes, single series, 0–5 scale)

```xml
<!-- Grid rings (concentric hexagons) + spokes: gridline gray #333333 -->
<polygon points="640,205 817.5,307.5 817.5,512.5 640,615 462.5,512.5 462.5,307.5"
         fill="none" stroke="#333333" stroke-width="1.5"/>   <!-- outer ring, +inner rings -->
<line x1="640" y1="410" x2="640" y2="205" stroke="#333333" stroke-width="1"/>   <!-- one spoke per axis -->

<!-- Data polygon: highlight stroke + 0.15 fill + vertex dots -->
<polygon points="640,225.5 782,328 746.5,471.5 640,553.5 490.9,496.1 540.6,352.6"
         fill="#FF6900" fill-opacity="0.15" stroke="#FF6900" stroke-width="2.5" stroke-linejoin="round"/>
<circle cx="640" cy="225.5" r="5" fill="#FF6900"/>   <!-- one per vertex -->

<!-- Vertex value labels (highlight hue), axis names at perimeter (r+28, ink) -->
<text x="640" y="213.5" font-size="13" font-weight="700" fill="#FF6900" text-anchor="middle">4.5</text>
<text x="640" y="177"   font-size="15" fill="#FFFFFF" text-anchor="middle">解決問題</text>

<!-- Optional center aggregate score (single series only) -->
<text x="640" y="402" font-size="52" font-weight="900" fill="#FFFFFF" text-anchor="middle">3.7</text>
<text x="640" y="430" font-size="14" fill="#A0A0A0" text-anchor="middle" letter-spacing="1">整體評分</text>
```

- **Single-hue discipline**: grid rings + spokes are gridline gray, never colored. The data polygon owns the highlight (stroke full hue, fill at 0.15). A second/third overlaid series drops its fill (stroke only at `stroke-opacity 0.45`, no dots) so the emphasis profile reads first — same emphasis logic as multi-series `chart_line`.
- **Axis-name anchoring**: right axes `text-anchor="start"`, left axes `end`, top/bottom `middle`. Perimeter labels sit at `R + 28`.
- **Center score** is a single-series affordance (the profile's average). Omit it when overlaying multiple series — the center would sit under two polygons.
- **`corporate_fresh`**: grid/spokes `#DDE2DF`, axis names `#383838`, data green `#3DB377` (fill 0.15), value labels `#383838` (green fails AA as small text on white — the Common-rules AA discipline). **`IT_prism`**: grid/spokes `#DFE2E9`, axis names `#344252`, data green `#58D494` (fill 0.15), value labels `#344252`.

See `templates/chart_radar.svg` for the starter.

---

## `chart_gantt` — project schedule across a time grid

Use when the message is **when work happens and how phases overlap**: an implementation roadmap, a rollout schedule, a multi-workstream plan. Rows are workstreams/tasks (≤8), columns are time periods (months/quarters), bars are duration spans. This is distinct from the `timeline` primitive — **`timeline` anchors events to points in time (no duration); `chart_gantt` draws parallel rows of duration bars on a grid.** If tasks have no duration (just milestone dates), use `timeline` or cards.

### Data → geometry

Left gutter `x=88…300` holds right-aligned row labels. Time grid spans `x=310…1192` across `N` equal columns (`col_w = 882 / N`; here 12 months → `73.5`). Column `i` starts at `x = 310 + i·col_w`. A task on months `[a, b]` is a bar at `x = 310 + a·col_w`, `width = (b − a + 1)·col_w`. Rows start `y=210`, pitch 46, bar height 28.

### SVG anatomy (6 workstreams × 12 months)

```xml
<!-- Vertical month gridlines (N+1) + a header line under the month labels: gridline gray -->
<line x1="310" y1="200" x2="310" y2="478" stroke="#333333" stroke-width="1"/>   <!-- per boundary -->
<line x1="88"  y1="200" x2="1192" y2="200" stroke="#333333" stroke-width="1.5"/>
<text x="346.75" y="190" font-size="13" fill="#A0A0A0" text-anchor="middle">1</text>   <!-- month labels, centered -->

<!-- Task bars: emphasis phase full hue, others 0.45. Row labels right-aligned in gutter -->
<rect x="530.5" y="302" width="367.5" height="28" rx="6" fill="#FF6900"/>                    <!-- emphasis -->
<rect x="310"   y="210" width="147"   height="28" rx="6" fill="#FF6900" fill-opacity="0.45"/>
<text x="295" y="321" font-size="15" fill="#FFFFFF" text-anchor="end">開發實作</text>

<!-- today / deadline reference line (value_line annotation, ink dashed) -->
<line x1="824.5" y1="200" x2="824.5" y2="478" stroke="#CCCCCC" stroke-width="1.5" stroke-dasharray="6 4"/>
<text x="824.5" y="192" font-size="13" font-weight="600" fill="#CCCCCC" text-anchor="middle">現在</text>

<!-- milestone diamond (callout annotation, ink) at a task's key date -->
<polygon points="1045,354 1053,362 1045,370 1037,362" fill="#FFFFFF"/>
<text x="1060" y="366" font-size="12" font-weight="600" fill="#FFFFFF" text-anchor="start">驗收</text>
```

- **Single-hue discipline**: every bar is the one highlight color; workstreams are **never** color-coded. Phase/status differentiation is by alpha — the current or critical-path phase at full hue, the rest at `0.45`. Colored-by-workstream is the classic Gantt anti-pattern that breaks the single-accent invariant.
- **Data speaks color, analysis speaks ink**: bars are hue; the today/deadline line (a vertical `value_line`) and milestone diamonds are ink (`#CCCCCC`/`#FFFFFF` dark, `#383838` fresh) — never a second accent.
- Keep it to ≤8 rows; more workstreams choke the row labels (split into phase pages). Month labels stay in the header; per-bar duration text is optional (the bar length already carries it).
- **`corporate_fresh`**: gridlines `#DDE2DF`, month/row labels `#6B7178`/`#383838`, bars green `#3DB377` (+0.45 tier), today line + milestones ink `#383838`. **`IT_prism`**: gridlines `#DFE2E9`, labels `#6B7686`/`#344252`, bars green `#58D494` (+0.45 tier), today line + milestones ink `#344252`.

See `templates/chart_gantt.svg` for the starter.

---

## Annotation layer — 圖表自帶分析

This is the heart of the consulting look. think-cell's charts read as *arguments* because the analysis is drawn on the chart: a CAGR arrow says "this grew this fast", a difference bracket says "the gap is this big", a reference line says "here is the bar to clear". DeckForge adopts the same vocabulary as an optional `annotations[]` array inside `chart_data`.

> **The claim rule.** A chart page's title is a claim (pyramid principle). When that claim is quantitative — grew ×2, all above 70%, gap widened to 3× — the chart must **visually assert it**, and the annotation layer is how. The planner computes the numbers and plans the annotation; the designer draws it. If planning omitted the annotation and the title's claim maps directly onto the data (a growth between two labeled points, a threshold every bar clears), the designer adds the one matching annotation — that judgment is expected, not optional polish. **Cap: ≤2 annotations per chart.** One annotation is a claim; three are noise.

### Schema

```json
"chart_data": {
  "unit": "%",
  "items": [ ... ],
  "annotations": [
    { "type": "value_line", "value": 70, "label": "目標 70%" },
    { "type": "cagr_arrow", "from": "2022", "to": "2025", "label": "+37.2% CAGR" },
    { "type": "diff_arrow", "from": "2023營收", "to": "2025營收", "label": "+72%" },
    { "type": "callout",    "at": "Q3", "label": "新品上市" }
  ]
}
```

`from` / `to` / `at` reference `items[].label` strings exactly. `label` is **required and pre-computed by the planner** — the designer draws, never invents math. (CAGR = `(end/start)^(1/periods) − 1`; sanity-check the arithmetic, don't re-derive it.)

### The four types — geometry recipes

**`value_line` — reference / target / average line.** Horizontal dashed line across the plot at the value's y; label right-aligned above its right end. On `chart_hbar` it's vertical.

```xml
<line x1="0" y1="120" x2="1000" y2="120" stroke="#CCCCCC" stroke-width="1.5" stroke-dasharray="6 4"/>
<text x="1000" y="108" font-size="13" font-weight="600" fill="#CCCCCC" text-anchor="end">目標 70%</text>
```

**`cagr_arrow` — growth arc across the series.** A quadratic arc from just above the first bar/point to just above the last, arrowhead at the far end, label at the apex. Ink voice.

```xml
<path d="M 120,244 Q 480,-30 840,16" fill="none" stroke="#FFFFFF" stroke-width="2"/>
<polygon points="840,16 828,8 832,22" fill="#FFFFFF"/>   <!-- arrowhead -->
<text x="480" y="-14" font-size="15" font-weight="700" fill="#FFFFFF" text-anchor="middle">+37.2% CAGR</text>
```

**`diff_arrow` — difference bracket.** A vertical bracket (line + 8px end ticks) spanning the two referenced levels, label beside its midpoint. Between two adjacent bars, or at the plot's right edge for start-vs-end (waterfall). The label states the delta — absolute or %, whichever the claim uses.

```xml
<line x1="1008" y1="44" x2="1008" y2="193" stroke="#FFFFFF" stroke-width="1.5"/>
<line x1="1000" y1="44" x2="1016" y2="44"  stroke="#FFFFFF" stroke-width="1.5"/>
<line x1="1000" y1="193" x2="1016" y2="193" stroke="#FFFFFF" stroke-width="1.5"/>
<text x="1020" y="123" font-size="17" font-weight="700" fill="#FF6900" text-anchor="start">+72%</text>
```

**`callout` — event marker.** A 4px dot on the referenced data point, a short 1px leader line up-and-away, and a ≤8-char label. For "what happened here" moments on trends: launch, policy change, incident.

```xml
<circle cx="500" cy="160" r="4" fill="#FFFFFF"/>
<line x1="500" y1="156" x2="530" y2="120" stroke="#CCCCCC" stroke-width="1"/>
<text x="536" y="116" font-size="13" fill="#CCCCCC" text-anchor="start">新品上市</text>
```

### Applicability

| | `value_line` | `cagr_arrow` | `diff_arrow` | `callout` |
|---|---|---|---|---|
| `chart_bar` | ✓ | ✓ (ordered categories) | ✓ (two bars) | ✓ |
| `chart_hbar` | ✓ (vertical) | — | ✓ | — |
| `chart_line` | ✓ | ✓ | ✓ (two points) | ✓ |
| `chart_stacked_bar` | ✓ (absolute mode) | ✓ (on totals) | ✓ (totals or one series) | — |
| `chart_waterfall` | — | — | ✓ (start↔end, the classic) | — |
| `chart_combo` | ✓ | ✓ (on bars) | ✓ | ✓ |
| `chart_donut` / `chart_mekko` | — (their emphasis segment IS the assertion) | — | — | — |
| `chart_radar` | — | — | — | ✓ (flag one axis) |
| `chart_gantt` | ✓ (today / deadline line) | — | — | ✓ (milestone diamond) |

Built-ins are not annotations: waterfall level-connectors, stacked-bar totals + segment connectors, and line-end series labels are part of their chart's base anatomy — always drawn, never requested.

### Color rules for annotations

Annotations speak **ink**, not hue (see "two voices" above): `#FFFFFF`/`#CCCCCC` strokes and labels on dark, `#383838` on fresh. One exception, **dark themes only**: the single most claim-bearing label's *text* may take the highlight hue — it passes AA on near-black (`#FF6900` ≈ 5.4:1). On light/fresh themes there is no hue exception: orange `#E8872E` on the white card is ≈ 2.65:1 and fails AA, so the claim-bearing label is ink `#383838` bold, and orange stays inside body-text inline runs. One hue label per page max, text only, never the stroke.

---

## What charts NOT to use

- **Pie chart (full circle, no center hole)**: harder to read center label, looks less modern. Use donut instead.
- **3D charts**: never. Distorts proportions.
- **Stacked bars with >4 segments**: unreadable. Merge the smallest into 其他, or split into two charts.
- **Truncated value axes**: bars start at zero, no exceptions (axis-break squiggle for the one outlier bar — see Common rules).
- **Dual-axis charts beyond `chart_combo`'s volume+rate pairing**: two arbitrary metrics sharing a canvas invite false correlation. If they're not a volume and its rate, they're two pages.
- **Radar for a single ranking or comparison**: a radar is for a multi-axis *profile* (3–8 criteria, shape is the message); when you have one metric across items, that's `chart_bar`/`chart_hbar`. Radar is hard to scan — don't reach for it just to look sophisticated (bounds in the `chart_radar` section).

---

## When the data is sparse, skip the chart

A line chart with 3 dots looks like a hand-drawn sketch. A bar chart with 2 bars is two cards. A waterfall with one delta is a before/after pair (`two_col_50_50` `before_after`). A stacked bar with one column is a donut. Don't force charts on small data — use `stat_hero` or `mini_grid` instead.

Minimum shapes: `chart_line` 4+ points · `chart_bar`/`chart_hbar` 4+ items · `chart_donut` 2–5 segments · `chart_stacked_bar` 2+ columns × 2+ segments · `chart_waterfall` 2 totals + 2+ deltas · `chart_combo` 3+ periods · `chart_mekko` 2+ columns × 2+ series · `chart_radar` 3+ axes · `chart_gantt` 3+ tasks spanning multiple periods.

The rule: **charts earn their visual cost only when data has shape** (a curve, a distribution, a clear ranking, a moving mix, a bridge). If you can show the data in 2–3 cards as fast as a chart — and no relationship is lost — choose cards.
