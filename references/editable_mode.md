# Editable Mode — when you need text to stay text

By default, `html_to_pptx.py` runs in `--mode image`: each HTML page is rendered to a high-DPI PNG and embedded full-bleed in the PPTX. Pros: perfect visual fidelity. Cons: text can't be edited in PowerPoint (it's a pixel).

For users who need to edit text after handoff (typo fixes, translation, brand-team review), use `--mode editable`.

## How editable mode works

Editable mode runs a small parser over each page's HTML and reconstructs the layout as native PPTX shapes via `python-pptx`:

1. Parse the HTML → DOM tree.
2. For each text node, create a PowerPoint text box at the matching position.
3. For each card (`.card` div), create a rounded-rectangle shape with fill/border matching the CSS.
4. For inline SVG icons, embed as a small picture (rasterized to PNG at 4× DPI for crispness).
5. Background gradients are flattened to a single PNG background.

## Trade-offs

| Aspect | `--mode image` (default) | `--mode editable` |
|---|---|---|
| Visual fidelity | Pixel-perfect | ~90% — small layout drift possible |
| Text editing | No | Yes |
| File size | Larger (each slide is a PNG) | Smaller |
| Speed | Faster | Slower (parsing overhead) |
| Complex layouts (mixed_grid, gradient mesh) | Always works | May approximate |

Recommendation: use `image` for client deliverables and demos; use `editable` when the brand or marketing team needs to make text changes after handoff.

## Limitations

Editable mode does not handle:
- CSS animations or transitions (no animation in slides anyway).
- `mix-blend-mode`, `backdrop-filter`, `clip-path` — these are flattened to image.
- Complex SVG illustrations — embedded as rasterized PNG.
- Custom web fonts not installed in PowerPoint — falls back to nearest system font.

## Usage

```bash
python scripts/html_to_pptx.py \
  --pages-dir pages/ \
  --output presentation.pptx \
  --mode editable
```

## Hybrid: best of both

If you want fidelity *and* editable titles, run `image` mode then **add a transparent text-box overlay** on the slide title region. Most editors only need to edit titles, not body cards. This is a manual step but takes ~30 seconds per slide.
