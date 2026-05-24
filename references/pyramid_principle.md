# Pyramid Principle — Cross-Phase Reference

Barbara Minto's Pyramid Principle is one of DeckForge's two load-bearing methodologies (alongside the Bento Grid layout system). It is **not** a Phase 2 detail — it runs end-to-end from Phase 1's `brief.md` through Phase 3's `planning.json` and is checked again at the Phase 3 → Phase 4 handoff. This reference explains both the principle and where it lives in each phase.

## The four rules

1. **Conclusion first** (結論先行)
   Open every section, every page, with its core claim. Don't bury the lede. Audiences should be able to read just your titles and walk away with the argument.

2. **Top supports bottom** (以上統下)
   A higher-level claim is supported by the level below it. Every supporting point must directly defend the parent claim — not "be about the same topic", but actually *make the parent claim more likely to be true*.

3. **MECE grouping** (歸類分組 — Mutually Exclusive, Collectively Exhaustive)
   Items at the same level must (a) not overlap (mutually exclusive), and (b) together cover the parent claim's full scope (collectively exhaustive). If your three pillars are "speed, reliability, and a great team", that's not MECE — "great team" is a cause of the first two, not a parallel pillar.

4. **Logical progression** (邏輯遞進)
   Order items within a level by a clear principle:
   - **Chronological**: past → present → future
   - **Structural**: north → south, head → toe, top → bottom of the stack
   - **Degree**: highest priority → lowest
   - **Cause-effect**: cause → effect → implication

## How this shows up in the outline

Bad outline (no pyramid):

```
Part 1: 公司介紹
  - 我們是誰
  - 我們的歷史
  - 團隊
Part 2: 產品
  - 產品 A
  - 產品 B
Part 3: 未來
```

Why bad: titles are topic labels, not claims. No clear conclusion. Pillars aren't MECE.

Good outline (pyramid):

```
Part 1: 我們是亞洲最大的 AIoT 解決方案商
  - 三年內服務 50 家 Fortune 500 企業
  - 在 8 個國家建立區域中心
  - 創辦團隊累計 50+ 年產業經驗
Part 2: 我們的產品線已覆蓋 AIoT 全價值鏈
  - 邊緣裝置 — 從感測器到閘道器
  - 雲端平台 — 數據編排與 AI 分析
  - 應用層 — 行業專屬解決方案
Part 3: 2026 年我們將進入服務型營收佔比 50% 的拐點
  - 服務型營收年增 80%
  - 訂閱客戶數突破 1,000
  - 服務毛利率超越硬體毛利率
```

Each title is a complete claim. Each sub-bullet supports the title. The three parts are MECE (who we are / what we do / where we're going).

## Use it as a checklist

When reviewing an outline, run this:

- [ ] Could a reader understand the whole argument by reading only the part titles?
- [ ] Does each page title make a claim, not just name a topic?
- [ ] Do same-level items not overlap?
- [ ] Do same-level items cover the parent claim completely?
- [ ] Is the order within each level explainable in one sentence?

If 5/5 → ship the outline. If <5/5 → revise before Phase 3.

## How pyramid principle shows up across phases

The whole deck is one pyramid. Each phase fills in a different layer:

```
                        APEX  ← Phase 1: brief.md → core_thesis
                          ▲
                          │
                  ┌───────┴───────┐
                  │               │
              LAYER 2  ← Phase 1: proof_pillars  (must be MECE)
                          ↓
                  ┌───────┴───────┐  ← Phase 2: outline.json
                  │   PART TITLES │       (part_title = pillar rephrased as claim)
                  └───────┬───────┘
                          ↓
              ┌──────┴──────┐  ← Phase 2: page titles
              │ PAGE TITLES │       (each title = sub-claim supporting part)
              └──────┬──────┘
                     ↓
            LEAVES ← Phase 3: planning.json → cards
                          (each card = evidence defending its page title)
```

| Phase | What it produces | Pyramid layer | Check enforced |
|---|---|---|---|
| Phase 1 | `brief.md` | apex (`core_thesis`) + layer 2 (`proof_pillars`) | **MECE check on proof_pillars** before writing brief.md. See `prompts/01_needs_research.md`. |
| Phase 2 | `outline.json` | layer 2 (part_titles) + layer 3 (page titles) | part_titles map to proof_pillars 1:1; every title is a claim; **title-only read** test runs |
| Phase 3 | `planning.json` | leaves (card content) | every card defends its page title's claim (on-topic ≠ load-bearing); **title-only read** test runs again at Phase 3→4 handoff |
| Phase 4 | `pages/*.svg` | render only — pyramid is already settled | n/a |
| Phase 5 | `.pptx` + `.pdf` | render only | n/a |

If any phase produces output that breaks the pyramid (overlapping pillars, topic-label titles, off-claim cards), it's caught at that phase's quality checklist and again at the next phase's handoff. The principle is not "applied once at the outline stage"; it's the spine that holds the whole deck together.

## Further reading

- Barbara Minto, *The Pyramid Principle* (the source book — dense, worth it)
- McKinsey's "Storyline" / SCQA framework (Situation, Complication, Question, Answer)
