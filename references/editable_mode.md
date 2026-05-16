# Editable Mode — how editing works in PowerPoint

This skill produces SVG-based slides on purpose: **PowerPoint 2016+ natively supports inserting SVGs as editable vector graphics.** When `svg_to_pptx.py` builds the deck, each slide's picture carries both a rasterized PNG fallback *and* the original SVG (via the `svgBlip` OOXML extension). PowerPoint renders the vector by default and lets the user decompose it into native shapes for editing.

## How to edit a slide in PowerPoint

1. Open the produced `presentation.pptx` in **PowerPoint 2016 or newer** (Microsoft 365 also works; older 2013 and earlier will fall back to the PNG raster — no editing in those versions).
2. Click on a slide so its picture is selected.
3. **Right-click → Convert to Shape**, or use the Graphics Format ribbon's *Convert to Shape* button.
4. PowerPoint decomposes the SVG into:
   - One native shape per `<rect>`, `<circle>`, `<path>` (fill, stroke, rounded corners preserved)
   - One native text box per `<text>` (with each `<tspan>` becoming a paragraph)
5. From here every text run, color, and shape is editable using PowerPoint's normal tools.

After Convert to Shape the slide is a regular collection of grouped objects; you can `Ungroup` it (Ctrl+Shift+G) to edit individual shapes.

## What stays editable

| Element in the SVG | After Convert to Shape |
|---|---|
| `<text>` + `<tspan>` rows | Native PowerPoint text box, each `<tspan>` becomes a paragraph |
| `<rect rx="…">` | Rounded rectangle shape (fill/border editable) |
| `<circle>` | Oval shape |
| `<path>` | Freeform shape |
| `<filter>` drop shadow | Approximated as shape effect (sometimes flattened to raster — minor visual drift) |
| `<radialGradient>` / `<linearGradient>` | Native gradient fill |
| Lucide icon `<path>` | Editable freeform shape (you can recolor by selecting and changing fill/line) |

## What may not survive perfectly

- **Complex `<filter>` chains** (multi-stage shadow + blur + colormatrix) may be rasterized inside the converted shape. Visual result is preserved, but you can't tweak filter parameters.
- **`<symbol>` / `<use>` references** that span multiple definitions: PowerPoint usually inlines them, but rarely you'll need to ungroup twice.
- **Fonts not installed on the viewer's machine**: PowerPoint substitutes the closest available system font, same as any other PPT.

## When NOT to Convert to Shape

If the user only wants to *view* or *print* the deck, leave it as a picture. The PNG fallback + vector embedding both work fine without conversion — Convert to Shape is only needed when someone wants to edit the slide contents.

## Verifying the SVG embed worked

Open the `.pptx` as a zip and inspect `ppt/slides/_rels/slide1.xml.rels`. You should see two image relationships — one to `media/image1.png` (the fallback) and one to `media/image1.svg` (the source). If only the PNG appears, the converter ran in `--mode raster`. Re-run with the default `--mode svg`.

```bash
unzip -p presentation.pptx ppt/slides/_rels/slide1.xml.rels | grep -E 'image.*\.(png|svg)'
```

## Working backwards: editing in the SVG instead

For complex edits (multi-page restyling, palette swap), it's often easier to edit `pages/page_*.svg` in a text editor or Inkscape, then re-run `svg_to_pptx.py`. The script is fast — full re-render of a 15-page deck is ~10 seconds with `cairosvg`.
