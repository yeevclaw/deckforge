# Brief

<!-- Golden fixture for the change-time verification loop — the READING pair
     (.claude/skills/deckforge-verify). Exercises delivery_mode: reading +
     reading_notes + one per-page presenting override. Frozen input: edits to
     this file and evals/planning_reading.json happen only together, in their
     own commit, re-baselined by one content-grader (07) pass. Guarded by
     scripts/check_docs.py check 8. -->

## Scenario
executive-briefing

## Audience
- **Who**: 營運長（COO），客服部門預算的最終核准者
- **Current belief**: 客服品質問題只能靠增聘人力解決，AI 客服等於品質降級

## Belief shift
- **From**: 客服規模 = 人力規模，導入 AI 是砍成本、犧牲品質
- **To**: 中台化讓品質與規模脫鉤——AI 中台同時降成本、升品質，而且十二週就能落地

## Core thesis
導入 AI 客服中台，能在不增加人力的前提下，把首次解決率從 58% 提升到 80%，同時把單張工單成本降低三分之二。

## Proof pillars
1. 成本結構重寫 — 證據: 三個月 pilot 實測，單張工單處理成本 NT$180 → NT$62（-66%），八個月回收導入成本
2. 品質不降反升 — 證據: pilot A/B 對照，五大客服管道首次解決率由 58% 升至 71–82%，平均首次回覆時間 4.2 小時 → 11 分鐘
3. 十二週可落地 — 證據: 架構評估報告確認四步導入（盤點→接入→試點→全面），不改動既有 CRM 與工單系統

## Likely objections
- 客服團隊會反彈：AI 是要取代他們嗎？（回應：中台接一線重複題，人力轉二線高價值案件）
- 客戶資料進入模型的資安疑慮（回應：pilot 已通過資安部門 DLP 審查，資料不出私有雲）

## Desired action
核准 Q3 全面導入預算（NT$1,200 萬），並指定客服部與 IT 部共同立項。

## Constraints
- **Page count**: 5（fixture 固定）
- **Tone**: data-heavy
- **Language**: zh-TW
- **Delivery mode**: reading — 核准會議前三天寄給 COO 的 pre-read，獨立閱讀無講者；例外：第 4 頁（結論數字頁）保留在會議現場由提案人開場展示，標 presenting
- **Brand**: 無特殊限制
- **Visual style hint**: IT_prism

## Open assumptions
- 假設 pilot 的三個月數據可線性外推至全量（Q3 導入後以雙週報驗證）

## Source material
none（合成 fixture，數字為虛構但自洽；與 evals/brief.md 同一題材的 reading 版本）
