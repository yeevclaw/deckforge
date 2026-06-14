# Chart Anatomy — SVG charts for data-heavy slides

Cards with numbers are great for hero stats. But when the story is **a trend, a composition, or a comparison across many items**, a chart communicates faster than a grid of mini-cards. This reference shows how to draw the three chart types DeckForge supports (`chart_bar`, `chart_line`, `chart_donut`) directly as SVG primitives — no external libraries, fully editable in PowerPoint after Convert to Shape.

The article that inspired DeckForge uses Chart.js for the web version. SVG charts here serve the same role for slides: visualizing trends, growth rates, compositions, and comparisons.

## When to use a chart vs cards

| Data shape | Best representation |
|---|---|
| 3–5 parallel numbers, each independently meaningful | `mini_grid` (cards) |
| 1 dominant number | `stat_hero` (card) |
| **Trend over time** (4+ time points) | **`chart_line`** |
| **Comparison across categories** (4+ items) | **`chart_bar`** |
| **Composition** (parts of a whole) | **`chart_donut`** |
| **Single proportion** (1 vs total) | **`stat_hero` with percent** or `chart_donut` with 1 segment |
| 2 items contrasting | `two_col_50_50` cards |

If you can fit it in cards, prefer cards — they're more flexible. Reach for charts when the data shape *demands* a chart.

## Common rules (all charts)

- **Single highlight color discipline.** All foreground/data fill uses the deck's `highlight_color`. No multi-color palettes inside the chart. Multiple data series? Use varying alpha (`0.9`, `0.6`, `0.3`) of the same hue.
- **Background**: same dark gray card (`#1A1A1A`) or pure black slide bg.
- **Axes / gridlines**: thin (1px) `#333333`. Subtle, not assertive.
- **Labels**: `#A0A0A0` 12–14px. Axis labels in English, data labels in CN.
- **`corporate_fresh` decks (the default style)**: same geometry, swap the neutrals and the data hue — white card on `#F4F4F4` canvas, gridlines `#DDE2DF`, labels `#6B7178` (values `#383838`), and the data series uses the family's **structure green `#3DB377`** with the same alpha tiers (donut segments: alphas of that green). Orange `#E8872E` stays reserved for inline text emphasis — never as chart fill.
- **Title sits OUTSIDE the chart**, as the page title. The chart itself has no internal title — the page title carries it.
- **Numbers on bars / points**: optional. If shown, render at 14–16px in highlight color, above each data point. Add `style="font-variant-numeric: tabular-nums"` so values align across bars/points and axis ticks.
- **No legend** if the highlight color is single-series. Legend only when you have 2+ series — keep it 12px in `#A0A0A0`, positioned top-right.

## Chart canvas

A chart layout (`chart_bar`, `chart_line`, `chart_donut`) takes the full slide content area below the title:
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

## What charts NOT to use

- **Pie chart (full circle, no center hole)**: harder to read center label, looks less modern. Use donut instead.
- **3D charts**: never. Distorts proportions.
- **Stacked bars with >3 segments**: hard to compare. Use grouped bars or two charts.
- **Radar/spider charts**: only if absolutely necessary; the article's source material doesn't use them, and they're hard to scan quickly.

---

## When the data is sparse (1–3 points), skip the chart

A line chart with 3 dots looks like a hand-drawn sketch. A bar chart with 2 bars is two cards. Don't force charts on small data — use `stat_hero` or `mini_grid` instead.

The rule: **charts earn their visual cost only when data has shape** (a curve, a distribution, a clear ranking). If you can show the data in 2–3 cards as fast as a chart, choose cards.
