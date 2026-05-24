# Design System — palettes, typography, motifs

This is the lookup table the Designer prompt uses to resolve `palette_hint`, `motif_hint`, and `typography_hint`.

## Palettes

DeckForge ships two **palette families**: dark Apple-style (single highlight color on black, our recommended default for data-dense decks) and traditional light themes.

### Dark Apple family (recommended default)

Pure black background, dark gray cards, one bold highlight color drawn from the brand or topic. Single-color discipline: that highlight carries 100% of the emphasis (no secondary or accent colors). Inspired by Apple keynote slides and the linux.do "Xiaomi annual report" visualization methodology.

| Hint key | Highlight | Best for |
|---|---|---|
| `dark_apple` | auto — pick brand color from content (e.g. Xiaomi `#FF6900`, Tesla `#E31937`, Anthropic `#D97757`); fallback `#FFA500` bright orange | Default for any data-/stat-heavy deck, annual reports, product launches, financial summaries |
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

### `rounded_cards_soft_shadow`

```xml
<defs>
  <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur in="SourceAlpha" stdDeviation="12"/>
    <feOffset dx="0" dy="8"/>
    <feComponentTransfer><feFuncA type="linear" slope="0.06"/></feComponentTransfer>
    <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<rect x="48" y="140" width="582" height="532" rx="16" ry="16"
      fill="#FFFFFF" filter="url(#cardShadow)"/>
```

Safe default. Works with any palette. Light, modern, magazine-y.

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
| `serif_header_sans_body` | Noto Serif TC, Playfair Display | Noto Sans TC, Inter | Editorial, premium |
| `sans_only_bold` | Noto Sans TC 900, Inter 800 | Noto Sans TC 400, Inter 400 | Modern, tech |
| `mono_accent` | JetBrains Mono 700, Inter 800 | Inter 400 | Tech-forward, dev-tools |

Web fonts are **not** loaded. To keep SVG pages fully self-contained, portable, and editable in PowerPoint, the designer uses a system-font stack via the SVG `font-family` attribute:

```xml
<svg … font-family="'Noto Sans TC', 'PingFang TC', 'Microsoft JhengHei', 'Hiragino Sans', Inter, system-ui, sans-serif">
```

This stack picks the best available CJK + Latin pair on macOS, Windows, and Linux. The PNG fallback rendered by `svg_to_pptx.py` will resolve the same stack via the renderer's font config (cairosvg → fontconfig, Inkscape → system fonts, rsvg-convert → fontconfig).

### Sizes (1280×720 canvas)

Use **dramatic** size contrast. The point of the design system is to create a clear visual hierarchy from "this matters" to "this is supporting." Soft, similar sizes flatten the deck.

| Element | Size | Weight | Color (dark_apple) | Color (light) |
|---|---|---|---|---|
| Cover title (CN) | 96–120px | 900 | white | primary |
| Cover subtitle (EN) | 22–28px | 500 | gray-400 / `#A0A0A0` | text-muted |
| Page title (CN) | 40–52px | 800 | white | primary |
| Page title (EN, optional) | 16–20px | 500 | gray-500 / `#666666` | text-muted |
| Page subtitle | 18–22px | 400 | gray-400 | text-muted |
| **Hero stat number** | **80–120px** | **900** | **highlight color** | **highlight color** |
| Hero stat caption | 14–16px | 400 | gray-400 | text-muted |
| Card heading (text-first) | 32–48px | 700–800 | white or highlight | primary |
| Mini-card heading | 24–32px | 700 | white | primary |
| Card body | 14–16px | 400, line-height 1.55 | gray-400 | text |
| English subtitle on mini-card | 11–13px | 400 | gray-500 | text-muted |
| Captions / footnotes | 11–13px | 400, opacity 0.6 | gray-600 | text-muted |

### Visual hierarchy rules

1. **Numbers dominate.** Whenever a card carries a key statistic, the number itself is the largest element on the card (`80–120px` for hero stats; `48–64px` for secondary stats). The caption explaining the number sits beneath it at `14–16px gray-400`.
2. **One hero element per card.** Either the big number OR the big text-title, never both at the same size.
3. **English is decorative.** Bilingual subtitles use one tier smaller and gray-500/600 — they add design polish without competing with the Chinese core.
4. **Body text is small and quiet.** `14–16px gray-400` for support copy. Don't make body text fight with headings.

---

## Anti-patterns

- **Generic blue everywhere.** If the topic is sustainability, the palette should be earthy, not blue.
- **All colors at equal weight.** Pick a dominant one (60-70%).
- **Accent underline below the page title.** Use whitespace or color instead.
- **Centering body text.** Left-align always; center only titles when it serves the design.
- **Mixing icon styles.** Stick to one stroke family (Lucide outline) at one stroke width (2px).
- **Random gap sizes.** Pick `20px` or `24px` — don't mix.
- **Forgetting padding when using `left_accent_bar`.** The bar will eat content if you don't add `padding-left: 30px`.
