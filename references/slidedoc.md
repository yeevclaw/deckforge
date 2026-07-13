# Slidedoc — the reading-mode design language

The canonical reference for `delivery_mode: "reading"` pages. The planner's rule forks
live in `prompts/04_planning_draft.md` → "Delivery mode"; the designer's hard rule is
`prompts/05_designer_svg.md` → Hard rule #12; this file is the design language itself —
what a DeckForge reading page looks like and why.

---

## 1. What reading mode is

A reading deck is sent out and consumed standalone — a pre-read before the meeting, a
leave-behind after it, an emailed briefing nobody will ever present. In Nancy Duarte's
vocabulary it is a **slidedoc**: a document wearing slide geometry. The defining fact is
that **the deck is its own presenter** — every sentence a presenter would have said out
loud must either be on the page or not exist. That single fact drives everything below:
fuller prose, an explicit reading order, a layered skim path, and the fold-back of
speaker-note content onto the page.

Reading mode is **not a new visual family**. It is a density-and-layering overlay on the
two light families that already argue in prose (`IT_prism`, `corporate_fresh`). Their
sentence-driven scale is 80% of a slidedoc already; this file adds the missing 20%.

## 2. The reading floor — the mode's single hard rule

> **In a reading-mode page, no text run renders below 16px on the 1280×720 canvas
> (= 12pt on the exported 16:9 slide: 1280px ÷ 13.333in = 96px/in; 12pt = 16px).**
> A reader holds the page at laptop or print distance with no presenter to say the small
> print aloud — text too small to read is text that does not exist. Everything else in
> this mode is judgment; this is not.

Enforced mechanically: the designer stamps `data-delivery-mode="reading"` on the root
`<svg>` (Hard rule #12) and `scripts/check_svg.py` fails any font-size below 16 in a
file that carries the attribute (rubric P4-13). The per-element deltas are in
`references/design_system.md` → "Delivery mode — reading (slidedoc) overlay".

## 3. 三層閱讀 — the layered-read architecture

A slidedoc serves two readers at once: the skimmer (30 seconds for the whole deck) and
the deep reader (a careful pass). Three layers, each an extension of a device the
harness already owns:

1. **Assertion-title spine** (layer 1 — exists, strengthened). Pyramid Rule 1 already
   demands that titles alone tell the argument. Reading mode extends the test one layer
   down: **titles + bold lead-ins alone must reconstruct the argument.** That is the
   skim read. Run it before emitting a reading deck the way you run the title-only read.
2. **Bold lead-in per body block** (layer 2 — the one genuinely new device). Every body
   block of **≥2 sentences opens with its claim, set bold in the ink voice** — the first
   phrase of the block, not a separate heading. `IT_prism`: `#344252` bold, **without**
   the green device; `corporate_fresh`: `#383838` bold, **never orange**. The lead-in is
   a *structural* bold, not an emphasis run — a lead-in painted in the emphasis voice
   collapses layers 2 and 3 into one and the hierarchy is gone.
3. **Inline emphasis runs** (layer 3 — exists, tightened). The family's emphasis device
   (prism: ink bold + green band/underline/pill; fresh: orange bold run) marks the
   **fact to retain**, at most **1 run per body block** in reading mode (presenting
   allows 1–2). The lead-in marks the claim; the emphasis marks the evidence.

Rejected mechanisms, so nobody reinvents them: numbered eyebrows on every card (imposes
false sequence on parallel content — genuinely ordered content already has
`numbered_steps` / `flow` / `timeline`); explicit reading-flow arrows (form outshouting
message — the grid already encodes the path); a second accent or color-coded layers
(violates the single-highlight / role-discipline core invariant); a side annotation rail
(steals ~25% of every layout's width — the note strip in §6 does the job for 60px of
height).

## 4. Reading order — the grid is the path

No new visual mechanism; one judgment rule:

> **Bento geometry *is* the reading order.** A reader traverses top-left → top-right →
> next row (the Z-path). On a reading page, order the cards so that traversal matches
> the argument's logical order — setup before payoff, options before recommendation,
> evidence before conclusion. Never park the concluding card mid-grid because it
> "balanced the composition".

## 5. One card, one argument — and the wrap math

The planner's fork (`prompts/04_planning_draft.md`): a reading card carries **one
argument** — a claim line (the lead-in) plus the 2–4 sentences that complete it — and
never a second claim. The designer's side of that bargain is making the block fit,
because SVG has no auto-wrap:

> **Wrap math before you write.** CJK chars per line ≈ card inner width ÷ font-size
> (a 381px `three_col` column at 19px ≈ 17 chars/line; a 568px `two_col_50_50` card
> ≈ 26). Line pitch at lh 1.85 ≈ 35px. Budget the block: lead-in (1 line) + N body
> lines × 35px must land inside the card with ≥32px bottom padding. If the argument
> needs more lines than the card holds, the card is on the wrong layout — promote to
> `two_col_50_50` or `single_focus`. **Never shrink below the 16px floor to make it
> fit.**

Overflow itself is already gated (P5-01); the math above is how you never meet that
gate.

## 6. The note strip — where speaker notes go to live

Reading pages fold Tier-2 content (what the presenter would have *said*) onto the page.
Card-worthy support goes into the body or `sub_cards`; the rest goes to the page's
`reading_notes` field, rendered as a **full-width, visually quiet footer strip**:

- **Geometry**: on a page carrying `reading_notes`, the bento band shortens to
  `y=140..630` (h=490, from the standard 532). A hairline rule at `y≈648`, x 48→1232 —
  `IT_prism`: solid `#DFE2E9`; `corporate_fresh`: dashed round-dot `#9FB9AE`. Note text
  starts `y≈676`: 1–2 lines, **16px** (the floor — never smaller), line-height ~1.5,
  prefixed by a small ink label `註 ·` / `資料來源 ·` / `Note ·`.
- **Color**: the on-canvas secondary token — `#4C5A6B` on prism (the wash-safe token;
  `#6B7686` is a white-card token and fails AA on the wash), `#6B7178` on fresh.
- **Pages without notes keep full-height cards** — the strip is not chrome that appears
  empty.

**The voice rule (this is the P5-10 firewall):**

> The note strip is the **quiet voice**: sources, methodology, denominators, historical
> baselines, caveats — content a presenter would have said in passing. It never carries
> a conclusion, a CTA, or anything that maps back to the title: the P5-10 title-echo
> rule applies to the strip verbatim. If a sentence in the strip feels like it deserves
> bold, it is Tier-1 content on the wrong layer — move it onto a card.

## 7. Per-layout reading recipes

| Bucket | Layouts | Reading note |
|---|---|---|
| **Workhorses (bias toward)** | `two_col_50_50`, `two_col_2_1`, `single_focus`, `compare_table`, `hero_top`, `three_col` (`lead_plus_pair` / `axis_labeled`), `mini_grid`:`ribbon_row`, `flow`:`cascade_fall`, `timeline` | absorb 2–4-sentence argument blocks naturally; `cascade_fall`'s trigger already reads "steps that need longer prose" |
| **Fine as-is** | `mixed_grid`, `quadrant_2x2`, `pyramid`, `hierarchy_tree`, `funnel`, `venn`, `cycle`, most `chart_*` | 16px label floor applies; primitives reduce node count before shrinking text (≤4 flow steps, ≤3 pyramid tiers when nodes carry prose) |
| **Adapted recipe** | `stat_hero` — rare in reading mode; a bare number with a 1-line caption assumes a presenter to interpret it. When the number truly is the message, pair it with a 2–3-sentence interpretation block (or use `single_focus` + `sub_cards`). `toc` may carry a one-line summary per section — the slidedoc navigation page. | |
| **Bias away** | 5-up `mini_grid` `even_grid` (200px cards can't hold prose — use 3–4 cards or `ribbon_row`), `chart_mekko` / `chart_radar` at high series counts (16px labels collide — reduce categories or switch to `chart_hbar`), motion pages (a GIF in an emailed deck read as PDF/print is dead weight and costs Convert-to-Shape editability) | |

## 8. Family notes

- **`IT_prism`** — the natural default carrier. Its highlight band already carries the
  skim path; reading mode adds the ink-bold lead-ins (without the green device) and
  floors the small annotation sizes at 16px. Everything else in the family spec applies
  unchanged.
- **`corporate_fresh`** — equally at home; "text density is a feature" is this family's
  own line. Lead-ins are `#383838` bold; orange keeps its single inline-emphasis run per
  block and **never** paints a lead-in.
- **`dark_apple` — presenting-only.** Its entire language is number-driven drama:
  80–120px heroes, 11–13px captions, "push to number 80px / body 14px". Retrofitting
  prose onto pure black produces gray text walls — the family's own documented failure
  mode — and emailed decks get printed, where full-bleed black is hostile. Reading decks
  resolve to a light family; if the user explicitly insists on dark + reading, the 16px
  floor still applies and the planner surfaces the tension rather than silently
  complying.

## 9. Reading-mode mistakes

- **The lead-in painted in the emphasis voice** (green device on prism, orange on
  fresh). Layers 2 and 3 collapse into one; the skim read is gone. Ink bold, always.
- **The note strip carrying a conclusion** or a paraphrase of the title. The strip is
  the quiet voice — P5-10 applies to it verbatim.
- **Keeping every EN decorative caption at 16px.** At the floor size, English decoration
  starts competing with the CN core. In reading mode bilingual polish is the first thing
  traded for prose room — cut most of it; what stays rises to 16px.
- **Prose crammed into a 5-up `mini_grid`.** 200px-wide cards hold captions, not
  arguments. 3–4 wider cards or `ribbon_row`.
- **A motion page in an emailed deck.** The reader sees a static frame in the PDF and
  loses Convert-to-Shape on that slide. Motion budget in reading mode: 0–1, and only
  when slideshow viewing is actually expected.
- **Density without layers.** More text is licensed only together with the three-layer
  architecture (§3). Dense prose with lead-ins is a slidedoc; dense prose without them
  is the reading-mode text wall — exactly what P5-08's reading branch fails.
