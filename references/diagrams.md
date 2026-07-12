# Diagram Primitives — Layouts beyond Bento

The Bento Grid (see [bento_grid.md](bento_grid.md)) is DeckForge's **base layout language**. Most content pages should use it. This document defines the nine **diagram primitives** that exist alongside bento for pages where rendering in bento would *drop structural information the audience needs to read the slide correctly*.

## Philosophy — primitives are precision rescue, not variety

Two rules govern when a primitive is used:

1. **Bento is the default.** Try bento first on every page.
2. **Switch to a primitive only on information loss.** The test is not "could a primitive express this" — it's "**what gets lost if I render this in bento?**" If you can't articulate the loss, stay in bento.

Visual variety is a side effect of good content-shape detection, not a goal. A deck that uses bento on 80% of pages is healthy; a deck that uses primitives on 60% of pages because "it looks more interesting" is a smell signal.

See [prompts/04_planning_draft.md → Primitive layouts](../prompts/04_planning_draft.md) for the four information-loss signals and the detection rule that decides when each primitive applies.

**Styling note — the geometry in this document is style-agnostic; the example colors are dark_apple.** On `IT_prism` decks (the default style), keep every coordinate but swap the neutrals: canvas `#EFF0F3`, white cards (whisper shadow), ink `#344252`, body `#4C5A6B`/`#6B7686`, connectors/strokes `#9BD9BE`, the single highlighted element uses accent green `#58D494` fill or a slate anchor (green never as a text fill). On `corporate_fresh` decks, swap instead to: canvas `#F4F4F4`, white cards (no border, whisper shadow), ink `#383838`, body `#4A5158`/`#6B7178`, connectors/strokes `#9BD4B8`, the single highlighted element uses structure green `#3DB377` (never orange — that's reserved for inline text emphasis). Where the family's composition vocabulary has a richer equivalent, prefer it: `flow` → `glass_arch_flow` (a four-variant family — render the variant in `design_brief.flow_variant`), `cycle` → `glass_orbit_loop`, `timeline`/process pipelines → `transit_pipeline`, `hierarchy_tree`/`pyramid` → `claim_tree` (see design_system.md → "Composition vocabulary").

---

## The four information-loss signals → 9 primitives

| Loss type | Primitive(s) |
|---|---|
| **Direction loss** — order matters and bento flattens it | `flow` / `timeline` / `cycle` / `funnel` |
| **Alignment loss** — row-by-row comparison required | `compare_table` |
| **Topology loss** — parent-child / hierarchy flattens | `hierarchy_tree` / `pyramid` |
| **Axis loss** — 2D positional semantics required | `quadrant_2x2` / `venn` |

---

## Designer SVG support status

| Primitive | Designer SVG status | Starter template |
|---|---|---|
| `flow` | supported | [templates/flow.svg](../templates/flow.svg) |
| `timeline` | supported | [templates/timeline.svg](../templates/timeline.svg) |
| `cycle` | supported | [templates/cycle.svg](../templates/cycle.svg) |
| `funnel` | supported | [templates/funnel.svg](../templates/funnel.svg) |
| `compare_table` | supported | [templates/compare_table.svg](../templates/compare_table.svg) |
| `quadrant_2x2` | supported | [templates/quadrant_2x2.svg](../templates/quadrant_2x2.svg) |
| `venn` | supported | [templates/venn.svg](../templates/venn.svg) |
| `hierarchy_tree` | supported | [templates/hierarchy_tree.svg](../templates/hierarchy_tree.svg) |
| `pyramid` | supported | [templates/pyramid.svg](../templates/pyramid.svg) |

Track changes to this status in the same edit that lands a Designer SVG template.

---

# Direction primitives

## 1. `flow` — sequential steps with direction

```
+----------+      +----------+      +----------+      +----------+
| step 1   | ───▶ | step 2   | ───▶ | step 3   | ───▶ | step 4   |
+----------+      +----------+      +----------+      +----------+
```

**Identity**: abstract sequence where each step depends on the prior. No time anchor.

**Use when**: process steps ("collect → analyze → validate → act"), pipeline stages, decision sequences.

**Don't use when**:
- Items are parallel features → `mini_grid`
- Has actual dates/quarters → `timeline`
- Loops back to start → `cycle`
- Quantity drops at each stage → `funnel`

**Common confusion**: 5 product features ≠ flow (they're parallel — use `mini_grid`). 5 onboarding steps = flow (each step depends on the prior).

**Schema**:
```json
{
  "layout": "flow",
  "flow_data": {
    "orientation": "horizontal",
    "steps": [
      { "label": "訊號收集", "label_en": "COLLECT",   "body": "從多源捕捉原始訊號" },
      { "label": "聚合分析", "label_en": "AGGREGATE", "body": "降噪後形成假設" },
      { "label": "假設驗證", "label_en": "VALIDATE",  "body": "資料對齊歷史模式" },
      { "label": "決策行動", "label_en": "ACT",       "body": "輸出可執行決策" }
    ]
  }
}
```

**SVG anatomy** — starter: [templates/flow.svg](../templates/flow.svg)

- Canvas: standard 1280×720 dark slide. Page title at `(48, 86)` (CN) + `(48, 114)` (EN). Footer page number `(1200, 710)`.
- **Horizontal 4-step layout** (most common):
  - Each node: `240w × 180h`, `rx=16`, fill `#1A1A1A`, stroke `#333333` (1px).
  - Vertical center `y=370` (node y `280..460`).
  - Node x positions: `88, 376, 664, 952` (gap 48 between right edge and next left edge).
  - Per-node text: `01 · LABEL_EN` at `y=42` (11px, `#666666`, letter-spacing 2); `label` at `y=92` (28px weight 800 white); `body` at `y=130..150` (14px gray, wrap with `<tspan>`).
  - Arrows: `<line>` between node edges with `marker-end="url(#flowArrow)"`. x1 = node_right + 4, x2 = next_node_left − 4. y=370.
  - Arrowhead marker (in `<defs>`): `markerUnits="userSpaceOnUse", markerWidth=12, markerHeight=9, refX=11, refY=4.5, orient=auto`, path `M0,0 L12,4.5 L0,9 Z`, fill `#666666`. (`userSpaceOnUse` keeps the head 12×9px regardless of stroke width — the default strokeWidth units blow a 2px-stroke arrow up to a 20px head, half the connector's length.)
- **Highlight**: by default the last node uses highlight-color stroke (2px), highlight-color label_en + label text, plus a highlight-color arrow leading INTO it. Override via `highlight_index` (0-indexed).
- **Terminal**: arrows connect node→node only — the last node has **no trailing arrow**, it IS the terminus (a static `flow` is already correct here). The "swallowed last node" failure only appears when a single rail carries a *trailing* head past the final station (the `transit_rail` motion composition); its fix is in [prompts/05 Step 5.7](../prompts/05_designer_svg.md). **Invariant for any flow/rail:** a terminal symbol never overlaps the terminal node, and no head points past the last node when that node is the destination.
- **For 3 nodes**: each node `320w`, x = `88, 472, 856`, gap 64.
- **For 5 nodes**: each node `192w`, x = `88, 332, 576, 820, 1064`, gap 52, body line cap = 1 line.
- **For 6+ nodes**: do not render. Split into two pages (3+3) or downgrade to bento `mini_grid`.
- **Vertical orientation** (`orientation: "vertical"`): nodes stacked, each `360w × 80h` centered on `x=640`, y positions `170, 270, 370, 470, 570` (gap 20). Connect with vertical arrows at `x=640`.
- **Fan-in / fan-out variant (hub)** — when N sources feed ONE target (or one source feeds N targets), arrowhead crowding is the failure mode. Geometry (canonical here; applies to static pages and to `motion: "hub"` animated pages alike):
  - **≤3 sources**: connect each directly, but spread the anchor points along the target's edge — **32px between arrowheads preferred, 24px floor**. Three anchors on a 180px node edge: y = center−50, center, center+50.
  - **≥4 sources**: never land 4+ arrowheads on one edge. Branches **merge into a single trunk** before the target (tributary curves joining at one point, then a straight trunk) — only ONE arrowhead reaches the target. Alternatively drop sources onto a shared bus line.
  - **Fan-out**: mirror the same rules (one trunk leaving the source, splitting into branches; or ≤3 direct edges from spread anchors).
  - Keep all flows in roughly the same direction — head-on opposing arrows on parallel paths read as chaos.

---

## 2. `timeline` — events anchored to time

```
●─────●─────●─────●─────●──────▶
2021  2022  2023  2024  2025
 ┊     ┊     ┊     ┊     ┊
 上市  併購  轉型  服務  IPO
```

**Identity**: events placed at specific points on a time axis.

**Use when**: company milestones (年份), quarterly progress, roadmap by date, project schedule with dated events.

**Don't use when**:
- Abstract steps without time → `flow`
- One dominant date is the whole story → `stat_hero`
- Multiple parallel tracks over time → consider `compare_table` with time as columns

**Common confusion**: "Q1 計劃 / Q2 計劃 / Q3 計劃 / Q4 計劃" = timeline (anchored to quarters). "需求收集 / 設計 / 開發 / 上線" = `flow` (abstract steps, no real dates).

**Schema**:
```json
{
  "layout": "timeline",
  "timeline_data": {
    "orientation": "horizontal",
    "events": [
      { "time": "2021", "label": "上市",   "body": "於港交所掛牌" },
      { "time": "2022", "label": "戰略併購", "body": "整合 AIoT 平台供應商" },
      { "time": "2023", "label": "業務轉型", "body": "服務收入占比首破 20%" },
      { "time": "2024", "label": "服務拐點", "body": "服務營收首次超越硬體" },
      { "time": "2025", "label": "IPO 分拆", "body": "服務事業獨立上市" }
    ]
  }
}
```

**SVG anatomy** — starter: [templates/timeline.svg](../templates/timeline.svg)

- Canvas: standard 1280×720 dark slide. Page title at `(48, 86)` / `(48, 114)`.
- **Horizontal axis line**: `<line x1="120" y1="420" x2="1160" y2="420" stroke="#333333" stroke-width="2"/>`. The axis spans the full diagram width.
- **Event dots on the axis** at `y=420`. Dot positions by event count:
  - 4 events: x = `184, 488, 792, 1096` (gap 304)
  - 5 events: x = `144, 392, 640, 888, 1136` (gap 248)
  - 6 events: x = `124, 326, 528, 730, 932, 1134` (gap ~202)
  - 7+ events: split or compress.
- **Per-event text stack** (centered on dot's x):
  - `time` label at `y=382` (18px weight 700, `#A0A0A0` — or highlight on the highlighted event)
  - Dot at `y=420`: non-highlighted = `r=8` fill `#1A1A1A` stroke `#A0A0A0` 2px; highlighted = `r=12` fill highlight stroke highlight.
  - `label` at `y=462` (20px weight 800, white — or highlight)
  - `label_en` at `y=488` (12px, `#A0A0A0` — or highlight, letter-spacing 1)
  - `body` at `y=510` (14px, `#A0A0A0`); wrap to `y=510 + y=530` only if necessary.
- **Highlight**: by default the last event (most recent). Override via `highlight_index`.
- **Vertical orientation** (`orientation: "vertical"`): axis `<line x1="640" y1="180" x2="640" y2="640" />`, dots at `y = 200, 308, 416, 524, 632` for 5 events. Time label LEFT of dot, label/body RIGHT.

---

## 3. `cycle` — iterative process with no endpoint

```
        ┌───────────┐
        │   Plan    │
        └─────┬─────┘
              │
   ┌──────────┘
   ▼                  ┌───────────┐
┌──────┐              │   Act     │◀──┐
│ Act  │              └───────────┘   │
└──┬───┘                              │
   ▼                                  │
┌──────────┐    ┌───────────┐    ┌────┴──────┐
│  Check   │───▶│   Do      │    │  Check    │
└──────────┘    └───────────┘    └───────────┘
              (4-stage clockwise loop)
```

**Identity**: process that returns to its start; no terminal state.

**Use when**: PDCA, OODA loop, design thinking, feedback loop, retrospective cycle, anything where "iteration" is the point.

**Don't use when**:
- One-way process with terminal output → `flow`
- 6+ stages — loop becomes unreadable, downgrade to `flow` with a "return to step 1" note
- Linear iterations of one specific task (use stat instead)

**Common confusion**: "需求 → 設計 → 開發 → 部署" is `flow` (terminal output). "規劃 → 執行 → 檢視 → 改進 → 規劃..." is `cycle` (returns to start, that's the point).

**Motion note**: because a true cycle *returns to its start*, the rotation itself can be the message — a core cycle page may carry `motion: "orbit"` (the planner's call, decided in [prompts/04_planning_draft.md](../prompts/04_planning_draft.md) → "Motion pages"; the ring must be built from open `<path>` arcs, never a closed `<circle>`, per Step 5.7). This is the one "iteration, not throughput" shape that still qualifies for motion. Still bound by the deck's 2–3-page motion budget; an animated cycle slide ships as a GIF and loses Convert-to-Shape.

**Schema**:
```json
{
  "layout": "cycle",
  "cycle_data": {
    "direction": "clockwise",
    "center_label": "PDCA",
    "center_label_en": "CONTINUOUS · LOOP",
    "stages": [
      { "label": "規劃", "label_en": "PLAN",  "body": "設定目標與假設" },
      { "label": "執行", "label_en": "DO",    "body": "小規模試行" },
      { "label": "檢視", "label_en": "CHECK", "body": "對照結果與假設" },
      { "label": "改進", "label_en": "ACT",   "body": "調整後進入下一輪" }
    ]
  }
}
```

**SVG anatomy** — starter: [templates/cycle.svg](../templates/cycle.svg)

- Canvas: standard 1280×720 dark slide. Page title at `(48, 86)` / `(48, 114)`.
- **Cycle geometry**: center `(640, 410)`. 4 stages at compass positions; node centers on radius 180:
  - Top: `(640, 230)` → node `x=560..720, y=180..280`
  - Right: `(820, 410)` → node `x=740..900, y=360..460`
  - Bottom: `(640, 590)` → node `x=560..720, y=540..640`
  - Left: `(460, 410)` → node `x=380..540, y=360..460`
- **Each node**: `160w × 100h`, `rx=14`, fill `#1A1A1A`, stroke `#333333` (1px). Stage text stack: `LABEL_EN` at `y=30` (11px gray, letter-spacing 2), `label` at `y=62` (22px weight 800 white), `body` at `y=84` (14px gray).
- **Curved arrows** (clockwise direction by default): cubic Bezier path between adjacent nodes, with `marker-end="url(#cycleArrow)"`. Exact paths (clockwise):
  - Top→Right: `M 720 252 C 778 252, 820 296, 820 360`
  - Right→Bottom: `M 820 460 C 820 524, 778 568, 720 568`
  - Bottom→Left: `M 560 568 C 502 568, 460 524, 460 460`
  - Left→Top: `M 460 360 C 460 296, 502 252, 560 252`
  - For `direction: "counter_clockwise"`, reverse the M/end points of each path.
- **Center label**: render `cycle_data.center_label` at `(640, 395)` (34px weight 900, highlight color, letter-spacing 2). Optional `center_label_en` at `(640, 430)` (13px gray, letter-spacing 2). Planner must provide `center_label` for the cycle framework name (e.g. "PDCA", "OODA") — Designer must not invent it from the page title.
- **Highlight**: by default the last stage (the "act" / "improve" stage). Override via `highlight_index`.
- **For 3 stages**: positions at 0°, 120°, 240° from top — `(640, 230)`, `(796, 480)`, `(484, 480)` (radius 180). Three curved arrows.
- **For 5+ stages**: cycle becomes cramped — downgrade to `flow` with a "loops back to step 1" note.

---

## 4. `funnel` — stage-by-stage quantity decrease

```
   ┌──────────────────────────┐
   │   訪客  1,000,000        │  ← top stage = widest
   └──────────────────────────┘
      ┌──────────────────┐
      │  註冊  120,000   │
      └──────────────────┘
         ┌────────────┐
         │ 試用 24,000 │
         └────────────┘
            ┌──────┐
            │付費 3,200│
            └──────┘
```

**Identity**: stages where each subsequent stage carries *less quantity* than the prior. Visual width = quantity.

**Use when**: marketing funnel, sales pipeline, conversion stages with numeric drop-off.

**Don't use when**:
- Equal-importance stages with no quantity drop → `flow`
- No quantitative measurement at each stage → `flow`
- Stages where quantity *increases* (use a reverse-funnel? rare — usually `flow` or `chart_bar` is better)

**Common confusion**: "認識 → 興趣 → 考慮 → 購買" *without numbers* is `flow`. With numbers showing drop-off it's `funnel`. The numeric drop is the point of the visual.

**Schema**:
```json
{
  "layout": "funnel",
  "funnel_data": {
    "unit": "人",
    "stages": [
      { "label": "訪客", "label_en": "VISITORS", "value": 1000000 },
      { "label": "註冊", "label_en": "SIGNUP",   "value": 120000 },
      { "label": "試用", "label_en": "TRIAL",    "value": 24000 },
      { "label": "付費", "label_en": "PAID",     "value": 3200 }
    ],
    "show_conversion_rate": true
  }
}
```

**SVG anatomy** — starter: [templates/funnel.svg](../templates/funnel.svg)

- Canvas: standard 1280×720 dark slide. Page title at `(48, 86)` / `(48, 114)`.
- **Funnel geometry** for 4 stages: stacked trapezoids centered on `x=640`. Widths narrow linearly from top (880) to bottom (240), step Δ=160.
  - Stage 1: top w=880, bottom w=720, y `160..274` — path `M 200 160 L 1080 160 L 1000 274 L 280 274 Z`
  - Stage 2: top w=720, bottom w=560, y `282..396` — path `M 280 282 L 1000 282 L 920 396 L 360 396 Z`
  - Stage 3: top w=560, bottom w=400, y `404..518` — path `M 360 404 L 920 404 L 840 518 L 440 518 Z`
  - Stage 4: top w=400, bottom w=240, y `526..640` — path `M 440 526 L 840 526 L 760 640 L 520 640 Z`
- **Stage fill**: `#1A1A1A`. **Stroke**: highlight color with alpha fading top→bottom (`0.40, 0.60, 0.80, 1.0` for 4 stages, stroke-width 1.5; last stage stroke-width 2.5). This makes the conversion goal pop.
- **Per-stage text** (centered on `x=640`):
  - `LABEL_EN` (e.g. `01 · VISITORS`) at top of trapezoid (11px gray, letter-spacing 2)
  - `label + value` (e.g. `訪客  1,000,000`) at vertical middle of trapezoid (28–34px weight 900, scaling DOWN as the trapezoid narrows). Stages 1→4: 34px, 32px, 30px, 28px. Stage 4 in highlight color.
- **Conversion rate labels** (when `show_conversion_rate: true`): between each pair of stages, right-anchored just outside the funnel. Format: `↓  12.0%`. 13px gray.
- **Overall conversion summary** (top-right corner of slide, aligned to title baseline): `總轉化率` label at `(1232, 88)` right-anchored (13px gray, letter-spacing 2) above the big number at `(1232, 122)` right-anchored (28px weight 900 highlight color). Placing the summary in the title row (instead of the bottom corner) keeps the standard page-number position at `(1200, 710)` free, consistent with every other primitive page in the deck.
- **For 5 stages**: widths `880 → 720 → 560 → 400 → 240 → 80` — that's a 5-step linear narrowing, but the bottom 80-wide segment will be too narrow for legible text. Prefer 4 stages; if you must have 5, use narrowing `880 → 752 → 624 → 496 → 368 → 240` (Δ=128).
- **Highlight**: bottom stage (the conversion goal) always — funnels are intrinsically about the goal at the bottom.

---

# Alignment primitive

## 5. `compare_table` — multi-option × multi-dimension matrix

```
+---------------+--------+---------+---------+
| 維度           |  方案A  |  方案B  |  方案C  |
+---------------+--------+---------+---------+
| 起始成本       |   低    |   中    |   高    |
| 上線時間       |  3 月   |  2 月   |  6 月   |
| 擴展性         |   中    |   高    |   高    |
| 維運複雜度     |   低    |   中    |   高    |
+---------------+--------+---------+---------+
```

**Identity**: row-by-row alignment is the point — each row is one shared dimension; each column is one option.

**Use when**: vendor comparison, plan comparison (basic/pro/enterprise), competitive analysis with consistent criteria, before/after across multiple dimensions.

**Don't use when**:
- 2 items without shared dimensions → `two_col_50_50`
- Single dimension across options → `chart_bar`
- 6+ columns or 6+ rows — table becomes unreadable, restructure
- Items genuinely don't share criteria (don't fabricate dimensions to fit the table)

**Common confusion**: "Pros vs Cons" laid out as two free-text columns is `two_col_50_50`. "Pros vs Cons" *with row-by-row corresponding points* (each pro on row N has a matched con on the same row) is `compare_table` with 2 columns.

**Schema**:
```json
{
  "layout": "compare_table",
  "table_data": {
    "columns": [
      { "label": "方案A", "label_en": "OPTION A" },
      { "label": "方案B", "label_en": "OPTION B" },
      { "label": "方案C", "label_en": "OPTION C" }
    ],
    "rows": [
      { "dimension": "起始成本",   "dimension_en": "UPFRONT COST",  "cells": ["低", "中", "高"] },
      { "dimension": "上線時間",   "dimension_en": "TIME TO LIVE",  "cells": ["3 月", "2 月", "6 月"] },
      { "dimension": "擴展性",     "dimension_en": "SCALABILITY",   "cells": ["中", "高", "高"] },
      { "dimension": "維運複雜度", "dimension_en": "OPS COMPLEXITY","cells": ["低", "中", "高"] }
    ],
    "highlight_column": 1
  }
}
```

**SVG anatomy** — starter: [templates/compare_table.svg](../templates/compare_table.svg)

- Canvas: standard 1280×720 dark slide. Page title at `(48, 86)` / `(48, 114)`.
- **Grid bounds**: `x=88..1192` (w=1104), `y=160..640` (h=480). Outer border: `<rect rx="14" stroke="#333333">`.
- **Column widths** (1 dimension + N options):
  - Dimension column always w=282 (left).
  - N=2 options: option cols each w=411
  - N=3 options: option cols each w=274
  - N=4 options: option cols each w=205
  - N≥5 options: too narrow, downgrade or split.
- **Row heights**:
  - Header row: 52px (`y=160..212`).
  - Data rows: split remaining 428px evenly. For 4 rows: 107px each. For 3 rows: 142px. For 5 rows: 85px.
- **Horizontal row separators**: `<line stroke="#333333" stroke-width="1">` between rows. No vertical column separators (keeps the layout airy).
- **Highlighted column** (when `highlight_column` is set): background `<rect>` fill = `highlight-color` at 0.08 alpha, spanning the full column height. Header text and cell values in that column use highlight color.
- **Header text** (each option column header, centered):
  - Option label: 20px weight 800, white (or highlight for the highlighted column).
  - Dimension column header: small caps `維度  ·  DIMENSION` left-aligned at `x=116`, `y=194`, 13px gray.
- **Cell content**:
  - Dimension cell (left column): primary CN label `rows[i].dimension` (17px weight 500, `#A0A0A0`, left-anchored at `x=116`). Optional EN subline `rows[i].dimension_en` (12px `#666666`, letter-spacing 1, ~22px below). Skip the EN subline if not provided — same selective-density rule as `stat_caption_en`.
  - Value cells (option columns): 19px weight 700, centered horizontally on column center, vertically centered in row. White for normal, highlight color for highlighted column.
- **Cell value brevity**: each value ≤6 Chinese chars or ≤3 EN words. For longer values, downgrade to a non-table layout — the comparison breaks if cells need to wrap.
- **Highlight**: default to no highlighted column (just neutral comparison); when `highlight_column` is set, that column is the recommended option.

---

# Topology primitives

## 6. `hierarchy_tree` — branching parent-child structure

```
                  +-------+
                  |  CEO  |
                  +---+---+
        ┌─────────────┼─────────────┐
        │             │             │
    +---+----+    +---+----+    +---+----+
    | VP 工程 |    | VP 業務 |    | VP 財務 |
    +---+----+    +---+----+    +---+----+
       │            │
   ┌───┴───┐    ┌───┴───┐
   │       │    │       │
 ┌─┴──┐ ┌─┴──┐┌─┴──┐ ┌─┴──┐
 │平台│ │產品││大型│ │中小│
 └────┘ └────┘└────┘ └────┘
```

**Identity**: tree of parent → child relationships, possibly multi-layer.

**Use when**: org chart, product family tree, taxonomy / classification, decision tree, file/system hierarchy.

**Don't use when**:
- Items are peers with no parent → `mini_grid`
- Strict layer count where layer **thickness** matters (Maslow-style) → `pyramid`
- Just two levels with 4–5 children — bento `hero_top` is enough (no topology to preserve beyond "one boss + N reports")

**Common confusion**: "CEO + 4 直屬副總" is `hero_top` (one-deep, no real topology to preserve). "CEO → 4 VPs → 12 directors with cross-team links" is `hierarchy_tree`.

**Schema**:
```json
{
  "layout": "hierarchy_tree",
  "tree_data": {
    "orientation": "vertical",
    "root": {
      "label": "CEO",
      "children": [
        { "label": "VP 工程", "children": [
          { "label": "平台" }, { "label": "產品" }
        ]},
        { "label": "VP 業務", "children": [
          { "label": "大型" }, { "label": "中小" }
        ]},
        { "label": "VP 財務" }
      ]
    }
  }
}
```

**SVG anatomy** — starter: [templates/hierarchy_tree.svg](../templates/hierarchy_tree.svg)

- Canvas: standard 1280×720 dark slide. Page title at `(48, 86)` / `(48, 114)`.
- **Vertical orientation** (root at top, default). 3-layer geometry:
  - Layer 1 (root): 1 node at `(540, 160)` to `(740, 240)` (200w × 80h, center x=640).
  - Layer 2 (children of root): 3 nodes at x-centers `256, 640, 1024`, each 200w × 80h, y `340..420`.
  - Layer 3 (grandchildren): up to 6 leaves at x-centers `170, 342, 554, 726, 938, 1110`, each 160w × 80h, y `520..600`.
- **Right-angle connectors** (draw before nodes so nodes overlay):
  - Layer 1 → Layer 2: vertical from root bottom `(640, 240) → (640, 290)`; horizontal branch at `y=290` from `x=256` to `x=1024`; verticals from each L2 x to `y=340`.
  - Layer 2 → Layer 3 (per L2 parent): vertical from parent bottom `(parent_x, 420) → (parent_x, 470)`; horizontal branch at `y=470` spanning the parent's two children's x's; vertical down to each leaf top at `y=520`.
- **Connector stroke**: `#333333` 1.5px for non-highlighted branches; **highlight color 2px for the highlighted branch** (Layer 1 → L2 child → L3 grandchildren) when a branch path is specified via `highlight_path` (e.g., `[0, 1, 0]` = root → 2nd L2 node → 1st L3 node).
- **Per-node text**:
  - Root: `LEVEL 1` (10px) + label (22px weight 800). Highlighted by default (highlight-color stroke 2px, highlight text).
  - L2 nodes: `LEVEL 2` (10px) + label (20px weight 700).
  - L3 nodes: `LEVEL 3` (10px) + label (17px weight 600).
- **Horizontal orientation** (`orientation: "horizontal"`, root at left): rotate the layout 90° — root at `(60, 360)`, L2 nodes at y-centers `200, 360, 520` with x-center `380`, etc. Use this for wide-shallow trees (few layers, many siblings).
- **Caps**: 3 layers max; ~12 leaf nodes max. Beyond that, abstract into sub-trees on separate pages.

---

## 7. `pyramid` — layered foundation→apex with size meaning

```
                  /\
                 /  \
                /apex\
               /------\
              /  上層  \
             /----------\
            /    中層    \
           /--------------\
          /     底基層      \
         /------------------\
```

**Identity**: stacked horizontal layers where **each layer supports the next** and visual thickness/area carries meaning (foundation is biggest, apex is narrowest).

**Use when**: Maslow's hierarchy, "下層支撐上層" type arguments, capability stack where lower layers enable upper, decision-making frameworks (data → information → knowledge → wisdom).

**Don't use when**:
- Branching tree → `hierarchy_tree`
- Layers don't actually support each other (just sequential) → `flow`
- 5+ layers (becomes unreadable; restructure to 3–4)

**Common confusion**: org chart = `hierarchy_tree` (branching). "Foundation → walls → roof" = `pyramid` (each enables next; reading from bottom up). Same number of items, different shape because the relationship is different.

**Schema**:
```json
{
  "layout": "pyramid",
  "pyramid_data": {
    "direction": "bottom_up",
    "layers": [
      { "label": "原始資料層",   "body": "感測器 + 日誌 + 第三方資料" },
      { "label": "結構化資料層", "body": "ETL 後可查詢" },
      { "label": "洞察層",       "body": "BI 報表與模型輸出" },
      { "label": "決策層",       "body": "驅動產品與戰略選擇" }
    ]
  }
}
```

**SVG anatomy** — starter: [templates/pyramid.svg](../templates/pyramid.svg)

- Canvas: standard 1280×720 dark slide. Page title at `(48, 86)` / `(48, 114)`.
- **Pyramid geometry** for 4 layers (each layer N's top width = layer N+1's bottom width, so layers connect seamlessly):
  - Foundation (bottom): bottom w=800, top w=600, y `500..600` — path `M 240 600 L 1040 600 L 940 500 L 340 500 Z`
  - Layer 2: bottom w=600, top w=400, y `400..500` — path `M 340 500 L 940 500 L 840 400 L 440 400 Z`
  - Layer 3: bottom w=400, top w=200, y `300..400` — path `M 440 400 L 840 400 L 740 300 L 540 300 Z`
  - Apex (top): bottom w=200, top w=80, y `200..300` — path `M 540 300 L 740 300 L 680 200 L 600 200 Z`
- **Layer fill**: `#1A1A1A`. **Layer stroke**: `#333333` 1.5px for normal layers; **highlight color 2.5px for the highlighted layer**.
- **Per-layer text** (centered on `x=640`, vertical center of each layer):
  - Foundation (y_mid 550): label 18px weight 700 white at `y=544`, body 14px gray at `y=572`.
  - Layer 2 (y_mid 450): same sizes at `y=444` / `y=472`.
  - Layer 3 (y_mid 350): same at `y=344` / `y=372`.
  - Apex (y_mid 250): smaller because the layer is narrow — label 16px weight 800 (highlight color) at `y=258`, optional small EN at `y=280` (11px, letter-spacing 1).
- **Side annotations** (optional, indicates reading direction):
  - Left side label at `y=558` (`FOUNDATION` in gray, 11px letter-spacing 2) and `y=258` (`APEX` in highlight color).
  - Upward arrow on the left margin: `<line x1="120" y1="540" x2="120" y2="280" marker-end="url(#pyramidArrow)">`.
- **For 3 layers** (more common): widths bottom→top `800, 540, 280, 80`; layer heights 140; y bands `200..340`, `348..488`, `496..636`.
- **For 5 layers**: each layer 80h, top w = 0 — apex becomes a point with no text. Avoid 5 — restructure to 3–4 layers or downgrade to `hierarchy_tree`.
- **Direction**:
  - `bottom_up` (default): foundation reads first, apex is the headline/goal. Highlight apex.
  - `top_down`: apex reads first, foundation is the underlying detail. Highlight apex still, but the reading order in the layer data is reversed.

---

# Axis primitives

## 8. `quadrant_2x2` — two-axis positioning

```
       高 │
          │    第二象限          第一象限
          │   (低成本高品質)    (高成本高品質)
          │       ● A                ● B
          │
          │  ──────────┼──────────  品質
          │
          │       ● C                ● D
          │   (低成本低品質)    (高成本低品質)
       低 │    第三象限          第四象限
          └──────────────────────────────▶
          低                            高    成本
```

**Identity**: items positioned on a 2D plane with two independent, meaningful axes.

**Use when**: BCG matrix (growth × share), Eisenhower matrix (urgency × importance), market positioning (price × quality), strategy 2×2 frameworks.

**Don't use when**:
- Only one axis matters → `chart_bar` (ranking) or stat
- Axes are arbitrary or for decoration → use comparison instead
- 8+ items on the plane → too crowded; restructure or split

**Common confusion**: "high/low" as a single dimension is not a quadrant — that's a one-axis ranking. Quadrant requires *two* independent axes where item position on both is meaningful.

**Schema**:
```json
{
  "layout": "quadrant_2x2",
  "quadrant_data": {
    "x_axis": { "label": "市占率", "low": "低", "high": "高" },
    "y_axis": { "label": "成長率", "low": "低", "high": "高" },
    "quadrant_labels": {
      "top_left":     "問號 (Question)",
      "top_right":    "明星 (Star)",
      "bottom_left":  "瘦狗 (Dog)",
      "bottom_right": "金牛 (Cash Cow)"
    },
    "items": [
      { "label": "產品線 A", "x": 0.8, "y": 0.7 },
      { "label": "產品線 B", "x": 0.3, "y": 0.9 },
      { "label": "產品線 C", "x": 0.6, "y": 0.2 },
      { "label": "產品線 D", "x": 0.2, "y": 0.2 }
    ]
  }
}
```

`x` / `y` are normalized to 0.0–1.0 (Planner can use semantic positions; Designer maps to canvas coordinates).

**SVG anatomy** — starter: [templates/quadrant_2x2.svg](../templates/quadrant_2x2.svg)

- Canvas: standard 1280×720 dark slide. Page title at `(48, 86)` / `(48, 114)`.
- **Plot bounds**: `x=200..1080` (w=880), `y=200..620` (h=420). Origin (axes intersect) at `(640, 410)`.
- **Axes**: cross lines through origin, `<line stroke="#333333" stroke-width="1.5"/>`. X spans `200..1080` at y=410; Y spans `200..620` at x=640.
- **Axis labels**:
  - X-axis label: right-aligned just below the x-axis at `x=1080, y=438` (13px gray), with `▶` glyph. Format: `<axis>  (Share)  ▶`.
  - Y-axis label: just above origin, at `x=652, y=208` (13px gray), with `▲` glyph.
  - Low/High markers: 11px gray letter-spacing 1 — `LOW` at start, `HIGH` at end of each axis.
- **Normalized coordinates**: `quadrant_data.items[].x` and `.y` are 0..1. Canvas mapping:
  - `canvas_x = 200 + x * 880`
  - `canvas_y = 620 - y * 420` (inverted — high y means up)
- **Quadrant labels**: 11px weight 500 letter-spacing 2, in the upper-inside corner of each quadrant.
  - Top-left (Q2): `x=220, y=226` (anchor start)
  - Top-right (Q1): `x=1060, y=226` (anchor end)
  - Bottom-left (Q3): `x=220, y=608`
  - Bottom-right (Q4): `x=1060, y=608` (anchor end)
- **Highlighted quadrant** (`highlight_quadrant`): light tint background — `<rect>` filling that quadrant's bounding box with `fill=highlight, fill-opacity=0.05`. Quadrant label uses highlight color. Default: `top_right` (the "good" quadrant in BCG / Eisenhower).
- **Items**: `<circle r="9">` filled in highlight color if inside the highlighted quadrant, else white at fading alpha (0.65 in 2nd/3rd quadrants, 0.45 in worst quadrant). Label 15px weight 600 white, anchored to the right of the dot (`x = dot_x + 18, y = dot_y + 4`).
- **Cap**: ~8 items max — beyond that, label overlap becomes unmanageable. If items cluster, optionally shift label position around the dot (above, below, left, right) to avoid overlap.

---

## 9. `venn` — set overlap

```
        +---+ A          B +---+
       /     \            /     \
      |       \   ┌──┐   /       |
      |   A    ╲ │ ∩  │ ╱    B   |
      |  only   ╳│    │╳   only  |
      |        ╱  └──┘  ╲         |
       \      /          \       /
        +---+              +---+
```

**Identity**: 2–3 sets where the overlap regions carry the point.

**Use when**: ideal candidate (technical × business × communication), 3-circle overlap frameworks, "both X and Y" arguments where the intersection is what matters.

**Don't use when**:
- No actual overlap (use `compare_table` instead)
- 4+ sets — Venn becomes unreadable beyond 3 circles
- The overlap isn't the point (use `mini_grid` for parallel listing of set members)

**Common confusion**: listing three skill categories side-by-side is `three_col`. Drawing those three categories as overlapping circles to highlight "the ideal candidate sits in the intersection" is `venn`.

**Schema**:
```json
{
  "layout": "venn",
  "venn_data": {
    "sets": [
      { "label": "技術能力", "body": "深度技術經驗" },
      { "label": "業務理解", "body": "讀懂市場與成本" },
      { "label": "溝通能力", "body": "向上下傳遞清晰決策" }
    ],
    "intersections": {
      "all":  { "label": "理想人選", "body": "三能力交集的全棧領導" },
      "01":   { "label": "業務型技術主管" },
      "02":   { "label": "技術型業務 PM" },
      "12":   { "label": "面向業務的職能主管" }
    }
  }
}
```

Intersection keys: `"all"` = all sets overlap; `"01"` = sets 0 and 1 only; etc. Optional — Designer only labels intersections that are specified.

**SVG anatomy** — starter: [templates/venn.svg](../templates/venn.svg)

- Canvas: standard 1280×720 dark slide. Page title at `(48, 86)` / `(48, 114)`.
- **3-set Venn geometry** (equilateral arrangement, radius 180, side 240):
  - Set 0 (top): center `(640, 280)`
  - Set 1 (bottom-left): center `(520, 488)`
  - Set 2 (bottom-right): center `(760, 488)`
- **Each circle**: `<circle r="180" stroke="#FF6900" stroke-width="1.5" fill="#FF6900" fill-opacity="0.10"/>`. Low-alpha fill so overlap regions naturally darken (additive alpha effect).
- **Set labels** (outside each circle, 20px weight 800 white + 12px gray subtitle below):
  - Set 0 (top circle): centered above at `(640, 78)` + `(640, 146)` for subtitle.
  - Set 1: left of bottom-left circle at `(280, 592)` + `(280, 616)`.
  - Set 2: right of bottom-right circle at `(1000, 592)` + `(1000, 616)`.
- **Intersection labels** (centered inside each overlap region):
  - `"all"` (3-way intersection): `(640, 416)` — highlight color, 18px weight 800, with optional EN line at `(640, 438)` (11px highlight, letter-spacing 2). This is the typical headline.
  - `"01"` (Set 0 ∩ Set 1 only): `(455, 380)`, 13px gray.
  - `"02"` (Set 0 ∩ Set 2 only): `(825, 380)`, 13px gray.
  - `"12"` (Set 1 ∩ Set 2 only): `(640, 534)`, 13px gray.
  - Labels are optional — only render the keys provided in `venn_data.intersections`.
- **2-set Venn variant** (when `venn_data.sets.length === 2`):
  - Set 0 center: `(520, 410)`, Set 1 center: `(760, 410)`, radius 180.
  - Intersection `"01"` at `(640, 410)` — highlight color.
  - Set 0 label outside left at `(280, 414)` (right-anchored); Set 1 label outside right at `(1000, 414)` (left-anchored).
- **Cap**: 4+ sets becomes geometrically infeasible. If the data requires 4+ sets, restructure to `compare_table` or two pages.

---

## Motion (flow-anim) — what must NEVER animate

A page may animate only when planning sets a `motion` field (decision flow in [prompts/04_planning_draft.md](../prompts/04_planning_draft.md); construction recipes and numeric rules in [prompts/05_designer_svg.md](../prompts/05_designer_svg.md) Step 5.7). Regardless of how tempting, these shapes never carry `flow-anim`:

- **Closed dashed shapes** (alert boxes, dashed borders) — animated, they become marching-ants selection boxes. This is the #1 trap: `dual_alert_panels` dashed boxes are already dashed strokes. (An orbit / cycle ring is **not** an exception — build it from open `<path>` arcs, never a closed `<circle>`, so the open-path rule still holds.)
- **The timeline axis** — events are discrete points in time; the 1040px axis is the single most tempting line in the template library. Resist.
- **Funnel strokes** — a funnel tells a quantity story, not a flow story (and the stages are fills).
- **Sequence-diagram message arrows** — discrete calls. Only a genuinely streaming channel qualifies (and that's a `motion` decision in planning, not a designer impulse).
- **`split_style_duel` bridge capsules** — before/after is a discrete transition.
- **`hierarchy_tree` / `compare_table` connectors** — too many short segments; dense diagrams stay static.
- **The `tapered_swoosh`** — it is atmosphere (a gradient fill), not a line; it cannot dash and must not be promoted to a foreground actor.

## Cross-references

- Detection logic and the 4 information-loss signals → [prompts/04_planning_draft.md → Primitive layouts](../prompts/04_planning_draft.md)
- Bento layouts (the default base language) → [bento_grid.md](bento_grid.md)
- Chart layouts (`chart_bar` / `chart_line` / `chart_donut`) — these are technically primitives too, but legacy from before this framework; treat them as additional "data-shape" primitives with the same bento-first discipline → [chart_anatomy.md](chart_anatomy.md)
- Color and motif → [design_system.md](design_system.md)

## Anti-pattern reminder

If you find yourself reaching for a primitive because "this deck has too many bento pages in a row" — stop. Repetition of bento is a feature (shared language across the deck), not a bug. Switch to a primitive only when one of the 4 loss signals fires on *that specific page*. The deck's coherence depends on this discipline.
