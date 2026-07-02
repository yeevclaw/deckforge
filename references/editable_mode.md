# Editable Mode — how editing works in PowerPoint

This skill produces SVG-based slides on purpose: **PowerPoint 2016+ natively supports inserting SVGs as editable vector graphics.** But PowerPoint's *Convert to Shape* only turns a *subset* of SVG into native, independently movable shapes (plain `<text>`, `<rect>`, `<circle>`, `<path>`, `<line>`). Anything using features it can't represent — blur/shadow `<filter>`s, gradient washes, glassmorphism, and (unreliably) `<use>`/`<symbol>` icon references — gets **rasterized** into the converted picture, so it can't be moved or resized. That's the asymmetry users hit: text moves, the background and effects don't.

## The two-layer slide

To get the best of both, `svg_to_pptx.py` (by default) builds **each slide as two stacked pictures**:

1. **Background image** — a full PNG render of the whole slide. It carries the atmosphere PowerPoint can't vectorize anyway (gradient backgrounds, glassmorphism, soft drop shadows, glows). Every viewer shows it correctly (Keynote, Preview, Quick Look, PowerPoint <2016). It is **one movable / resizable picture** — you can reposition or scale it, you just can't edit its internals.
2. **Content layer** — a transparent layer carrying the original geometry via the `svgBlip` extension, with the atmosphere removed (it lives in the background image), card shadow `<filter>`s stripped (the soft shadow still shows from the background image; the card itself becomes a clean editable shape), and `<use>`/`<symbol>` icons **inlined into real geometry**. *Convert to Shape* on this layer makes text, cards, icons and lines individually editable / movable / resizable.

The content layer sits exactly over the background image, so the slide looks identical to a single-picture render. Because the background image always carries the full look, a misclassified element is at worst non-editable — never visually wrong.

Pass `--no-decompose` to fall back to the older single-picture model (full render + `svgBlip` on one picture).

## How to edit a slide in PowerPoint

1. Open the produced `presentation.pptx` in **PowerPoint 2016 or newer** (Microsoft 365 also works; 2013 and earlier fall back to the raster — no editing there).
2. To **move or resize the background**, click it and drag / scale like any picture.
3. To **edit the content**, click the content layer, **right-click → Convert to Shape** (or the Graphics Format ribbon's *Convert to Shape* button). PowerPoint decomposes it into:
   - One native text box per `<text>` (each `<tspan>` becomes a paragraph)
   - One native shape per `<rect>`, `<circle>`, `<path>`, `<line>`
   - One freeform-shape group per icon (the inlined geometry)
4. The result is a group; `Ungroup` it (Ctrl+Shift+G) to move/resize individual shapes.

## What stays editable

| Element in the SVG | After Convert to Shape (content layer) |
|---|---|
| `<text>` + `<tspan>` rows | Native PowerPoint text box, each `<tspan>` a paragraph — fully editable |
| `<rect rx="…">` / `<circle>` / `<path>` with a **solid** fill | Native shape (fill/border editable, movable, resizable) |
| `<line>` (incl. dashed) | Line shape (movable, resizable) |
| Inlined icon geometry | Freeform-shape group — movable, resizable, recolorable |
| Card with a shadow `<filter>` | The card becomes a clean editable shape; its **soft shadow** stays in the background image |

## What is NOT vector-editable (lives in the background image)

These are rasterized into the movable background picture — you can move/resize the whole background, but not edit them individually:

- **`<filter>` effects** — soft drop shadows, glassmorphism blur, glows. Blur is raster by nature; PowerPoint has no editable-vector equivalent.
- **Gradient fills used as backgrounds / washes / glows** (`fill="url(#…)"`) and any **translucent shape** (`opacity`/`fill-opacity` < 1) — e.g. glass arches, Venn overlaps, and the `corporate_fresh` glass-flow cards (the white step cards at `fill-opacity` 0.88 sitting on the arches). The **text** on such a card lives in `<text>` and **stays editable**; only the translucent card body itself rides in the background image, so on glass-flow pages you edit the labels, not the card rectangles.
- **Full-canvas background plates.**

This is the intentional trade: the premium look (shadows, glass, gradients) is preserved exactly, and those atmospheric layers are still movable/resizable as one background picture — just not vector-editable. Mark a decorative group `class="atmosphere"` to force it into the background image explicitly.

## Notes & limits

- **Fonts not installed on the viewer's machine**: PowerPoint substitutes the closest available system font, same as any other PPT.
- **Want a single object instead of two?** Use `--no-decompose`. Then *Convert to Shape* still edits text but rasterizes the rest into the one picture (the old behavior).
- **Animated (flow-anim) slides** — any page planning marked with a `motion` field, whether a throughput flow (`transit_rail` / `hub` / `accent_bypass`) or a true cycle (`orbit`) — are embedded as a looping GIF and are **not** Convert-to-Shape editable (the GIF is the whole slide).

## Verifying the embed worked

Open the `.pptx` as a zip and inspect a slide's rels. In the default two-layer mode you should see **two image relationships to `.png`** (background + content) and **one to `.svg`** (the editable content layer):

```bash
unzip -p presentation.pptx ppt/slides/_rels/slide1.xml.rels | grep -Eo 'media/image[0-9]+\.(png|svg)'
```

If only one PNG and no SVG appears, the converter ran in `--no-svg` / `--placeholder-only` mode.

## Working backwards: editing in the SVG instead

For complex edits (multi-page restyling, palette swap), it's often easier to edit `pages/page_*.svg` in a text editor or Inkscape, then re-run `svg_to_pptx.py`. The script is fast — full re-render of a 15-page deck is ~10 seconds with `cairosvg`.
