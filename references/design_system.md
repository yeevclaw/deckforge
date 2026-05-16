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

Pick one motif. Apply on every page.

### `rounded_cards_soft_shadow`

```css
.card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.06);
  padding: 24px;
}
```

Safe default. Works with any palette. Light, modern, magazine-y.

### `left_accent_bar`

```css
.card {
  background: #fff;
  border-radius: 8px;
  padding: 24px 24px 24px 30px;
  position: relative;
  overflow: hidden;
}
.card::before {
  content: '';
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 6px;
  background: var(--primary);
}
```

Editorial, structured feel. Pairs well with serif headers.

### `icon_in_circle`

```css
.card .icon-wrap {
  width: 48px; height: 48px;
  border-radius: 50%;
  background: var(--secondary);
  display: grid;
  place-items: center;
}
.card .icon-wrap svg { stroke: var(--primary); width: 24px; height: 24px; }
```

Friendly, approachable. Good for consumer / education decks.

### `gradient_mesh_bg`

```css
body {
  background:
    radial-gradient(circle at 20% 20%, color-mix(in oklab, var(--primary) 30%, transparent), transparent 50%),
    radial-gradient(circle at 80% 80%, color-mix(in oklab, var(--accent) 25%, transparent), transparent 50%),
    var(--bg);
}
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

Web fonts: load via `<style>@import url('https://fonts.googleapis.com/css2?family=…')</style>` — but only inside `_base.html` template. The page-level designer prompt should NOT add new font imports; it inherits from the base.

Actually — to keep pages fully self-contained and avoid network requests during rendering, the base template uses **system font stacks** by default:

```css
:root {
  --font-header: "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", "Hiragino Sans", Inter, system-ui, -apple-system, sans-serif;
  --font-body: "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", Inter, system-ui, -apple-system, sans-serif;
}
```

System fonts are sufficient — the Chromium renderer used by `html_to_pptx.py` has Noto fonts installed.

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
