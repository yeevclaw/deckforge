# Phase 0 — Source Analysis (文件分析)

Use this **when the user supplies a source document** (PDF, .docx, transcript, long-form text, annual report, whitepaper, blog post, paper) rather than just a topic. You analyze the document first, producing a structured analysis report, before any deck planning starts.

> **The single biggest reason AI decks from documents look generic** is skipping this step. Treating a 100-page annual report as "just a topic" loses 95% of the actual signal — names, numbers, comparisons, parallel claims. This phase forces a careful pass that pulls those out before the deck thinks about itself.

Adapted from the linux.do "Xiaomi annual report → web visualization" methodology by *sandun*: stage 1 produces a structured analysis, stage 2 turns it into visual cards. Two stages, both essential.

---

## When to run Phase 0

✅ Run when:
- The user attached a document and said "make me a deck from this"
- The user pointed at a URL with substantial content (article, report, paper)
- The user pasted a long block of text (>1000 chars) and asked for a deck
- Even if the user gave a topic, if there's a source they referenced, read it first

❌ Skip when:
- The user gave only a topic with no source ("make me a Series B deck about our AI platform"). In that case, go to Phase 1 (Needs research) directly.
- The source is trivial (a few paragraphs, a tweet). Just incorporate inline.

When in doubt, **run it**. A clean analysis pass is cheap; missing facts is expensive.

---

## AI Task — be a senior analyst, not a summarizer

> Read the source document end-to-end. Then act as a senior analyst writing a brief for a presentation team. Extract the **specific, concrete, citable** material a designer needs to build a deck — not a paraphrase.

The mistake to avoid: producing a 3-paragraph summary. That throws away the data. The output here should be **structured, extractive, and longer than the deck itself**. The deck will pick from it; this phase shouldn't pre-filter.

---

## Master prompt

When invoking the analysis on the source, use language adapted from sandun's original Xiaomi prompt:

```
You are a senior analyst. The source document is attached. Please:

1. Summarize the overall situation (who, what, scale, context — 3–5 sentences).
2. Extract every key metric: revenue numbers, growth rates, market share figures,
   user counts, margins, dates, named entities. Format each as
   `<value> · <CN caption> · <EN caption>` (e.g., "42% · 三年複合年成長率 · CAGR").
3. Identify the 3–8 most important claims or arguments the document makes.
4. Identify any sets of parallel items (3+ comparable items that could become
   a mini-card grid): product lines, business segments, pillars, risks, steps,
   regions, fiscal periods, etc. List each set explicitly.
5. Flag exceptions, anomalies, or surprising findings (good fodder for hero stats).
6. Note 1–2 contrarian or counter-views if mentioned (for balanced framing).
7. Note the source's tone (formal/upbeat/cautious/regulatory) so the deck can
   match.

Use the source's exact language for names and numbers. When the source uses
specific terms ("AIoT", "Robotaxi", "FY24"), preserve them. Don't paraphrase
numbers; quote them.

Length: produce enough material that a deck designer wouldn't need to re-read
the source. As a rough heuristic, ~10× the deck length in raw notes.
```

---

## Output format

Save to `analysis.md` in the working directory:

```markdown
# Source Analysis: <source title>

## Overall situation
<3–5 sentences>

## Key metrics
- 42% · 三年複合年成長率 · CAGR · 2023–2025
- NT$510 億 · 2025 年營收 · FY2025 Revenue
- 26% · 毛利率(由 18%) · Gross Margin
- ...

## Top claims / arguments
1. <claim 1, with the source's wording>
2. <claim 2>
3. ...

## Parallel sets (each can become a mini_grid page)
- **Business segments**: 智慧電動車 · AIoT 平台 · 互聯網服務 · 國際拓展
- **Quarterly trend**: Q1 → Q2 → Q3 → Q4
- **Risk factors**: 監管 · 競爭 · 供應鏈 · 匯率
- ...

## Anomalies / surprising findings
- <finding> — why it matters
- ...

## Counter-views
- <opposing view if any>

## Source tone
<formal / upbeat / cautious / regulatory / academic>
```

---

## Handoff to Phase 1 — ask for approval, never silent

After `analysis.md` is written, **do not start Phase 1 silently**. Ask the user via `AskUserQuestion` whether they want to continue:

```
Question: Phase 0 完成（已產出 analysis.md，含 <N> 個關鍵數字 / <M> 組平行集合）。要繼續進入 Phase 1 蘇格拉底反詰嗎？

  ○ 繼續進入 Phase 1 (Recommended)
       → 我會根據文件抽出的主線，用跳窗反詰幫你定 thesis 跟 belief shift
  ○ 我要先檢視 analysis.md
       → 你看完告訴我哪邊要補抓或重抓
  ○ 暫停在這裡
       → analysis.md 已存好，之後可以再回來繼續
```

Only continue when they approve. The same approval discipline applies at every phase boundary — see SKILL.md "Every phase handoff requires explicit user approval".

## Passing to Phase 1 (Socratic Clarification) — DO NOT SKIP

> Phase 0 produces *material*. It does NOT produce a thesis.
>
> Even when `analysis.md` is rich (60+ metrics, multiple parallel sets, clear anomalies), you **must** run Phase 1 next — never jump to Phase 2 directly. The analysis tells you what's *in the document*; Phase 1's Socratic loop tells you what *judgment must change in the audience's head*. Those are different things, and skipping Phase 1 is the most common reason document-driven decks come out as generic summaries instead of decisions.

When Phase 1 runs, hand it `analysis.md` as context. Phase 1's first Socratic question typically becomes: "I see three possible storylines from the document — which one are we writing the deck around?" The user picks one storyline; Phase 1 then layers in `audience / belief_shift / core_thesis / desired_action` via further Socratic rounds; only then is `brief.md` written and Phase 2 begins.

The handoff order is non-negotiable:

```
Phase 0 (analysis.md)  →  Phase 1 (brief.md)  →  Phase 2 (outline.json)
                          ^^^^^^^^^^^^^^^^^^
                          cannot be bypassed
```

## Passing to Phase 2 (Outline) — via Phase 1, not directly

When you eventually run Phase 2's prompt, paste the relevant sections of `analysis.md` as the **背景調研信息 (Context)** block, alongside `brief.md`. The Outline Architect prompt is designed to consume both — page titles should make claims grounded in the analysis, parallel sets should suggest pages with `mini_grid` layouts, and key metrics should hint at `stat_hero` pages. But the *spine* of the outline comes from `brief.md`'s `core_thesis` + `proof_pillars`, not from the analysis itself.

---

## Quality checklist

Before declaring Phase 0 done:

- [ ] Are there **at least 6 specific metrics** with both CN and EN captions?
- [ ] Did I extract **named entities** (products, people, regions, dates) verbatim from the source?
- [ ] Did I find **at least 2 parallel sets** (3+ comparable items each) that could each become a mini_grid?
- [ ] Did I flag **at least 1 anomaly or surprising finding** that could anchor a stat_hero page?
- [ ] Did I avoid paraphrasing numbers (quoting exactly)?
- [ ] Is the source tone noted, so the deck can match register?

> Gradeable mirror: [references/rubric.md](../references/rubric.md) → "Phase 0" (ids P0-01..P0-06). Graders and `scripts/check_docs.py` reference these by id — keep them in sync.

If you got fewer than these counts, **the source has more material** — re-read it. Phase 0 is the only place this material can come from cheaply.

---

## Why this stage matters

A common failure mode without Phase 0:

> User uploads a 379-page annual report. Claude reads ~5 pages, generates a 12-slide deck. Slides have generic claims ("revenue grew significantly", "the company expanded into new markets"). Specific numbers are missing or wrong. Designer fills with placeholder stats.

After Phase 0:

> Claude reads the full report, extracts 60+ specific metrics with captions, identifies 5 business segments as a parallel set, flags Q3's profit anomaly. Deck has `stat_hero` pages for the 3 most striking numbers, a `mini_grid` showing all 5 segments side-by-side, and concrete numbers everywhere.

The deck quality difference is enormous. The cost is one extra analyst-mode pass before designing — a small price for the difference between "AI generated" and "actually useful".
