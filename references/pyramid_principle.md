# Pyramid Principle — Quick Guide

The Outline Architect prompt (`prompts/02_outline_architect.md`) is built on Barbara Minto's Pyramid Principle. Read this if you want to understand *why* the prompt is shaped the way it is, or if you want to debug a weak outline.

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

## Further reading

- Barbara Minto, *The Pyramid Principle* (the source book — dense, worth it)
- McKinsey's "Storyline" / SCQA framework (Situation, Complication, Question, Answer)
