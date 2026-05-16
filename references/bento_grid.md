# Bento Grid Layout System

The Bento Grid (便當網格) is a flexible card-based layout system, originally inspired by Japanese bento boxes and popularized by Apple's product pages. It's the **only** layout language this skill uses for content pages.

Why Bento Grid?

1. **It holds a lot of info on one page** without feeling stuffed.
2. **Card count and size are flexible** — fits 2, 3, 4, 5, 6+ items.
3. **It's easy for AI to design well.** Card boundaries give structure that prevents the "everything floating in space" failure mode.
4. **Size = importance** is intuitive for viewers.

## Core principles

| Principle | Rule |
|---|---|
| **Flexibility** | Card count is not fixed. Pick the count that best holds the content. |
| **Hierarchy** | The biggest card holds the most important info. Use size to express priority. |
| **Whitespace** | ≥20px gap between cards. ≥48px page outer margin. Don't fill every pixel. |
| **One motif** | Pick one card style (rounded corners + shadow, accent bar, etc.) and reuse on every page. |

---

## The six layouts

### 1. `single_focus` — one big card

```
+------------------------------------------+
|                                          |
|                                          |
|              [ one card ]                |
|                                          |
|                                          |
+------------------------------------------+
```

Card dimensions: ~1200×580 (full canvas minus margins).

**Use when**: one headline stat, one quote, one chart, one hero claim.

**Don't use when**: you have 2+ ideas of similar weight (use 2-col instead).

---

### 2. `two_col_50_50` — equal halves

```
+-----------------+  +----------------+
|                 |  |                |
|   [ card A ]    |  |  [ card B ]    |
|                 |  |                |
+-----------------+  +----------------+
```

**Use when**: before/after, pros/cons, two parallel ideas, side-by-side comparison.

---

### 3. `two_col_2_1` — asymmetric

```
+------------------------------+ +------------+
|                              | |            |
|       [ card A — big ]       | | [ card B ] |
|                              | |            |
+------------------------------+ +------------+
```

Wide card ~2/3, narrow ~1/3.

**Use when**: one main idea + one supporting detail (a sidebar, a stat callout, an image).

---

### 4. `three_col` — three equal columns

```
+----------+  +----------+  +----------+
|          |  |          |  |          |
| [card A] |  | [card B] |  | [card C] |
|          |  |          |  |          |
+----------+  +----------+  +----------+
```

**Use when**: three parallel pillars (values, steps, features, comparisons).

**Don't use when**: only 2 items (looks lonely) or 4+ (use mixed_grid).

---

### 5. `hero_top` — hero + grid below

```
+------------------------------------------+
|              [ hero card ]               |
+------------------------------------------+
+--------+  +--------+  +--------+  +-----+
| card B |  | card C |  | card D |  |  E  |
+--------+  +--------+  +--------+  +-----+
```

Top card spans full width. Below, 2–4 smaller equal-width cards.

**Use when**: one headline claim + 2–4 supporting details / stats / steps.

---

### 6. `mixed_grid` — asymmetric freeform

```
+----------+  +----------+----------+
|          |  |          |          |
| [ big A ]|  | [ med B ]| [ med C ]|
|          |  +----------+----------+
|          |  |       [ wide D ]   |
+----------+  +-----------+--------+
```

Combine sizes freely. Most flexibility, most design judgment required.

**Use when**: 4–6 items of varying importance.

**Caution**: easiest layout to overdo. If you have to think hard about it, use one of the simpler layouts.

---

## CSS grid templates

All templates assume a 1280×720 viewport with 48px outer padding.

```css
:root {
  --slide-w: 1280px;
  --slide-h: 720px;
  --pad: 48px;
  --gap: 20px;
}

.slide {
  width: var(--slide-w);
  height: var(--slide-h);
  padding: var(--pad);
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.slide-title { font-size: 40px; font-weight: 700; margin: 0 0 8px; }
.slide-subtitle { font-size: 18px; opacity: 0.7; margin: 0 0 32px; }

.bento {
  flex: 1;
  display: grid;
  gap: var(--gap);
}

.bento.single_focus { grid-template-columns: 1fr; }
.bento.two_col_50_50 { grid-template-columns: 1fr 1fr; }
.bento.two_col_2_1 { grid-template-columns: 2fr 1fr; }
.bento.three_col { grid-template-columns: 1fr 1fr 1fr; }

.bento.hero_top {
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: 1fr 1fr;
}
.bento.hero_top > .card.hero { grid-column: 1 / -1; }

.bento.mixed_grid {
  grid-template-columns: repeat(6, 1fr);
  grid-template-rows: repeat(3, 1fr);
}
/* Card placement is content-specific in mixed_grid */

.card {
  background: var(--card-bg, #fff);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.card .icon { width: 48px; height: 48px; }
.card h3 { font-size: 22px; margin: 0; }
.card p { font-size: 15px; margin: 0; line-height: 1.55; }
```

The starter templates in `templates/` already include this base CSS plus motif variants.

---

## When NOT to use a Bento Grid

- **Cover page**: hero text + bg. Skip the grid.
- **Section break**: huge title + tiny subtitle. Skip the grid.
- **Quote page**: a single oversized quote can use `single_focus` or just centered text.
- **End page**: simple "thank you" + contact. Skip the grid.

For these page types, use `single_focus` or no grid at all — see the templates folder.
