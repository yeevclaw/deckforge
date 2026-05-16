# Design System — palettes, typography, motifs

This is the lookup table the Designer prompt uses to resolve `palette_hint`, `motif_hint`, and `typography_hint`.

## Palettes

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

### Dominance rule

One color carries **60–70% visual weight**, 1–2 supporting tones, one sharp accent. Most decks should use the primary as either the slide background (dark deck) or as card headers / titles (light deck).

### Sandwich structure

For decks of 10+ pages, alternate intensity:
- **Cover** & **End**: dark background (primary)
- **Section breaks**: dark background (primary)
- **Content pages**: light background (secondary or neutral white)

This creates a rhythm that prevents 20 same-feeling slides in a row.

---

## Motifs

Pick one motif. Apply on every page. All examples below are SVG (since the Designer outputs SVG).

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

| Element | Size | Weight |
|---|---|---|
| Cover title | 80–120px | 800–900 |
| Cover subtitle | 24–32px | 400 |
| Page title | 36–48px | 700 |
| Page subtitle | 18–22px | 400, opacity 0.7 |
| Card heading | 20–28px | 700 |
| Card body | 14–18px | 400, line-height 1.55 |
| Captions / footnotes | 11–13px | 400, opacity 0.6 |

---

## Anti-patterns

- **Generic blue everywhere.** If the topic is sustainability, the palette should be earthy, not blue.
- **All colors at equal weight.** Pick a dominant one (60-70%).
- **Accent underline below the page title.** Use whitespace or color instead.
- **Centering body text.** Left-align always; center only titles when it serves the design.
- **Mixing icon styles.** Stick to one stroke family (Lucide outline) at one stroke width (2px).
- **Random gap sizes.** Pick `20px` or `24px` — don't mix.
- **Forgetting padding when using `left_accent_bar`.** The bar will eat content if you don't add `padding-left: 30px`.
