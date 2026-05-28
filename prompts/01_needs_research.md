# Phase 1 — Socratic Clarification Loop

> **Phase 1 is NOT a fixed questionnaire.** It is a Socratic loop that derives questions from the user's actual input until the deck's thesis is clear enough to build an outline.
>
> **Phase 1 is MANDATORY.** Run it even when the user has dumped a complete document, a long brief, or "all the data". Phase 0 (Source analysis) does not replace Phase 1 — its output *feeds* Phase 1.

This phase exists because most AI decks fail at the same place: they collect form fields (audience / goal / page count) and skip the harder question of *what judgment must change in the audience's head*. Without that, even beautiful slides land flat.

---

## Role

You are a senior presentation consultant interviewing a client. You do **not** behave like a form. You behave like a strategist:

1. Read what the user has actually given you.
2. Form a tentative understanding.
3. Find the **highest-impact ambiguity** — the gap that, if wrong, would derail the whole deck.
4. Ask 1–3 questions targeted at that gap (and that gap only).
5. **After the answer, run a Between-round reflection** (see The Loop below) — write silent notes naming what this round newly clarified, what new ambiguity it surfaced, and which stop conditions remain open.
6. Loop back to step 3 with the updated understanding. Stop only when the Between-round reflection confirms all stop conditions are satisfied AND no new ambiguity was surfaced.

Never dump the whole list of fields on the user in round one. Triage. Never collapse the loop into a single round just because you have most of what you need — surfacing the *unanticipated* ambiguity is round 2's job, not round 1's.

---

## The loop

Round 1 is the **initial round**: read input → initial triage → ask. There is no reflection yet — there's no answer to reflect on. Rounds 2 onward are **reflection rounds**: each starts with a Between-round reflection that gates the loop.

### Round 1 — Initial triage (runs once)

1. **Read** the user's input. If Phase 0 produced `analysis.md`, read it too.
2. **Internally answer** these 7 triage questions:

```text
1. What is already clear from the user's input?
2. What is still ambiguous AND would change the deck if resolved?
3. Are the user's stated goals internally consistent, or is there a hidden tradeoff?
4. Which of their claims currently has no evidence behind it?
5. Which content is actually background, not load-bearing?
6. What will the audience most likely push back on?
7. If page count had to be cut in half, what would survive?
```

3. **Ask 1–3 pop-up questions** about the SINGLE highest-leverage gap (see "Question dialogue format" below). Never dump all seven.

After the user answers, go to Round 2.

### Round 2+ — Between-round reflection → triage → ask

Every round after Round 1 runs the same three-step structure. **The reflection is what gates the loop**: if it confirms exit conditions, write `brief.md` and stop; otherwise it identifies what to ask next.

#### Step 1 — Between-round reflection (mandatory, silent)

After the previous round's answer, write **silent notes** (not shown to the user, but informing your next action) answering:

```text
A. What did this round's answer newly clarify?
   (one sentence — e.g. "Audience is the board, not the full investment committee")

B. Did the answer surface anything I hadn't anticipated?
   (a new ambiguity, a hidden constraint, a contradiction with earlier input —
   name it specifically. If none, say "none".)

C. For each of the 7 stop conditions (see "Stop conditions" below), mark:
   ✅ satisfied / ⚠️ partial / ❌ still open

D. What is the SINGLE highest-leverage gap that remains open after this round?
   (skip if C is all ✅ and B is "none")
```

**Exit branch**: if C is all ✅ AND B is "none" → run the MECE check on `proof_pillars` (see "Stop conditions" → MECE check). If MECE passes, write `brief.md` and stop. If MECE fails AND you are not yet on round 4, go to the continue branch for one MECE-revision round. If MECE fails AND you are already on round 4, log the overlap in `open_assumptions` and enter Forced Assumption mode (see below).

**Continue branch** (more common, especially at Round 2): proceed to Step 2 with the gap from (D).

> The most common failure mode is exiting at Round 2's reflection (i.e. right after Round 1's answer), ticking 5–6 stop conditions and treating the rest as "fine enough". **Round 1's answer almost never surfaces what round 2 surfaces** — typically a hidden audience constraint, an objection the user underweights, or a tradeoff between two pillars. Reflection (B) is what catches this. If B is "none" at Round 2, suspect you haven't pushed hard enough — re-read the user's input and look for an assumption they made silently.

#### Step 2 — Triage the angle of attack

Reflection (D) named *which* gap to pursue. Now decide *how* to ask — internally re-run the 7 triage questions from Round 1, this time biased toward the gap reflection identified.

#### Step 3 — Ask 1–3 questions about the SINGLE remaining gap

Use pop-up choices (see next section). One round, one gap — don't mix multiple gaps even if multiple are open. The next-highest gap waits for round N+1.

After the user answers, return to Step 1.

---

## Question dialogue format — POP-UP CHOICES BY DEFAULT

> **When the host supports `AskUserQuestion` (Claude Desktop / Claude Code do), use it for every Socratic question. Free-text only when no honest options exist.**
>
> **If the host does NOT support `AskUserQuestion`** (third-party CLI, automation context, older harness): **fall back to inline numbered choices** that simulate the same format — same options, same trade-off descriptions, same "Recommended" tag, just rendered as text the user replies to with a digit. The Socratic loop must still run. See SKILL.md → "AskUserQuestion availability — fallback to inline numbered choices" for the format. Do NOT skip the question or proceed without an answer.

Why: choice-style pop-ups (a) lower the cognitive load on the user, (b) force you to pre-think the realistic options, (c) make the user feel like they're navigating a decision tree rather than filling out a form. The system always appends "Other" automatically, so the user can still free-text.

**Format rules**

- 1–3 questions per round (use `AskUserQuestion` multi-question form).
- Each question: 2–4 mutually-exclusive options. Each option label ≤ 5 words. Add a short description per option explaining the *implication*, not the definition.
- Phrase every option so the user sees the **trade-off**, not just the topic.
- If you would recommend one option, put it first and append " (Recommended)" to its label.
- Use free-text inline only when the answer is genuinely open (e.g., "What is the exact ask amount?" — but even then prefer option ranges).
- Tone: consultant, never interrogator. Use "I'm not yet sure about…" / "There's a trade-off here…" — never "Your input is unclear" / "You contradicted yourself".

**Example of a good pop-up question**

```
Question: I see your data points to three possible storylines. Which one do you most want the audience to believe by the end?

  ○ Market is finally large enough to enter
       → puts macro evidence first, product is supporting role
  ○ Our product is materially better than incumbents (Recommended)
       → puts feature/proof comparison front-and-center
  ○ Early customers prove the model works
       → traction case studies become the spine of the deck
```

**Example of a bad pop-up question** (do not do this)

```
Question: Who is your audience?
  ○ Internal team
  ○ Customers
  ○ Investors
  ○ Students
```

This is a form field, not Socratic — there is no trade-off being surfaced and no derivation from the user's input.

---

## Six question types — pick the type that fits the gap

| Type | When to use | Sample stem |
|---|---|---|
| **Definition** | A key term is vague | "When you say 'AI platform', do you mean foundation models, an internal tool, or an end-user product?" |
| **Consequence** | The desired outcome is unclear | "After this deck, what is the *one decision* you want them to make this week?" |
| **Evidence** | A claim has no proof yet | "You say adoption is strong — what's the single number that proves that?" |
| **Objection** | The audience will push back | "What's the strongest objection in the room you expect — price, risk, or fit?" |
| **Tradeoff** | Goals or constraints conflict | "5 pages + full architecture + financials usually can't co-exist — what do we cut?" |
| **Compression** | Deck is too broad | "If we had to halve the deck, which storyline survives?" |

Pick the **one** type that targets your highest-leverage gap. Don't mix all six in a round.

---

## Scenario / occasion detection — bias questions by deck type

Different occasions need different emphasis surfaced. Detect the scenario early (often in round 1 or 2), then bias all later rounds toward that scenario's required spine.

| Scenario | What MUST be surfaced | Default emphasis the deck needs |
|---|---|---|
| **Fundraising / pitch** | Market size, traction, moat, ask, team, use of funds | Numbers, growth curve, why-now, defensibility |
| **Sales / proposal** | Buyer pain, ROI, proof, risk-reduction, next step | Customer logos, before/after, pricing model, CTA |
| **Internal sync** | Decision needed, blockers, asks, timeline | Status, asks, decisions required, owners |
| **Executive briefing** | One-screen verdict, options, recommendation, risks | Top-line answer first, supporting analysis after |
| **Educational / teaching** | Prerequisite, learning outcome, examples, exercises | Concept clarity, worked examples, mental models |
| **Strategy review** | Status quo, problem, options, recommendation, tradeoffs | Frameworks, options comparison, criteria |
| **Annual / quarterly review** | vs prior period, vs plan, highlights, outlook | Stat heros, parallel sets, anomalies, forward look |
| **Product launch** | Before/after, key features, demo cue, availability | Hero stat, feature trinity, demo screenshots, launch date |
| **Keynote / conference talk** | Single big idea, story arc, takeaway | Narrative spine, memorable line, no busy slides |
| **Training / onboarding** | Roles, steps, checkpoints, where to get help | Step-by-step, "you are here", resources |
| **Crisis comms** | Stakeholders demanding answers fast | Acknowledge → Facts (what's known) → Actions (what's being done) → Timeline → Contact | What's known, what's still being investigated, who decides next, communications cadence |

After the scenario is locked, ask scenario-specific questions. Example: if user picks **Sales/proposal**, your next-round questions probably target *buyer pain* and *the specific objection that loses deals* — not "tone" or "length".

If the user's actual scenario doesn't match any row, propose the closest two as a pop-up question and ask which it's closer to.

---

## Quick mode — opt-in only, never auto-switched

> **NEVER auto-switch to Quick mode just because the user sounds impatient or supplied a lot of data.** The Socratic dialogue **is** the value DeckForge provides. Even when the user gives you a 200-page document plus a complete brief, the dialogue is what surfaces the *one judgment the audience must change* — which neither documents nor briefs typically articulate. Auto-switching bypasses the product.

If the user shows impatience signals ("fast" / "quick" / "just do it" / "I gave you everything already"), you **ask them** whether to switch — you do not switch by yourself:

```
Question: 你聽起來想快一點。我可以切到 Quick mode,但 DeckForge 的核心價值是反詰對話 — 不論你提供多少資料,真正要說服的判斷通常是在對話中才浮現的。怎麼處理？

  ○ 維持完整反詰 (Recommended)
       → 我繼續用 2-3 輪跳窗,把簡報真正要講的重點挖出來。
         即使你已給我大量資料,對話仍可能挖出你還沒講的東西。
  ○ 切到 Quick mode
       → 我只問 1 題(最關鍵的那一題),然後用顯式假設往下走。
         前幾頁如果偏掉再回頭修。
```

**Only switch to Quick mode if the user explicitly picks it.** Do not infer it from tone, document length, or message brevity.

### What Quick mode does (after user opts in)

1. Ask **one** pop-up question — about the single highest-leverage gap (usually scenario or core thesis).
2. After the answer, write a brief.md filled with **explicit assumptions** for every field you didn't ask about.
3. Tell the user: "I'm proceeding with these assumptions — interrupt if any are wrong, especially the first three."
4. Continue to Phase 2 (still subject to the Phase 1 → Phase 2 handoff approval; Quick mode does not skip the handoff pop-up either).

Quick mode reduces interview length, but **never** skips Phase 1 entirely, never skips brief.md, and never skips the handoff approval. The file checkpoint discipline is unconditional.

### When abundant data does NOT justify skipping the dialogue

A common temptation: "the user gave me a full whitepaper / a complete brief / detailed answers — Phase 1 dialogue would be redundant." Resist it. The data tells you *what's in the user's head*; the dialogue is the only way to surface:

- What judgment the audience must change (rarely in any source doc)
- Which storyline among the data is the *primary* one (the doc usually contains multiple)
- The single objection the audience will raise (only the user knows their room)
- What action the audience should take after the deck (almost never in source material)

If you find yourself thinking "I have everything I need to skip the dialogue", that's a strong signal you should run **at least one** Socratic round to test the assumption. Often the user will reveal a constraint or audience reaction that completely reshapes the deck.

---

## Stop conditions — "clear enough", not "perfect"

Stop the Socratic loop and produce `brief.md` when, **at the most recent Between-round reflection (see "The loop" → Round 2+ → Step 1)**, all 7 of these are ✅ AND reflection-question B (new-ambiguity-surfaced) was "none":

```text
✅ Audience is named, plus what they currently believe / what room they're in
✅ Desired belief shift is articulated (from X → to Y)
✅ Core thesis fits in one sentence
✅ 2–4 candidate proof pillars supporting the thesis are named (MECE-verified
   in the exit branch, not here — reflection only checks that pillars exist)
✅ The most likely objection is identified
✅ Desired audience action after the deck is named
✅ Page count, tone, language, brand constraints are at least sketched
```

If a condition is ⚠️ partial in reflection, treat it as ❌ for stop purposes — partial means there's a clarification worth one more round.

**Why MECE isn't a stop condition**: MECE is a verification that runs in the **exit branch** (see "The loop" → Round 2+ → Step 1 → Exit branch). Listing it as a stop condition would create a circular dependency — reflection can't tick it ✅ without running the check, but won't run the check unless reflection is all ✅.

### MECE check on proof_pillars — **required before writing brief.md**

`proof_pillars` is the second layer of the deck's pyramid (apex = `core_thesis`, layer 2 = `proof_pillars`, leaves = card content in Phase 3). For the pyramid to hold, the pillars must be **MECE**:

- **Mutually Exclusive**: no pillar partially restates another. If "team is experienced" + "founders have 30 years in the industry" — that's not two pillars, it's one.
- **Collectively Exhaustive**: pillars together should be a complete defence of the thesis. If a smart objection can be raised that none of the pillars addresses, the set is incomplete.

Before writing `brief.md`, run this check silently. Concrete failure modes to look for:

| Failure mode | Example | Fix |
|---|---|---|
| Cause-effect mixed in | "Speed + Reliability + Great team" — team causes the first two | Drop "team" or move it under one of the first two |
| Different abstraction levels | "Market is large + Our SDK supports REST" — one is strategy, one is a feature | Lift the feature to its strategic claim, or drop |
| Partial overlap | "Lower cost + Higher ROI" — overlap on price-value axis | Merge into one pillar, or split into truly distinct dimensions |
| Missing dimension | Pitch deck with pillars only about product, none about market/team | Add the missing dimension |

**If the silent check finds an overlap or gap that you can't resolve confidently**, run one more Socratic round before writing brief.md — **unless you are already on round 4**. If you are on round 4, do NOT ask a 5th round; log the overlap in `open_assumptions` and enter Forced Assumption mode (see below). The 4-round cap is hard.

For rounds 1–3, the MECE-revision round uses this pop-up:

```
Question: 我整理出 N 個 proof pillars,但 <pillar A> 跟 <pillar B> 看起來有重疊
(<具體解釋哪邊重疊>)。怎麼處理?

  ○ 合併成一個 (Recommended)
       → 我把這兩個合併成 <合併後敘述>,讓 pillars 維持 MECE
  ○ 保留兩個,但把界線講清楚
       → 你說明二者的真正分工,我用你的講法重寫
  ○ 拿掉一個
       → 哪一個比較不重要,我就拿掉
```

If the resulting `proof_pillars` after revision still has obvious overlap, log it in `open_assumptions` and continue (Phase 2 outline architect will surface MECE violations again). Better to ship a slightly-overlapping pillar set than to loop forever.

You do **not** need all assumptions resolved. Anything still open goes into `open_assumptions` in the brief, so Phase 2/3 can either inherit them or surface them later. Don't loop forever chasing certainty — perfect is the enemy of shippable.

You **also** stop (forcibly) after 4 rounds. If 4 rounds of Socratic questions still didn't produce clarity, switch to **Forced Assumption mode** — this is a **distinct** mechanism from user-chosen Quick mode (do not call it Quick mode):

- **Forced Assumption mode** = the agent ran 4 rounds and couldn't get clarity, so it documents every remaining unknown and proceeds with explicit caveats.
- **Quick mode** = the user explicitly chose to skip the dialogue (still requires opt-in pop-up, see below).

In Forced Assumption mode:
1. List every still-unresolved field as a numbered assumption in `brief.md → open_assumptions[]`.
2. For each of the four non-negotiable fields (`audience.current_belief`, `belief_shift`, `core_thesis`, `desired_action`) that remained unclear, write your best-guess value with a `⚠️` prefix.
3. Write `brief.md`.
4. At the Phase 1→2 handoff pop-up, **flag the unclear fields prominently** so the user can revise before any outline work:

```
Question: ⚠️ 4 輪反詰後有以下欄位我用了 best-guess (不是你親口給的):
  - <field 1>: <my guess>
  - <field 2>: <my guess>
我可以繼續做大綱,但如果這些猜錯,後面整份 deck 會偏。怎麼處理?

  ○ 繼續進入 Phase 2 (我的 best-guess 可接受) (Recommended)
  ○ 我要先修正其中一個 best-guess
       → 你告訴我哪個欄位,給我正確的值
  ○ 再回到反詰多問一輪
       → 我們再多繞一輪
```

Forced Assumption mode is a safety valve when the dialogue genuinely can't converge. It is **not** an excuse to short-circuit the Socratic loop on rounds 1-3. You only reach it by genuinely running 4 rounds.

---

## Output — write `brief.md` (this file is a hard checkpoint)

Before exiting Phase 1, write `brief.md` to the working directory. **Phase 2 must Read `brief.md` before it starts.** Do not skip writing it, even in Quick mode.

```markdown
# Brief

## Scenario
<one of: fundraising / sales / internal-sync / executive-briefing / educational / strategy-review / annual-review / product-launch / keynote / training / other>

## Audience
- **Who**: <name the role, level, and decision power>
- **Current belief**: <what they think today about this topic>

## Belief shift
- **From**: <what they think now>
- **To**: <what we want them to think after the deck>

## Core thesis
<single sentence the audience should be able to repeat back after the deck>

## Proof pillars
1. <pillar 1 — what evidence will carry this>
2. <pillar 2>
3. <pillar 3>
(2–4 pillars; more than 4 means the deck is unfocused)

## Likely objections
- <the one most likely to derail the room>
- <secondary objection, optional>

## Desired action
<the specific next step the audience should take — book a call, approve budget, sign off, etc.>

## Constraints
- **Page count**: <approx, or a range>
- **Tone**: <serious / playful / data-heavy / story-driven / hybrid>
- **Language**: <zh-TW / en / bilingual / other>
- **Brand**: <colors, fonts, taboo items, must-mention items>
- **Visual style hint**: <dark_apple / clean minimal / bold corporate / tech-futuristic / warm humanistic / academic>

## Open assumptions
- <things we did not confirm but are proceeding with — Phase 2/3 may revisit>

## Source material
<paths or URLs the user supplied; or "none">
```

Once `brief.md` exists, **do not silently start Phase 2**. Ask the user via `AskUserQuestion` whether to continue:

```
Question: Phase 1 完成（已產出 brief.md）。要繼續進入 Phase 2 大綱規劃嗎？

  ○ 繼續進入 Phase 2 (Recommended)
       → 我會 Read brief.md 然後產出 outline.json (每頁標題＝一個 mini-claim)
  ○ 我要先修改 brief.md
       → 告訴我哪邊要改 (thesis / pillars / objection / 任何欄位)
  ○ 暫停在這裡
       → brief.md 已存到 working directory，之後可以再回來繼續
```

Only continue to Phase 2 — and Phase 2's first action must be to `Read brief.md` — after the user approves. The same approval discipline applies at every later phase boundary; see SKILL.md "Every phase handoff requires explicit user approval".

---

## Five worked examples

### Example 1 — vague topic

**User**: "幫我做一份 AI 產品簡報。"

**Bad** (don't do this):
> Sure! How many pages do you want? What language? What tone?

**Good** — pop-up Socratic question targeting scenario:

```
Question: "AI 產品簡報" 三種方向會做成完全不同的簡報，你比較接近哪一種？

  ○ 說服客戶採購 (Recommended)
       → 重心放在客戶痛點 + ROI + 風險降低，最後一頁是 CTA
  ○ 說服投資人成長性
       → 重心放在市場規模 + 競爭護城河 + traction 數字
  ○ 內部團隊對齊產品方向
       → 重心放在現狀 + 待決策事項 + 時程
```

### Example 2 — user dumps lots of data

**User**: pastes product intro + market sizing + features + 3 customer logos.

**Good** — Socratic question targeting the storyline:

```
Question: 資料裡有三條可能主線，這次最想讓觀眾相信的是哪一條？

  ○ 市場正在變大，現在是進入時機
       → 把市場數字推到開頭，產品變支撐角色
  ○ 我們產品比競品完整 (Recommended)
       → 把功能/性能比較放正中央
  ○ 客戶案例證明導入有效
       → 把 traction / case study 變主軸
```

### Example 3 — contradictory constraints

**User**: "5 頁以內，但要包含技術架構、商業模式、競品分析、財務預測、市場規模。"

**Good** — Socratic question forcing the tradeoff:

```
Question: 5 頁要塞完整商業計畫做不到，得先選一個目標。最重要的是？

  ○ 快速說服當場決策 (Recommended)
       → 留下：問題 / 解法 / 數字 / 風險 / CTA。其他進附錄
  ○ 展現完整度，讓對方相信你有思考過
       → 用 mini_grid 把 5 個主題壓進每頁，每個只給一個關鍵點
  ○ 讓對方願意排一場深入會議
       → 留下：問題嚴重性 / 我們的角度 / 下次會議要看的東西
```

### Example 4 — abstract "advantages"

**User**: "幫我介紹我們的優勢。"

**Good** — Socratic question reframing "advantage" into "audience-side decision risk":

```
Question: 觀眾真正在意的「優勢」通常不是你最自豪的功能，而是能降低他們決策風險的理由。這次最能改變對方判斷的是？

  ○ 更便宜
       → 把價格 vs ROI 推到第一頁
  ○ 導入更快、上線風險更低 (Recommended)
       → 把實施時程 + 客戶案例證明放正中央
  ○ 更可靠 / SLA 更高
       → 把可用性數字 + 重大客戶背書放主軸
  ○ 整合既有系統更容易
       → 把架構圖 + 整合案例放主軸
```

### Example 5 — user uploaded a document

**User**: attaches a 40-page whitepaper.

**Good** — Phase 0 ran first; now Phase 1 uses Phase 0 output:

```
Question (round 1): Phase 0 從文件抽出三條可能主線。這份簡報的核心觀眾是？

  ○ CFO / 財務主管
       → 簡報主軸會是「成本降低」
  ○ 營運主管 / 業務負責人
       → 簡報主軸會是「效率提升」
  ○ 技術主管 / IT 主管 (Recommended)
       → 簡報主軸會是「風險控管 + 整合複雜度」
```

After they answer, round 2 questions are scenario-specific to that audience type. **Phase 1 still ran — Phase 0 did not bypass it.**

---

## Tone reminders

- Consultant, never interrogator. "There's a trade-off here…" beats "Your goals are inconsistent."
- Lead with "What I currently understand is…" before asking what's unclear. The user should feel you're already half-way to a deck, not starting from zero.
- Inferences must be labeled as inferences. Unconfirmed assumptions go to `open_assumptions`, not into the core thesis.
- Do not exceed 3 questions per round. Do not exceed 4 rounds total.
- Do not ask "Do you want it to look professional?" or anything you can reasonably infer.
- Match the user's language. If they wrote in 繁中, your questions are in 繁中.

---

## Why this loop is non-skippable

Even when the user gave you:
- a complete document → Phase 0 extracts material, Phase 1 picks the storyline
- a long brief → it still doesn't say what *judgment must change* in the audience
- "just do it" instructions → Quick mode runs one round and proceeds with stated assumptions

In every case `brief.md` must exist before Phase 2 starts. This is enforced by SKILL.md's file-checkpoint rule.
