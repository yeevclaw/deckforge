# Design System — palettes, typography, motifs

This is the lookup table the Designer prompt uses to resolve `palette_hint`, `motif_hint`, and `typography_hint`.

## Palettes

DeckForge ships four **palette families**: the IT-prism light style (**the default** — cool lavender-mint canvas, single green accent, slate structure), the corporate-fresh light style (on request — warm consulting look: green gradient structure, orange inline emphasis), dark Apple-style (single highlight color on black — pick on request, or propose it for overwhelmingly stat-heavy decks), and traditional light themes.

### Dark Apple family (on request — the dark, data-dense pick)

Pure black background, dark gray cards, one bold highlight color drawn from the brand or topic. Single-color discipline: that highlight carries 100% of the emphasis (no secondary or accent colors). Inspired by Apple keynote slides and the linux.do "Xiaomi annual report" visualization methodology. A **presenting-mode language** — number-driven drama, tiny captions; `delivery_mode: "reading"` decks resolve to a light family instead (see [references/slidedoc.md](slidedoc.md) §8).

| Hint key | Highlight | Best for |
|---|---|---|
| `dark_apple` | auto — pick brand color from content (e.g. Xiaomi `#FF6900`, Tesla `#E31937`, Anthropic `#D97757`); fallback `#FFA500` bright orange | The family's base hint — data-/stat-heavy decks, annual reports, product launches, financial summaries |
| `dark_apple_blue` | `#00AEEF` tech blue | Tech / SaaS / enterprise software |
| `dark_apple_orange` | `#FFA500` bright orange | Energy, launch, consumer-tech |
| `dark_apple_green` | `#00C277` Spotify-green | Health-tech, growth narratives, sustainability with edge |
| `dark_apple_red` | `#FF3B30` Apple-red | Bold, urgent, statement decks |

All `dark_apple_*` variants share the same neutrals:
- Page background: `#000000` (pure black)
- Main card background: `#1A1A1A`
- Mini card background: `#222222`
- Subtle border: `#333333` (1px)
- Primary text on dark: `#FFFFFF` 100%
- Secondary text on dark: `#A0A0A0` (gray-400 equivalent)
- Tertiary / English subtitle text: `#666666` (gray-500/600)

### IT prism family (`IT_prism`) — THE DEFAULT style

**DeckForge's default: whenever the user doesn't specify a style, use this family** (`palette_hint: "IT_prism"`, `highlight_color: "#58D494"`, `motif_hint: "prism_panel_cards"`).

Cool light style modeled on a 2026 bank-IT external template system: a lavender-tinted light canvas with a soft diagonal lavender→mint wash, white panel cards with a whisper shadow, **one green accent** (`#58D494`) that lives in shapes only, and **slate** (`#344252`) carrying every structural voice — titles, card headers, hinge numbers, icons, dark anchor blocks. Covers and end pages get the family's signature **reeded glass** (vertical fluted-glass panel over gaussian-blurred color blobs); content pages get a quiet **corner bloom** top-right. Like `corporate_fresh` it argues in full-sentence assertion titles and well-set prose — but where fresh is warm (orange emphasis, pastel washes), prism is cool, technical, and quieter.

**Role palette — colors are assigned to fixed roles, never mixed freely:**

All values below were pixel-sampled from the reference template's own 顏色配置參考 page and cross-validated across its swatches — don't "round" them toward adjacent hues.

| Role | Color | Used for — and nothing else |
|---|---|---|
| Canvas | `#EFF0F3` cool light gray | page background on all content pages |
| Canvas washes | lavender `#EEEEFD` (top-left) → mint `#E7F9F1` (bottom-right) | the diagonal soft wash pair (radial blobs, opacity ≤ 0.55); at most one of each per page |
| Ink / slate | `#344252` | titles, card headings, hinge numbers, icon strokes, slate anchor blocks (white text on slate is fine — 10.3:1) |
| Body text | `#4C5A6B`; secondary `#6B7686` | paragraphs, captions — `#6B7686` is a **white-card token** (4.6:1 on white, only 4.0:1 on the wash, fails AA); any text sitting directly on the canvas/wash (page eyebrow, cover date line, footer) uses `#4C5A6B` (6.2:1) |
| **Accent green** | `#58D494`; light tier `#83E0B4`; separators `#9BD9BE` | **shapes only** — tag pills, underline bars, progress ticks, connectors, proportion bars, chart data fills, structure shapes. **Never a text fill, never a hinge number** (green on white ≈1.9:1, fails AA) |
| Emphasis highlight band | `#DDF5E8` light green | the rectangle painted BEHIND an ink-bold key phrase (the family's inline-emphasis device) |
| Gridline | `#DFE2E9` | chart gridlines, hairline rules |
| Card | `#FFFFFF` + whisper shadow (`prismShadow`: blur 10, offset 0/5, alpha 0.05) | content cards |
| Muted gray | `#909091` fills, `#DDE1E8` inactive ticks | table content fills, inactive progress ticks |
| Cover/end atmosphere | lavender-purple `#C9C6FF` circle / mint `#8AEBD2` block / cyan `#B8EEFF` haze; deep tones indigo `#848BF2`, sky `#4AB7F9` | reeded-glass cover & end pages ONLY — **none of these hues ever appears on a content page** (same rule as fresh's cover gradient) |

**Emphasis discipline (this family's equivalent of single-highlight discipline):** green is the only accent and it is a **shape voice, not a text voice**. A key phrase inside body text is marked by ink `#344252` bold **plus a green device** — a `#DDF5E8` highlight band painted behind it, a 3px `#58D494` underline bar beneath it, or a green-bordered tag pill around it (`stroke="#58D494"`, `fill="#EFFBF4"`, ink text). If green shows up as a `fill` on a `<text>` element, as a hinge number, or as a heading color, the style is broken. Slate carries structure and meaning-anchors; green carries pointing; indigo/sky/lavender stay on the cover.

**Signature components:**

```xml
<!-- Assertion title (every content page) — slate, no pill bar, no underline -->
<text x="48" y="88" font-size="34" font-weight="700" fill="#344252">標題是一句完整的主張，不是名詞短語</text>
<text x="48" y="118" font-size="16" fill="#4C5A6B">副標說明文字（可省略）— 直接坐在畫布上，用 #4C5A6B 不用 #6B7686</text>

<!-- progress_ticks — top-right page-position indicator (content pages) -->
<g>
  <rect x="1022" y="46" width="64" height="10" rx="2" fill="#58D494"/>
  <rect x="1096" y="46" width="64" height="10" rx="2" fill="#DDE1E8"/>
  <rect x="1170" y="46" width="64" height="10" rx="2" fill="#DDE1E8"/>
</g>

<!-- White panel card -->
<rect x="…" y="…" width="…" height="…" rx="14" fill="#FFFFFF" filter="url(#prismShadow)"/>
<!-- prismShadow: feGaussianBlur stdDeviation 10, offset (0,5), alpha slope 0.05 -->

<!-- slate_anchor — the dark contrast device (card header band / KPI block / hub circle) -->
<rect x="…" y="…" width="…" height="44" rx="10" fill="#344252"/>
<text x="…" y="…" font-size="20" font-weight="700" fill="#FFFFFF" text-anchor="middle">標題文字</text>

<!-- Green tag pill (inline label) — green border, ink text -->
<rect x="…" y="…" width="88" height="28" rx="6" fill="#EFFBF4" stroke="#58D494" stroke-width="1.5"/>
<text x="…" y="…" font-size="14" font-weight="600" fill="#344252" text-anchor="middle">標籤文字</text>

<!-- Inline emphasis: highlight band BEHIND ink-bold text (band first, text on top) -->
<rect x="236" y="304" width="188" height="30" rx="4" fill="#DDF5E8"/>
<text x="48" y="326" font-size="19" fill="#4C5A6B">現行流程
  <tspan font-weight="700" fill="#344252">人工覆核佔六成工時</tspan>，且錯誤率隨量增。</text>

<!-- Dashed column separator -->
<line x1="640" y1="220" x2="640" y2="600" stroke="#C9CFD9" stroke-width="2" stroke-dasharray="2 7"/>
```

**Craft recipes — where the 質感 comes from.** This family's glass vocabulary is **reeded (fluted) glass + gaussian-blurred color blobs — NOT `corporate_fresh`'s dome arches / tapered swoosh / aurora ribbons**; borrowing those makes a prism page read as a recolored fresh page. Starter templates `templates/prism_*.svg` already embed the recipes below.

*`reeded_glass`* — the cover/end signature. Behind: 2–3 large gaussian-blurred color blobs (lavender `#C9C6FF` circle, mint `#8AEBD2` rounded block, cyan `#B8EEFF` haze) on a near-white base. In front: a vertical fluted-glass panel built from evenly-spaced 1px white vertical lines (α 0.5–0.7, spacing ~18px) over a white veil (`fill="#FFFFFF"` α 0.28–0.4), so the blobs smear into soft vertical streaks. The panel occupies the right ~55% of the canvas; the title block sits on the clear left side:

```xml
<defs><filter id="blobBlur" x="-60%" y="-60%" width="220%" height="220%">
  <feGaussianBlur stdDeviation="46"/></filter></defs>
<circle cx="1120" cy="330" r="180" fill="#C9C6FF" filter="url(#blobBlur)"/>
<rect x="760" y="400" width="320" height="230" rx="18" fill="#8AEBD2" filter="url(#blobBlur)"/>
<rect x="620" y="0" width="660" height="720" fill="#FFFFFF" fill-opacity="0.32"/>
<g stroke="#FFFFFF" stroke-opacity="0.6" stroke-width="1.5">
  <line x1="638" y1="0" x2="638" y2="720"/>  <!-- repeat every ~18px across the panel -->
</g>
```

*`corner_bloom`* — the content-page atmosphere: ONE soft green radial bloom bleeding off the top-right corner (`#7CDDAB` → transparent, peak α ≤ 0.5) plus a faint white dashed rotated-square outline riding the bloom (`stroke="#FFFFFF"` α 0.5, `stroke-dasharray="5 5"`, rotated ~12°, partially off-canvas). Quiet, identical corner signature on every content page:

```xml
<defs><radialGradient id="bloomTR" cx="78%" cy="4%" r="34%">
  <stop offset="0%" stop-color="#7CDDAB" stop-opacity="0.5"/>
  <stop offset="100%" stop-color="#7CDDAB" stop-opacity="0"/>
</radialGradient></defs>
<rect width="1280" height="720" fill="url(#bloomTR)"/>
<rect x="960" y="-80" width="220" height="220" fill="none" stroke="#FFFFFF"
      stroke-opacity="0.5" stroke-dasharray="5 5" transform="rotate(12 1070 30)"/>
```

*`slate_anchor`* — the focus device (prism's counterpart of fresh's teal): the ONE element the page pivots on goes dark — a slate card-header band, a slate KPI block, the hub-center circle, the "current phase" chip. White text on slate. At most 1–2 slate anchors per page; more and the page turns heavy.

*`progress_ticks`* — the top-right page-position indicator on content pages: N horizontal ticks (64×10, rx 2), current = green `#58D494`, rest = `#DDE1E8`. N = the deck's section count (3–5); omit on cover/end.

*`blur_bloom`* — soft content-page color mass (used sparingly, e.g. behind a hero panel or as a flow mass): a gaussian-blurred mint/lavender rounded shape at α ≤ 0.35, always **edge-anchored** (bleeding off a canvas edge, never a complete floating shape). This replaces fresh's `tapered_swoosh` as the atmosphere device.

*`prism_icon`* — icons are slate line-work: Lucide skeleton scaled to 72–96px in `#344252` 2px strokes over a light cool panel (`#E4E8EF` rounded rect) with 2–3 extra detail strokes. Never blue (`#5E8FEF` is fresh's voice — blue on a prism content page breaks the cover-only rule), never green fills.

**Composition vocabulary.** The bento/diagram compositions carry over from `corporate_fresh` (same macro geometry — hero duo, orbit loop, transit pipeline, claim tree, meta bento, split duel), rendered with the prism role palette and the recipes above instead of the fresh craft: glass masses are `blur_bloom` shapes, connectors/rails are green `#58D494`/`#9BD9BE`, icons are `prism_icon` slate, emphasis anchors are `slate_anchor`. Compositions with a dedicated prism starter:

| Composition | Content shape it fits | Template |
|---|---|---|
| `prism_reeded_cover` | cover / end | `templates/prism_cover.svg` (end page: same recipe, centered CTA) |
| `prism_panel_cards` | the family's default card language | all `prism_*` bento starters below |
| flow family | 3–5 sequential steps | four variants — see the flow_variant table below |
| compare table | options × dimensions | `templates/prism_compare.svg` |

#### three_col card_variant — prism 版(值與 fresh 相同,per-page)

Card language: white panels, slate titles `#344252`, body `#4C5A6B`, green structure (`#58D494` / `#9BD9BE`), slate icons, highlight-band emphasis. The variant semantics and pick-rules are identical to the `corporate_fresh` tables below — same values, same per-page discipline, same "never for variety" rule; only the template files differ:

| `card_variant` | Template |
|---|---|
| `icon_column` (default) | `templates/prism_3col.svg` |
| `numbered_steps` | `templates/prism_3col_steps.svg` |
| `axis_labeled` | `templates/prism_3col_axis.svg` |
| `lead_plus_pair` | `templates/prism_3col_lead.svg` |

#### mini_grid card_variant — prism 版

Numbers are **slate `#344252`** (never green — a green number is a text fill of the accent, the family's cardinal sin) with `tabular-nums`. Proportion bars and accent rules are green.

| `card_variant` | Template |
|---|---|
| `even_grid` (default) | `templates/prism_mini_grid.svg` |
| `ribbon_row` | `templates/prism_mini_grid_ribbon.svg` |
| `spotlight` | `templates/prism_mini_grid_spotlight.svg` |

#### two_col_50_50 card_variant — prism 版

| `card_variant` | Template |
|---|---|
| `balanced` (default) | `templates/prism_2col.svg` |
| `before_after` | `templates/prism_2col_beforeafter.svg` |

#### flow_variant — prism 版(值與 fresh 相同,per-deck)

Same four macro silhouettes and pick-rules as the `glass_arch_flow` variants below, same invariants (edge-anchored two-layer masses dissolving to ≤0.10 at the bleed edge; the sweep is ONE continuous filled path painted before the masses) — but the masses are prism `blur_bloom` shapes in mint/lavender (`#B9EBD2` / `#DCD9F6` tones) and the sweep is mint (`#C4EEDA` α0.5 → `#9BE4BE` α0.85). No dome-arch gradients, no fresh swoosh hues. **Tie-breaker when no story shape fits: `river_ribbon`** (same as fresh).

| `flow_variant` | Template |
|---|---|
| `terrace_ascent` | `templates/prism_flow_terrace.svg` |
| `river_ribbon` | `templates/prism_flow_river.svg` |
| `cascade_fall` | `templates/prism_flow_cascade.svg` |
| `dome_arcade` | `templates/prism_flow.svg` (soft-dome silhouette in prism blur_bloom, not fresh's arch gradients) |

**Motion pages (`IT_prism`)**: `transit_pipeline`'s rail is a green gradient (`#58D494 → #83E0B4`, 12px round caps) and takes a thin **white** pulse overlay (`motion: "transit_rail"`); the orbit ring is dotted `#9BD9BE` **open arc segments** (never a closed circle) and animates directly (`motion: "orbit"`). Same gates and recipes as the fresh bullet in "Motion pages — flow-anim 載體" below.

**Style traits** (what makes it read as this family):
- **Full-sentence assertion titles** — slate `#344252`, 30–36px weight 700, left-aligned at x=48. No pill bar (that's fresh's mark), no accent underline (global invariant). The top-right `progress_ticks` + `corner_bloom` carry the page signature instead.
- **Cover formula** — reeded glass right, clear left column: a small slate chip (`#344252` rect, white 14px label, e.g. 提案簡報), slate title 56–64px weight 700, a date/department line in `#4C5A6B` (on-canvas text — the lighter `#6B7686` fails AA on the wash), all on the near-white left side. **Slate text on light — never white-on-gradient, never green title text.** End page mirrors the cover with a centered short CTA.
- **Text density is a feature** — body 18–19px / line-height 1.85, the highlight band carrying the skim path. This family is a natural carrier of `delivery_mode: "reading"` (slidedoc) decks — see [references/slidedoc.md](slidedoc.md).
- **Hinge numbers are slate** — a page that pivots on one number renders it 48–72px weight 800 in `#344252` (or white on a `slate_anchor` block). Never green (fails AA), never any cover hue.
- **Tables** — slate header band (`#344252`, white text), white body rows, `#DFE2E9` hairlines, green tag pills for status marks.
- **Diagram affinity** — primitives keep their geometry; connectors/strokes `#9BD9BE`, the single highlighted element `#58D494` fill or `slate_anchor`, node icons slate.

### Corporate fresh family (`corporate_fresh`) — on request

Pick this family when the user asks for it (`palette_hint: "corporate_fresh"`, `highlight_color: "#E8872E"`, `motif_hint: "fresh_pill_cards"`).

Light consulting-deck style modeled on top-tier bank/consulting internal decks: warm light-gray canvas with soft pastel radial washes, a green→indigo gradient reserved for cover/end pages, white rounded cards, dashed separators, blue line-icons, and **orange bold inline emphasis** inside body text. Where `dark_apple` speaks through one highlight color and giant numbers, `corporate_fresh` speaks through **full-sentence assertion titles and dense, well-set body text** — executive briefings, internal proposals, and decks that argue in prose rather than in statistics.

**Role palette — colors are assigned to fixed roles, never mixed freely:**

All values below were calibrated by pixel-sampling a reference deck of this style — don't "round" them toward adjacent hues.

| Role | Color | Used for — and nothing else |
|---|---|---|
| Canvas | `#F4F4F4` neutral light gray | page background on all content pages |
| Pastel washes | `#BFE5CC` green / `#D9D4F0` lavender / `#F6ECC4` yellow / `#F3D4D4` rose | huge soft `radialGradient` blobs (opacity ≤ 0.55) at canvas corners/sides; max 2 per page |
| Ink | `#383838` neutral charcoal | titles, card headings |
| Body text | `#4A5158`; secondary `#6B7178` | paragraphs, captions |
| Structure green | bright mint gradient `#4EC487 → #7BD8A6`; dashed separators `#9BD4B8` | title pill bar, connectors, timeline/arrow shapes |
| Teal | `#1B8A82` | positive / recommended option headings, scheme names, underlined key phrases on roadmap cards |
| Icon blue | `#5E8FEF` stroke, `#D8E4FB` duotone fill | duotone icons ONLY — never text, never card fills |
| **Emphasis orange** | `#E8872E` | **bold inline runs inside body text only** — never fills, never icons, never large areas |
| Alert pair | `#E05B5B` red / `#E5B53A` amber | risk/warning panels only (dashed-border boxes + warning labels) |
| Recommendation capsule | gradient `#A8E8E0 → #80D0F8`, text `#2F3437` near-black bold | the 推薦方案-style capsule only |
| Cover gradient | `x1=0,y1=0 → x2=100%,y2=55%`: `#56BE85 → #5BA7D6 42% → #7378E0 80% → #878DEB` | cover + end pages only, full-bleed, with white aurora ribbons at 0.05–0.10 opacity + one soft white corner glow |

**Emphasis discipline (this family's equivalent of single-highlight discipline):** each color may appear only in its role above. Orange is the loudest voice and lives exclusively in bold `<tspan>` runs inside body paragraphs — 1–2 runs per paragraph, marking the phrase the audience must retain. If orange shows up as a card fill, an icon, or a heading, the style is broken. Green carries structure, blue carries icons, orange carries meaning.

**Signature components:**

```xml
<!-- Title pill bar + assertion title (every content page) -->
<defs><linearGradient id="pillGrad" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="#4EC487"/><stop offset="100%" stop-color="#7BD8A6"/>
</linearGradient></defs>
<rect x="48" y="44" width="64" height="8" rx="4" fill="url(#pillGrad)"/>
<text x="48" y="96" font-size="34" font-weight="700" fill="#383838">標題是一句完整的主張，不是名詞短語</text>

<!-- White card -->
<rect x="…" y="…" width="…" height="…" rx="14" fill="#FFFFFF" filter="url(#freshShadow)"/>
<!-- freshShadow: feGaussianBlur stdDeviation 10, offset (0,5), alpha slope 0.05 -->

<!-- Dashed column separator -->
<line x1="640" y1="220" x2="640" y2="600" stroke="#9BD4B8" stroke-width="2" stroke-dasharray="2 7"/>

<!-- Dashed alert box (risk panels) -->
<rect x="…" y="…" width="…" height="…" rx="10" fill="#FFFFFF" fill-opacity="0.6"
      stroke="#E05B5B" stroke-width="1.5" stroke-dasharray="6 5"/>

<!-- Recommendation capsule (e.g. 推薦方案) — spans the recommended column's full width -->
<defs><linearGradient id="recGrad" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="#A8E8E0"/><stop offset="100%" stop-color="#80D0F8"/>
</linearGradient></defs>
<rect x="…" y="…" width="330" height="48" rx="14" fill="url(#recGrad)"/>
<text x="…" y="…" font-size="21" font-weight="700" fill="#2F3437" text-anchor="middle">推薦方案</text>

<!-- Orange inline emphasis inside body text -->
<text x="…" y="…" font-size="19" fill="#4A5158">現行私銀網銀
  <tspan fill="#E8872E" font-weight="700">活躍度極低</tspan>，且存在
  <tspan fill="#E8872E" font-weight="700">嚴重資安風險</tspan>。</text>
```

**Craft recipes — where the 質感 comes from.** Flat fills, uniform strokes, and bare scaled-up icons are what make a page read "AI-generated" in this family. Each named recipe below replaces one of those tells. Starter templates `templates/fresh_*.svg` already embed them.

*`glass_arch`* — step-flow background shapes are bottom-bleed ARCHES, not floating circles. A complete circle hovering mid-canvas with a visible bottom edge is the #1 fusion killer: the composition must anchor to the page's bottom edge. Each step is TWO nested layers (outer halo + inner, more saturated dome), both running off the canvas bottom, with a vertical gradient that dissolves to near-nothing by the bottom edge. Overlapping neighbors layer into soft lenses:

```xml
<defs>
  <linearGradient id="archHalo" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#A6CDD4" stop-opacity="0.50"/>
    <stop offset="60%" stop-color="#BCD9D6" stop-opacity="0.22"/>
    <stop offset="100%" stop-color="#C8DED8" stop-opacity="0.05"/>
  </linearGradient>
  <linearGradient id="archDome" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#A6CDD4" stop-opacity="0.62"/>
    <stop offset="60%" stop-color="#BCD9D6" stop-opacity="0.28"/>
    <stop offset="100%" stop-color="#C8DED8" stop-opacity="0.08"/>
  </linearGradient>
</defs>
<!-- per step, centered on cx: paint ALL halos first, then all domes -->
<path d="M cx-150 720 L cx-150 380 A 150 150 0 0 1 cx+150 380 L cx+150 720 Z" fill="url(#archHalo)"/>
<path d="M cx-125 720 L cx-125 383 A 125 125 0 0 1 cx+125 383 L cx+125 720 Z" fill="url(#archDome)"/>
```

Give the FINAL step's arch a slightly greener pair (`#A1E5DE` / `#B6E8D8` / `#C5EDD8` at the same alphas) — a quiet closing emphasis. Cards inside arches: `fill="#FFFFFF" fill-opacity="0.88"`, **no shadow filter** — the arch itself provides separation; a shadow would lift the card off the arch and break the fusion.

*`tapered_swoosh`* — the sweeping arrow is ATMOSPHERE, not a line. Three rules: ① it is extremely light (tail ~`#CDEBD9` α0.55 → head ~`#A8DFC2` α0.9 — on canvas that reads as a 10–15% tint); ② it is ONE continuous filled path — tail flick, widening wedge, and arrowhead barbs in a single outline, never a stroke with a triangle glued on; ③ it is drawn BEFORE the arches, so the translucent arches overlap its endpoints and the swoosh visibly tucks behind the first and last arch:

```xml
<defs><linearGradient id="swooshGrad" x1="180" y1="0" x2="1042" y2="0" gradientUnits="userSpaceOnUse">
  <stop offset="0%" stop-color="#CDEBD9" stop-opacity="0.55"/>
  <stop offset="100%" stop-color="#A8DFC2" stop-opacity="0.9"/>
</linearGradient></defs>
<!-- tail flick at (180,196) → upper edge → barb up → tip → barb down → lower edge back -->
<path d="M 180 196 Q 480 122 950 172 L 938 148 L 1042 206 L 920 238 L 940 210 Q 470 180 190 232 Z"
      fill="url(#swooshGrad)"/>
<!-- then paint the arches OVER this -->
```

*`duotone_icon`* — feature icons are composed, 96–120px, in three layers: ① light-blue filled panels (`#D8E4FB`) giving the illustration its mass, ② a Lucide skeleton scaled up in `#5E8FEF` 2px strokes, ③ 2–4 extra detail strokes (screen content lines, signal dots, small badge). Never ship a bare 24×24 Lucide scaled 4× as a hero icon:

```xml
<g transform="translate(190 258)">
  <rect x="14" y="10" width="68" height="46" rx="6" fill="#D8E4FB"/>          <!-- ① panel -->
  <g transform="scale(4)" stroke="#5E8FEF" stroke-width="2" fill="none"
     stroke-linecap="round" stroke-linejoin="round">
    <rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/>
    <line x1="12" y1="17" x2="12" y2="21"/>                                    <!-- ② skeleton -->
  </g>
  <path d="M22 38 l10 -10 8 6 14 -14" stroke="#5E8FEF" stroke-width="3"
        fill="none" stroke-linecap="round" stroke-linejoin="round"/>           <!-- ③ detail -->
</g>
```

*`aurora_ribbons`* — the cover/end background texture is 2–3 SMOOTH translucent ribbon bands (long C-curve paths, white at 0.05–0.10) flowing across the lower half, plus one soft white radial glow in a top corner (α≤0.16). Bands must be wide, slow curves spanning the full canvas width — no hard-edged geometric shapes, emblems, or rows of repeated silhouettes (those read as clutter on a gradient):

```xml
<radialGradient id="glowTR" cx="86%" cy="8%" r="42%">
  <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.16"/>
  <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
</radialGradient>
<rect width="1280" height="720" fill="url(#glowTR)"/>
<g fill="#FFFFFF">
  <path d="M -60 560 C 280 450, 620 620, 940 490 C 1130 413, 1250 400, 1340 385
           L 1340 480 C 1250 495, 1150 515, 960 590 C 640 716, 300 560, -60 670 Z" fill-opacity="0.07"/>
  <path d="M -60 680 C 320 580, 700 716, 1020 600 C 1180 542, 1290 532, 1340 526
           L 1340 720 L -60 720 Z" fill-opacity="0.10"/>
</g>
```

*`chunky_chevron`* — arrows between cards are single soft white wedges (~56×110px, α0.55) sitting in the arch-overlap lens at card mid-height — not 20px chevron glyphs, and not high-contrast stacked layers:

```xml
<path d="M 259 429 L 315 484 L 259 539 Z" fill="#FFFFFF" fill-opacity="0.55"/>
```

*dotted separator* — row separators inside cards are round dots, not dashes: `stroke="#9FB9AE" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="0.1 9"`.

**Composition vocabulary — pick the layout from the content's shape, then build it from the recipes above.** These ten named compositions are proven combinations (all built from the same recipes; none copies a reference slide). The shape of the content decides:

| Composition | Content shape it fits | Geometry in one line |
|---|---|---|
| `aurora_cover` | cover | gradient + title/bar formula + `aurora_ribbons` background texture (template: `fresh_cover.svg`) |
| `bento_hero_duo` | one core claim + 2 supports | 60% hero white card (duotone icon + 2-line 32px claim + emphasized body) + two stacked support cards right |
| `dual_alert_panels` | problems / risks | rose + amber washes left/right, dashed alert boxes grouped under red/amber labels, bottom gradient capsule pointing to the solution |
| `glass_arch_flow` | 3–5 sequential steps | a FAMILY of four variants sharing the glass craft — the planner picks one per deck via `design_brief.flow_variant`; see "glass_arch_flow variants" below |
| `glass_orbit_loop` | a cycle / iterative loop | dotted `#9BD4B8` orbit ring, 4 glass-circle nodes (dark line icons + labels), tangential direction arrows, center white claim card, side annotation; the orbit ring (drawn as open arc segments, not a closed circle) can carry `flow-anim` (`motion: "orbit"`) |
| `claim_tree` | hierarchy (thesis → pillars → pages) | apex gradient capsule → thin green S-curve fans → 3 white pillar cards → fading ghost-thumbnail row |
| `meta_bento` | an inventory / catalog | true bento grid (1 big + 2 medium + N small white cards), each holding a gray `#E3E8E5` wireframe + name + one-line caption |
| `split_style_duel` | two-sided contrast | two large rounded panels (each styled as the thing it depicts, as content thumbnails), bridged by a centered gradient capsule |
| `transit_pipeline` | a transformation pipeline | one wide white panel, a single gradient transit line (12px, round caps; ends on the last station — a trailing head only when the flow hands off downstream, see Step 5.7), ring stations + duotone icons above, names/bodies below; the line takes a white `flow-anim` pulse overlay (`motion: "transit_rail"`) |
| `cta_end` | closing with an action | cover gradient + aurora ribbons, centered CTA title + translucent mono command chip + link line; "Thanks" demoted to a small corner note |

Several common bento layouts are `card_variant` families — `three_col`, `mini_grid`, and `two_col_50_50` each have multiple fresh compositions chosen **per page** (see the `card_variant` subsections below); compare-table card pages (the `fresh_compare.svg` template) remain available for option comparisons.

#### three_col card_variant — 同一套卡片語言，四種構圖

`three_col` is a **family** too: the card language is fixed — pill bar, `washGreen` corner wash, white-on-canvas columns, `#383838` charcoal titles, `#4A5158` body, orange `#E8872E` inline emphasis, green structure (`#4EC487` / `#9BD4B8`). What varies is the macro composition, picked **per page** (not per deck — `three_col` recurs within a deck) from *that page's* content sub-shape. The planner sets `card_variant`; absent → `icon_column`.

| `card_variant` | Pick when the three items read as… | Geometry in one line | When NOT to use | Template |
|---|---|---|---|---|
| `icon_column` | independent parallels — no order, no shared axis | three even columns, duotone icon on top, centered title + body, dashed separators (the original) | — this is the neutral default | `templates/fresh_3col.svg` |
| `numbered_steps` | a weak order (first → then → then) not strong enough to lose to `flow` | green numbered badges riding a rising connector, forward chevrons, left-aligned text | the order is a hard dependency or dated → use `flow` / `timeline` | `templates/fresh_3col_steps.svg` |
| `axis_labeled` | measured along ONE shared dimension axis (e.g. Product / Process / Performance) | a shared light-green label band split into three segments by the column separators, content aligned beneath | the three items don't share a common ruler | `templates/fresh_3col_axis.svg` |
| `lead_plus_pair` | three parallels where ONE leads and two support it | a 60% hero card (big duotone icon + 2-line claim + emphasized body) + two stacked support cards right | the three are co-equal (use `icon_column`) or it's really 2 ideas (use `two_col_2_1`) | `templates/fresh_3col_lead.svg` |

#### mini_grid card_variant — KPI 網格的三種構圖

`mini_grid` is the corporate_fresh KPI grid — for **numbers** (`meta_bento` is the one for catalogs with wireframe thumbnails). It's a `card_variant` family too. Numbers are teal `#1B8A82` (never orange — a giant orange number breaks the role palette) with `tabular-nums` so digits align. Absent → `even_grid`.

| `card_variant` | Pick when the KPIs read as… | Geometry in one line | When NOT to use | Template |
|---|---|---|---|---|
| `even_grid` | 3–5 parallel metrics of comparable weight | equal white number-cards in a row, big teal number + caption + EN, short green accent rule | — the neutral default | `templates/fresh_mini_grid.svg` |
| `ribbon_row` | metrics whose relative magnitudes matter, or that need a longer caption | full-width rows: number left, label + caption middle, a proportion bar right (structure green) | the numbers aren't comparable on one scale | `templates/fresh_mini_grid_ribbon.svg` |
| `spotlight` | a set where ONE number dominates and the rest break it down | one large lead card + stacked satellite cards | it's a single number with no set → `stat_hero` | `templates/fresh_mini_grid_spotlight.svg` |

#### two_col_50_50 card_variant — 兩欄的兩種構圖

`two_col_50_50` is a `card_variant` family for two-up content. Absent → `balanced`.

| `card_variant` | Pick when the two read as… | Geometry in one line | When NOT to use | Template |
|---|---|---|---|---|
| `balanced` | two co-equal options / ideas / pros-vs-cons | two equal white cards, icon + eyebrow + title + body each | — the neutral default | `templates/fresh_2col.svg` |
| `before_after` | a transformation: current state → new state | two cards with a green directional arrow between; the "after" card carries the green eyebrow + orange payoff | the two are co-equal (use `balanced`) or it's a dramatic style contrast (use `split_style_duel`) | `templates/fresh_2col_beforeafter.svg` |

**Where card_variant stops (and the composition vocabulary takes over).** Only the recurring bento card layouts whose sub-shapes genuinely differ get a `card_variant` family. The rest are already served by a named composition or have no sub-shape to vary — adding variants there would only manufacture overlapping options:
- **one claim + 2–3 supports** → `bento_hero_duo` (and `three_col`'s `lead_plus_pair`), not a `hero_top` / `two_col_2_1` variant family
- **inventory / catalog** → `meta_bento`; **two-sided dramatic contrast** → `split_style_duel`
- **a single number** → `stat_hero`; **one element** → `single_focus`; **charts** → `chart_*`; **diagram primitives** → their own specs

Same discipline as flow: a content-driven family where it earns its keep, never variety for its own sake.

**This is composition, never recolor and never a new layout** — `layout` stays `three_col`, the role palette is untouched, and `card_variant` never bypasses the 4 information-loss signals (if direction / alignment / topology / axis loss fires on the page, switch to the matching primitive instead). **Repetition is still a feature**: a same-structure parallel series (the four D's, N pillars) keeps this one shared card language; assign variants only by each page's real sub-shape — when several pages share one ruler, give them all `axis_labeled` with identical labels (deliberate rhyme, not monotony). Forcing different variants just to look different is the same bug as switching layouts for variety (P3-06).

#### glass_arch_flow variants — 同一套工藝，四種構圖

`glass_arch_flow` is a **family**: the craft is fixed, the macro geometry is not. Every variant keeps the same invariants — large glass forms are **edge-anchored** (bleeding off a canvas edge; never a complete shape floating mid-canvas), built in **two layers** (outer halo + inner body, gradient dissolving to ≤0.10 alpha at the bleed edge); the directional sweep is **atmosphere, not a line** (ONE continuous filled path with an integrated arrowhead, painted BEFORE the glass forms so its ends tuck behind the first and last — this sweep bleeds off-canvas and never lands on a discrete node, so the `transit_rail` terminal rule below does not apply to it); white cards sitting on glass are `fill-opacity 0.88` with no shadow; the final step carries the quiet greener emphasis pair. What varies is the macro composition: silhouette, anchor edge, sweep course, rhythm.

The planner sets `design_brief.flow_variant` **once per deck**; all static `flow` pages in that deck share it (coherence inside the deck, variety across decks). Derive the pick from the story the steps tell — never roll dice, and never default to the same variant out of habit:

| `flow_variant` | Pick when the steps read as… | Geometry in one line | Worked example |
|---|---|---|---|
| `terrace_ascent` | capability / maturity built up step by step | bottom-bleed flat-top mesas RISING left→right, step cards inside each mesa, a low horizon swoosh weaving BEHIND the skyline, arrowhead emerging past the final mesa | `templates/fresh_flow_terrace.svg` |
| `river_ribbon` | a journey / end-to-end experience through stations | ONE wide ultra-light meandering ribbon (filled path, edge-to-edge bleed, integrated arrowhead), numbered ring stations fused ON its centerline, cards alternating above / below | `templates/fresh_flow_river.svg` |
| `cascade_fall` | a top-down procedure, or steps that need longer prose (3–4 steps) | glass half-discs bleeding off the LEFT edge as a numbered bank (downward chevrons in the overlap lenses), a falling swoosh behind the bank, full-width white rows with round-dot separators | `templates/fresh_flow_cascade.svg` |
| `dome_arcade` | evenly-weighted parallel stages, classic consulting look | the original: bottom-bleed dome arches + high tapered swoosh through the tops | `templates/fresh_flow.svg` |

`dome_arcade` is **no longer an automatic default** — it is one option of four, chosen on the same story-shape grounds as the others. **Tie-breaker: when no story shape clearly fits** (the steps read as none of the four, or as more than one equally well), **default to `river_ribbon`** — not `dome_arcade`. If a rendered flow page is geometrically congruent with a worked example the planning did not pick (same silhouette, same shape count, positions within ~10%), the designer copied instead of deriving — rebuild it. Worked examples show 4 steps; for 3 or 5 steps keep each variant's silhouette and re-space the step axis evenly (terrace tops keep rising; river stations stay on the centerline; cascade rows divide the content band).

### Motion pages — flow-anim 載體

When planning sets a `motion` field, the slide ships as a looping GIF (flowing dashes in slideshow mode; that slide loses Convert-to-Shape). The animated element rides an existing composition — never invent a new one for it:

- **`corporate_fresh`**: `transit_pipeline`'s gradient rail takes a thin **white** pulse overlay (`motion: "transit_rail"`); `glass_orbit_loop`'s dotted ring — drawn as open arc segments, not a closed circle — animates directly (`motion: "orbit"`). A conceptual cycle (not just a money loop) is an equally valid reason to animate this ring — the qualifying call is the planner's, per the gate in [prompts/04_planning_draft.md](../prompts/04_planning_draft.md) → "Motion pages". The swoosh is atmosphere, not a line — it never animates.
- **`dark_apple`**: same rail composition with a graphite `#333333` 12px rail and a pulse overlay in the deck's **highlight color**. How the rail ends follows the arrival-vs-hand-off rule in Step 5.7 — when the last station is the destination (the usual case) the rail ends ON it with a highlight-color terminal ring and **no trailing head**; a trailing head appears only when the flow hands off downstream. The highlight appears only in the pulses, the terminal ring (and a trailing head if present) — single-highlight discipline holds.

Construction recipes, marking rules, and all numeric baselines: [prompts/05_designer_svg.md](../prompts/05_designer_svg.md) Step 5.7 (canonical). The "never animate" list: [references/diagrams.md](diagrams.md).

**Style traits** (what makes it read as this family):
- **Full-sentence assertion titles** — page titles state the conclusion ("新架構兼具現代化與極致安全，無需重建安控"), not the topic ("架構介紹"). 30–36px, weight 700, charcoal, left-aligned after the pill bar. Because the title already *is* the page's conclusion, a page does not also need a closing so-what line at the bottom; a bottom line that paraphrases the title is the title said twice. Reserve any bottom line for a genuinely new point (consequence / hand-off) — see [prompts/05_designer_svg.md](../prompts/05_designer_svg.md) Step 6 → "content".
- **Text density is a feature** — body runs 18–19px / line-height 1.85, 2–4 lines per block, with orange emphasis carrying the skim path. This family tolerates (and expects) more prose than `dark_apple`, and is a natural carrier of `delivery_mode: "reading"` (slidedoc) decks — see [references/slidedoc.md](slidedoc.md).
- **Centered short blocks are allowed** — column/card paragraphs ≤4 lines under an icon may center; longer prose left-aligns. (Per-family exception to the global "never center body text" rule.)
- **Icons are composed duotone illustrations** — 96–120px, built per the `duotone_icon` recipe (light-blue `#D8E4FB` panels + `#5E8FEF` Lucide skeleton + detail strokes). Icons never carry color variety.
- **Cover/end formula** — full-bleed gradient, white title 64–72px weight 700 left at x≈120, a solid white bar beneath holding the subtitle in `#3E5BA8` bold, date/author line in white 0.92; end page is the same gradient with a single centered "Thanks".
- **Diagram affinity** — this family renders timelines, step flows, comparison cards, and even sequence diagrams comfortably; structure shapes (arrows, bars, lifelines) use greens/teals at 0.5–0.9 opacity, message/flow arrows may use a yellow→blue subtle duo-tone, returns are dashed gray.

### Light traditional family

For decks that need to match brand decks, print, or where dark mode is wrong (academic, healthcare patient-facing, conservative finance).

| Hint key | Primary | Secondary | Accent | Best for |
|---|---|---|---|---|
| `midnight_executive` | `#1E2761` navy | `#CADCFC` ice blue | `#FFFFFF` white | Enterprise, finance, B2B SaaS |
| `forest_moss` | `#2C5F2D` forest | `#97BC62` moss | `#F5F5F5` cream | Sustainability, agriculture, wellness |
| `coral_energy` | `#F96167` coral | `#F9E795` gold | `#2F3C7E` navy | Consumer, lifestyle, energetic launches |
| `warm_terracotta` | `#B85042` terracotta | `#E7E8D1` sand | `#A7BEAE` sage | Hospitality, design, NGO |
| `ocean_gradient` | `#065A82` deep blue | `#1C7293` teal | `#21295C` midnight | Tech, infrastructure, calm authority |
| `charcoal_minimal` | `#36454F` charcoal | `#F2F2F2` off-white | `#212121` black | Minimal, premium, fashion |
| `teal_trust` | `#028090` teal | `#00A896` seafoam | `#02C39A` mint | Healthcare, fintech-trust |
| `berry_cream` | `#6D2E46` berry | `#A26769` dusty rose | `#ECE2D0` cream | Food & beverage, beauty |
| `sage_calm` | `#84B59F` sage | `#69A297` eucalyptus | `#50808E` slate | Wellness, mindfulness, ed-tech |
| `cherry_bold` | `#990011` cherry | `#FCF6F5` off-white | `#2F3C7E` navy | Bold proposals, anniversary, statement decks |

### Single highlight color discipline (dark_apple family)

This is non-negotiable for the dark Apple style and is what separates "AI deck" from "designed deck":

- Pick **one** highlight color at the start of phase 4. Apply it everywhere emphasis is needed: hero numbers, section titles, key icons, chart accents, chart fills, gradient tints. **No second accent color.** No "complementary" warm-cool pairing.
- The only other colors on the slide are the dark-mode neutrals listed above (black bg, dark gray cards, white text, gray subtitles).
- Tech gradient: allowed only as `rgba(highlight, 0.7) → rgba(highlight, 0.3)` — single hue alpha gradient. **No multi-color gradients ever.**
- When in doubt, more black + more highlight ≠ multiple colors.

### Highlight color saturation tiers — what alpha to use where

Single highlight color discipline doesn't mean "use the same alpha everywhere". The highlight color carries different visual weight in different roles. Use this tier table:

| Role | Alpha / Saturation | Example |
|---|---|---|
| **Hero element** (numbers, key icons, hero text) | **1.00** (full saturation) | `<text fill="#FF6900">142.5%</text>` — the number IS the message |
| **Card border / accent line** | 1.00 | `stroke="#FF6900"` 1–2px on the secret-sauce card |
| **Highlighted card body tint** | **≤ 0.20** | The "secret sauce" `mini_grid` Phase 3 card uses `fill-opacity="0.15"` |
| **stat_hero radial glow behind number** | **≤ 0.10** (peak), fades to 0 | `radialGradient` stops `0% → 0.10, 60% → 0.03, 100% → 0` |
| **Page-background mesh / atmosphere** | **≤ 0.08** | Cover page corner glow: `radialGradient` with `stop-opacity="0.08"` |
| **Subtle card lift** (whole-page secondary fills) | **≤ 0.06** | Quiet background warmth on a section_break |

**The rule of thumb**: full saturation only on the thing the audience must *read*. Sustained or large-area use of the highlight color must drop below 0.20 alpha. Going above 0.30 on a large area produces eye fatigue — Tip 4 from the Keynote研究所 "15 tips" article ("大面積純色降低飽和度") translated to our dark + alpha context.

Bright orange (`#FF6900`) filling 40% of the canvas at 1.00 alpha is a **failure mode**, not a feature. The eye gets nowhere to rest, and the actual content stops reading. If you find yourself painting big regions with the highlight color, drop the alpha first; never reach for a second hue.

### Dominance rule (light family)

For light palettes, one color carries **60–70% visual weight**, 1–2 supporting tones, one sharp accent. Most decks should use the primary as card headers / titles (light deck) or background (dark variant).

### Sandwich structure (light family only)

For light decks of 10+ pages, alternate intensity:
- **Cover** & **End**: dark background (primary)
- **Section breaks**: dark background (primary)
- **Content pages**: light background (secondary or neutral white)

For `dark_apple` decks, the entire deck is on the same pure-black background — visual rhythm comes from **card density and highlight color saturation**, not background swaps.

---

## Motifs

Pick one motif. Apply on every page. All examples below are SVG (since the Designer outputs SVG).

### `apple_dark_cards` (default for dark_apple palettes)

Dark gray cards on pure black, subtle 1px borders. The highlight color appears only on text, numbers, icons, and a small accent rect — never as a card background.

```xml
<!-- Main card -->
<rect x="48" y="140" width="582" height="532" rx="20" ry="20"
      fill="#1A1A1A" stroke="#333333" stroke-width="1"/>

<!-- Mini card (smaller radius) -->
<rect x="80" y="200" width="160" height="120" rx="12" ry="12"
      fill="#222222" stroke="#333333" stroke-width="1"/>

<!-- Optional: faint highlight-color glow on important cards -->
<defs>
  <linearGradient id="heroGlow" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#FF6900" stop-opacity="0.18"/>
    <stop offset="100%" stop-color="#FF6900" stop-opacity="0.04"/>
  </linearGradient>
</defs>
<rect x="48" y="140" width="582" height="532" rx="20" ry="20"
      fill="url(#heroGlow)"/>
<rect x="48" y="140" width="582" height="532" rx="20" ry="20"
      fill="#1A1A1A" fill-opacity="0.85" stroke="#333333" stroke-width="1"/>
```

The look: minimal, modern, premium. Card boundaries do the work; shadow is replaced by border + slight value separation (`#1A1A1A` cards on `#000000` page).

### `prism_panel_cards` (default for `IT_prism` — the default style)

White rounded panel cards (rx=14) with the `prismShadow` whisper on the cool `#EFF0F3` canvas, the diagonal lavender→mint wash, the green `corner_bloom` + white dashed geometry top-right, `progress_ticks` at the top-right corner, slate assertion titles, and `slate_anchor` dark blocks as the focus device. SVG snippets live in the `IT_prism` palette section above. The look: cool, technical, quiet; structure in slate, pointing in green, atmosphere in blurred lavender/mint.

```xml
<!-- Canvas with the diagonal wash pair + corner bloom -->
<defs>
  <radialGradient id="washLav" cx="8%" cy="10%" r="55%">
    <stop offset="0%" stop-color="#EEEEFD" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="#EEEEFD" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="washMint" cx="92%" cy="92%" r="55%">
    <stop offset="0%" stop-color="#E7F9F1" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="#E7F9F1" stop-opacity="0"/>
  </radialGradient>
</defs>
<rect width="1280" height="720" fill="#EFF0F3"/>
<rect width="1280" height="720" fill="url(#washLav)"/>
<rect width="1280" height="720" fill="url(#washMint)"/>
```

### `fresh_pill_cards` (default for `corporate_fresh`)

White rounded cards (rx=14) with a whisper shadow on the light `#F4F4F4` canvas, the green gradient pill bar above every page title, pastel radial washes in the canvas corners, and dashed green separators between columns. SVG snippets live in the `corporate_fresh` palette section above. The look: airy, premium consulting; structure drawn in green, content in charcoal/gray with orange inline emphasis.

```xml
<!-- Canvas with one pastel wash -->
<defs>
  <radialGradient id="washA" cx="12%" cy="88%" r="55%">
    <stop offset="0%" stop-color="#BFE5CC" stop-opacity="0.5"/>
    <stop offset="100%" stop-color="#BFE5CC" stop-opacity="0"/>
  </radialGradient>
</defs>
<rect width="1280" height="720" fill="#F4F4F4"/>
<rect width="1280" height="720" fill="url(#washA)"/>
```

### `rounded_cards_soft_shadow`

```xml
<defs>
  <!-- Shadow tinted toward the palette primary (flood-color), not pure black —
       a faintly hued shadow reads as intentional. Swap flood-color per palette. -->
  <filter id="cardShadow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur in="SourceAlpha" stdDeviation="12" result="blur"/>
    <feOffset in="blur" dx="0" dy="8" result="offsetblur"/>
    <feFlood flood-color="#1E2761" flood-opacity="0.12" result="tint"/>
    <feComposite in="tint" in2="offsetblur" operator="in" result="shadow"/>
    <feMerge><feMergeNode in="shadow"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<rect x="48" y="140" width="582" height="532" rx="16" ry="16"
      fill="#FFFFFF" filter="url(#cardShadow)"/>
```

Safe default. Works with any palette. Light, modern, magazine-y. (The `corporate_fresh` family keeps its own lighter `freshShadow` whisper — this tinted shadow is only for the `rounded_cards_soft_shadow` motif.)

### `left_accent_bar`

```xml
<!-- Card body with extra left padding (text starts at x = card_x + 30) -->
<rect x="48" y="140" width="582" height="532" rx="8" ry="8" fill="#FFFFFF"/>
<!-- 6×card-height accent bar pinned to the card's left edge -->
<rect x="48" y="140" width="6" height="532" fill="#1E2761"/>
```

Editorial, structured feel. Pairs well with serif headers. Remember to shift card text to `x = card_x + 30` so the bar doesn't eat into it.

### `icon_in_circle`

```xml
<!-- 48×48 circle filled with secondary color, icon centered inside -->
<circle cx="104" cy="196" r="24" fill="#CADCFC"/>
<g transform="translate(80 172)" color="#1E2761">
  <!-- 24×24 Lucide icon path, stroke=currentColor (= primary), stroke-width=2 -->
  <path d="…" fill="none" stroke="currentColor" stroke-width="2"
        stroke-linecap="round" stroke-linejoin="round"/>
</g>
```

Friendly, approachable. Good for consumer / education decks. The 24×24 icon viewport sits at `(card_x + 32, card_y + 32)` so the circle is centered around `(card_x + 56, card_y + 56)`.

### `gradient_mesh_bg`

```xml
<defs>
  <radialGradient id="meshA" cx="20%" cy="20%" r="55%">
    <stop offset="0%" stop-color="#1E2761" stop-opacity="0.28"/>
    <stop offset="100%" stop-color="#1E2761" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="meshB" cx="85%" cy="80%" r="55%">
    <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.22"/>
    <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
  </radialGradient>
</defs>
<rect width="1280" height="720" fill="#F7F9FC"/>
<rect width="1280" height="720" fill="url(#meshA)"/>
<rect width="1280" height="720" fill="url(#meshB)"/>
```

Atmospheric. Best on dark backgrounds for cover/section pages, paired with white card bodies on content pages.

---

## Typography

### Pairings

| Hint key | Header font | Body font | Vibe |
|---|---|---|---|
| `serif_header_sans_body` | Noto Serif TC, Playfair Display | PingFang TC, Helvetica | Editorial, premium |
| `sans_only_bold` | PingFang TC 900, Helvetica 800 | PingFang TC 400, Helvetica 400 | Modern, tech |
| `mono_accent` | JetBrains Mono 700, Helvetica 800 | Helvetica 400 | Tech-forward, dev-tools |

Web fonts are **not** loaded. To keep SVG pages fully self-contained, portable, and editable in PowerPoint, the designer uses a system-font stack via the SVG `font-family` attribute on the root `<svg>`:

```xml
<svg … font-family="Helvetica, 'Helvetica Neue', Arial, 'PingFang TC', 'Microsoft JhengHei', 'Hiragino Sans', 'Noto Sans CJK TC', 'Noto Sans TC', sans-serif">
```

**Order rationale**:
- **Latin chars** resolve to Helvetica (macOS preinstalled) → Helvetica Neue → Arial (Windows fallback; visually near-identical Microsoft clone of Helvetica)
- **CJK chars** resolve to PingFang TC (macOS preinstalled) → Microsoft JhengHei 微軟正黑體 (Windows preinstalled) → Hiragino Sans (older macOS) → Noto Sans CJK TC (Linux / installed-by-choice) → Noto Sans TC → sans-serif final fallback

Both Latin and CJK use OS-preinstalled fonts — zero recipient install effort. Same stack works in macOS / Windows / Linux without anyone needing to download anything. The PNG fallback rendered by `svg_to_pptx.py` resolves the same stack via the renderer's font config (resvg-py → fontkit / fontconfig, cairosvg → fontconfig, Inkscape → system fonts).

### Sizes (1280×720 canvas)

Use **dramatic** size contrast. The point of the design system is to create a clear visual hierarchy from "this matters" to "this is supporting." Soft, similar sizes flatten the deck.

**Sizes bumped in v0.7.4** to improve readability of body / caption / supporting text on projected slides. Hero numbers, cover titles, and mini-card stat numbers unchanged — they were already commanding.

| Element | Size | Weight | Color (dark_apple) | Color (light) |
|---|---|---|---|---|
| Cover title (CN) | 96–120px | 900 | white | primary |
| Cover subtitle (EN) | 22–28px | 500 | gray-400 / `#A0A0A0` | text-muted |
| Page title (CN) | 40–52px | 800 | white | primary |
| Page title (EN, optional) | **18–22px** | 500 | gray-500 / `#666666` | text-muted |
| Page subtitle | 18–22px | 400 | gray-400 | text-muted |
| **Hero stat number** | **80–120px** | **900** | **highlight color** | **highlight color** |
| Hero stat caption (CN) | **16–18px** | 400 | gray-300 / `#A0A0A0` | text-muted |
| Hero stat caption (EN) | **12–14px** | 400 | gray-500 / `#666666` | text-muted |
| Card heading (text-first, big) | **36–52px** | 700–800 | white or highlight | primary |
| Mini-card heading (text-first) | **26–34px** | 700 | white | primary |
| Mini-card stat number | 56–72px | 900 | highlight | highlight |
| Mini-card caption (CN) | **16–18px** | 400, line-height 1.55 | white / gray-300 | text |
| Mini-card caption (EN, decorative) | **12–14px** | 400 | gray-500 | text-muted |
| Card body / support text | **17–19px** | 400, line-height 1.55 | gray-400 | text |
| Primitive body (flow / cycle / pyramid / venn / tree node body) | **14–15px** | 400 | gray-400 | text |
| Compare_table cell value | **19px** | 700 | white or highlight | primary |
| Compare_table dimension label | **17px** | 500 | gray-400 | text |
| Captions / footnotes | 11–13px | 400, opacity 0.6 | gray-600 | text-muted |

### Sizes — `IT_prism` family (1280×720 canvas)

Same sentence-driven hierarchy as `corporate_fresh` (this family also argues in prose), with the prism color roles:

| Element | Size | Weight | Color |
|---|---|---|---|
| Cover chip label | 14–16px | 600 | `#FFFFFF` on `#344252` chip |
| Cover title (CN) | 56–64px | 700 | `#344252` |
| Cover date/department | 18–20px | 400 | `#4C5A6B` (sits on the wash — not `#6B7686`) |
| Page title (full-sentence assertion) | 30–36px | 700 | `#344252` |
| Column / card heading | 24–32px | 700 | `#344252` (or `#FFFFFF` on a `slate_anchor` band) |
| Step or option label | 20–24px | 700 | `#344252` |
| **Hinge number** (page pivots on it) | 48–72px | 800 | **`#344252` slate — never green, never a cover hue** |
| Mini-card stat number | 44–60px | 800 | `#344252`, `tabular-nums` |
| Body text | 18–19px | 400, line-height 1.85 | `#4C5A6B` |
| Inline emphasis run | 18–19px (same as body) | 700 | `#344252` ink + green device (band / underline / pill) |
| Small annotation / axis label | 15–16px | 400–700 | `#6B7686` (on white cards; on the canvas itself use `#4C5A6B`) |
| End-page CTA | 44–56px | 700 | `#344252` |

### Sizes — `corporate_fresh` family (1280×720 canvas)

This family argues in sentences, so its hierarchy is flatter than `dark_apple`'s number-driven drama — but still deliberate. Titles assert, body carries the reasoning, orange emphasis carries the skim path.

| Element | Size | Weight | Color |
|---|---|---|---|
| Cover title (CN) | 64–72px | 700 | `#FFFFFF` |
| Cover subtitle (in white bar) | 26–30px | 700 | `#3E5BA8` |
| Cover date/author | 20–22px | 400 | white 0.92 |
| Page title (full-sentence assertion) | 30–36px | 700 | `#383838` |
| Column / card heading | 28–34px | 700 | `#383838` (or `#1B8A82` teal when "recommended/positive") |
| Step or option label (Step 1 / 方案一) | 22–26px | 700 | `#1B8A82` or `#383838` |
| Body text | 18–19px | 400, line-height 1.85 | `#4A5158` |
| Inline emphasis run | 18–19px (same as body) | 700 | `#E8872E` |
| Small annotation / axis label | 15–16px | 400–700 | `#6B7178` |
| End-page "Thanks" | 52–60px | 300–400 | `#FFFFFF` |

**No giant hero-number row here on purpose.** If a `corporate_fresh` page genuinely hinges on one number, render that number in ink `#383838` or teal `#1B8A82` — **never** the orange `highlight_color`. Orange is inline-emphasis only; a giant orange number is a large-area fill that breaks the role palette. (`dark_apple` is the family that speaks through giant highlight-color numbers; `corporate_fresh` argues in sentences.)

### Delivery mode — reading (slidedoc) overlay

When a page's effective `delivery_mode` is `reading` (resolution rule in
`prompts/04_planning_draft.md`), the sentence-driven scale above gains one hard rule and
a set of size deltas. Full design language: [references/slidedoc.md](slidedoc.md).

> **The reading floor**: no text run below **16px** on the 1280×720 canvas (= 12pt on
> the exported 16:9 slide). A standalone reader has no presenter to say the small print
> aloud. This is the mode's single hard geometric rule — everything else is judgment.

Deltas versus the presenting tables (only sizes below the floor move; the skim layer
stays dramatic):

| Element (presenting size) | Reading mode |
|---|---|
| Captions / footnotes 11–13px | **16px** — the "quiet" is carried by color/opacity, not size |
| Primitive body (flow / cycle / pyramid / venn / tree) 14–15px | **16–17px** — and reduce node count before shrinking text (≤4 flow steps, ≤3 pyramid tiers with prose) |
| EN decorative captions 12–14px | **cut first; 16px if kept** — at floor size English decoration competes with the CN core; bilingual polish is the first thing traded for prose room |
| Small annotation / axis label 15–16px | **16px** |
| Cover chip label 14–16px, tag-pill text 14px | **16px** |
| Bottom line / footer voice 14–16px | **16px** |
| Chart axis / value / legend labels below 16px | **16px** — if floored labels collide, reduce categories, switch `chart_bar` → `chart_hbar`, or drop the sub-label row; never shrink below the floor |
| Body text 18–19px | unchanged (19–20px allowed on prose-heavy pages); line-height stays 1.85 |
| Titles, card headings, hinge numbers | unchanged — the skim layer keeps its drama |

Layer rules (see slidedoc.md §3): every ≥2-sentence body block opens with an **ink-bold
lead-in** (`#344252` prism / `#383838` fresh — never the emphasis voice), and inline
emphasis tightens to ≤1 run per block.

### Visual hierarchy rules

1. **Numbers dominate.** Whenever a card carries a key statistic, the number itself is the largest element on the card (`80–120px` for hero stats; `56–72px` for mini-card stats). The caption explaining the number sits beneath it at `16–18px gray-300`.
2. **One hero element per card.** Either the big number OR the big text-title, never both at the same size.
3. **English is decorative.** Bilingual subtitles use one tier smaller and gray-500/600 — they add design polish without competing with the Chinese core.
4. **Body text is readable but quiet.** `17–19px gray-400` for support copy. Quieter than headings, but **large enough to read when projected** (the v0.7.4 bump targeted this specifically — pre-v0.7.4 sizes were 14–16px which read too small from the back row).
5. **Aligned figures use tabular numerals.** Any number that sits in a column or a row meant to line up — `mini_grid` stats, `compare_table` values, chart axis/value labels — carries `style="font-variant-numeric: tabular-nums"` so digits share one advance width and align vertically. A lone `stat_hero` number doesn't need it.

---

## Anti-patterns

- **Generic blue everywhere.** If the topic is sustainability, the palette should be earthy, not blue.
- **All colors at equal weight.** Pick a dominant one (60-70%).
- **Accent underline below the page title.** Use whitespace or color instead.
- **Centering body text.** Left-align always; center only titles when it serves the design. (Exception: `corporate_fresh` may center short ≤4-line blocks under icons in columns/cards.)
- **Mixing icon styles.** Stick to one stroke family (Lucide outline) at one stroke width (2px).
- **Random gap sizes.** Pick `20px` or `24px` — don't mix.
- **Forgetting padding when using `left_accent_bar`.** The bar will eat content if you don't add `padding-left: 30px`.
