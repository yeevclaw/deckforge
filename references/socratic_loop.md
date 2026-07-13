# Socratic Clarification Loop — reference

A reference companion to `prompts/01_needs_research.md`. This file explains *why* the loop is structured the way it is and gives a deeper taxonomy of question types and deck scenarios. Read this when you (the Phase 1 agent) want to go beyond the recipe.

---

## 1. The triage-then-ask discipline

The loop is **read first, ask second**. Every round:

1. Read everything the user has supplied (their message, attached doc, any prior round answers).
2. Internally answer the 7 triage questions in the Phase 1 prompt.
3. Identify the **single highest-leverage gap** — the unknown that, if wrong, would change the deck structure the most.
4. Pick the right *question type* for that gap (table below).
5. Ask 1–3 pop-up questions via `AskUserQuestion`.
6. Update understanding, re-triage.

Why this matters: a question that is correctly chosen and well-framed can collapse 3 future rounds into one. A questionnaire-style round, by contrast, often produces shallow answers that don't move the deck forward.

---

## 2. The six question types

| Type | Purpose | When to use | Bad failure mode if skipped |
|---|---|---|---|
| **Definition** | Pin down a vague term | Multiple interpretations possible | Deck pivots half-way because the term was different |
| **Consequence** | Surface the audience's desired action | The "what then?" is unclear | Deck ends without a CTA |
| **Evidence** | Demand proof for a claim | A bold claim has no number behind it | Slide is opinionated but unconvincing |
| **Objection** | Pre-empt the room's pushback | Audience pushback is foreseeable | Q&A destroys the deck |
| **Tradeoff** | Force a priority when goals conflict | Stated constraints can't co-exist | Deck becomes a kitchen sink, no spine |
| **Compression** | Cut to the spine | Deck has too many storylines | Slides are busy and unfocused |

**Rule**: one type per round. Don't ask a Definition question plus a Tradeoff question in the same round — the user will answer the easier one and you've wasted leverage on the harder gap.

**Evidence questions and missing data**: when an Evidence question hits "I don't have that number at hand", don't stall and don't invent — offer collaboration: a targeted single-fact web lookup (when a search tool is available, value + source played back for confirmation) or a `needs-research` tag that Phase 2.5 picks up first. See `prompts/01_needs_research.md` → "When the user doesn't have the evidence".

---

## 3. The eleven deck scenarios — and the spine each requires

The Phase 1 agent must detect the scenario early. The detection itself can be a pop-up question if it's not obvious from input. Each scenario has a different **default spine** — the order and emphasis that the deck must reflect. If Phase 1 doesn't lock the scenario, Phase 2 will pick the wrong spine.

| Scenario | Audience reality | Default spine | Surface in Phase 1 | Delivery-mode lean |
|---|---|---|---|---|
| **Fundraising / pitch** | Investors comparing 10+ decks/week | Problem → Solution → Why-now → Traction → Moat → Team → Ask → Use of funds | Stage, round size, traction stat, moat | presenting — but investors read cold before any meeting; probe whether a send-ahead copy is the deck's primary life |
| **Sales / proposal** | Buyer comparing 3 vendors | Pain → Cost of pain → Our approach → Proof → Pricing → Next step | Buyer's role, decision criterion, deal stage | presenting — but proposals get left behind / forwarded to the economic buyer who wasn't in the room; probe |
| **Internal sync** | Colleagues with limited time | Status → What's blocking → What we need decided → Timeline | Decisions needed, blockers, owners | presenting (live meeting artifact) |
| **Executive briefing** | One exec, one screen, low patience | Verdict → 2–3 options → Recommendation → Risks → Resource ask | The one decision being asked | **reading** — usually a pre-read consumed alone; confirm always |
| **Educational** | Students or new hires | Prerequisite → Concept → Example → Practice → Recap | Learner level, learning outcome, time budget | presenting (a teacher voices it) |
| **Strategy review** | Leadership team | Status quo → Problem → Options → Criteria → Recommendation → Tradeoffs | Forcing function (why review now), criteria | presenting (leadership meeting) |
| **Annual / quarterly review** | Internal or shareholders | Highlights → vs Prior → vs Plan → Anomalies → Outlook → Asks | Period, what's surprising, forward asks | presenting (all-hands / live review) |
| **Product launch** | External (media, customers) | Before/After → Hero feature → Demo → Availability → CTA | Launch date, hero feature, target customer | presenting (staged event) |
| **Keynote / conference talk** | Audience with phones in hand | One big idea → Story arc → Examples → Memorable line | The single big idea, the memorable line | presenting — hard; the anti-slidedoc scenario, reading mode is almost never right here |
| **Training / onboarding** | New employees | Roles → Steps → Checkpoints → Where to get help | Role being onboarded, knowledge they have | **reading** — self-serve reference consumed without a presenter |
| **Crisis comms** | Internal or external during incident | What happened → Impact → What we're doing → Timeline → Contact | Audience (internal vs external), facts known | **reading** — distributed under time pressure, no presenter available |

The **Delivery-mode lean** column is the single source of truth Phase 1's "Delivery mode — infer a default, confirm once" section (in `prompts/01_needs_research.md`) reads its defaults from. A lean is a starting inference, not a verdict — it caps at ⚠️ `[inferred]` until the user confirms it in a pop-up round.

If the user's deck doesn't match any row exactly, **don't force a fit** — propose the two closest as a pop-up question and let them pick (or pick "Other" for free-text).

---

## 4. The brief.md contract

`brief.md` is the artifact that survives Phase 1. It is **a hard checkpoint**: Phase 2 must `Read brief.md` as its first action. SKILL.md enforces this rule.

The fields in `brief.md` are not interchangeable with the old "audience / goal / length / tone" form. They map to *judgment-shifting*, not topic-collection:

- `audience.current_belief` → what the room believes today (before the deck)
- `belief_shift.from → to` → the change the deck must produce
- `core_thesis` → the one sentence the audience should be able to repeat back
- `proof_pillars` → the 2–4 sub-claims that support the thesis
- `likely_objections` → what the room will push back on
- `desired_action` → what the audience does *after* the deck
- `open_assumptions` → things we proceeded with but didn't confirm

If any of `audience.current_belief`, `belief_shift`, `core_thesis`, `desired_action` is empty when you're about to write the file — **loop one more round**. Those four are non-negotiable. They must also be **user-confirmed, not merely inferred**: a value you derived from the user's input caps at ⚠️ until you play it back (as a pop-up option, not a dry re-ask) and they confirm it. See the prompt's Between-round reflection contract.

The remaining fields (constraints, source material) can be sketched.

---

## 5. Tone — consultant, not interrogator

The Socratic method *can* feel like cross-examination. That makes users defensive and they give worse answers. Counter it with three habits:

1. **Lead with what you understand.** "I currently understand X. I'm not yet sure about Y." Shows progress, invites correction.
2. **Frame gaps as trade-offs, not contradictions.** "There's a trade-off here between A and B" — not "Your goals conflict."
3. **Surface options the user can pick from.** Pop-up choices are inherently less confrontational than open-ended questions. A user picking option B isn't admitting a mistake — they're making a decision.

If a user pushes back on a question ("just make the deck already"), **do not auto-switch**. Ask via `AskUserQuestion` whether they want Quick mode (one pop-up question max, then proceed with documented assumptions) or the full Socratic loop. Only switch if they explicitly pick Quick mode. Auto-switching bypasses the Socratic dialogue that IS DeckForge's value.

---

## 6. Stop conditions

**Single source of truth**: stop conditions live in [`prompts/01_needs_research.md` → "Stop conditions"](../prompts/01_needs_research.md). This reference doc deliberately does **not** duplicate them — duplication has drifted in the past (this file used to list 7 fields; the prompt now lists 7 stop conditions with different framing, plus a Between-round reflection contract that gates exit). When in doubt about whether the loop can stop, consult the prompt, not this reference.

Hard floor at the other end: the exit branch is closed at Round 2's reflection — the earliest legal exit is after the user has answered 2 rounds, and user-chosen Quick mode is the only single-question path. Forced stop after **4 rounds**. If 4 rounds didn't produce clarity, switch to **Forced Assumption mode** (a **distinct** mechanism from user-chosen Quick mode — do not conflate). Document your best-guess assumptions in `open_assumptions`, prefix the four non-negotiable fields (`audience.current_belief`, `belief_shift`, `core_thesis`, `desired_action`) with `⚠️` if they remained unclear, and flag the unclear fields prominently at the Phase 1→2 handoff so the user can revise before any outline work. See `prompts/01_needs_research.md` → "Forced Assumption mode" for the full procedure.

---

## 7. Why this loop must run even on "I have all the data"

A common user mistake: "I gave you the full document, just make the deck." When this happens, gently explain:

> "The document tells me *what's in your head*. It doesn't tell me *what should change in the audience's head* after the deck. That second part is what determines structure. Let me ask one or two questions to pin it down, then I'll move fast."

If they still push back after this framing, **ask via `AskUserQuestion`** whether they want Quick mode (one pop-up question, then proceed with explicit assumptions) or the full Socratic loop. Only switch to Quick mode if they explicitly pick it. The `brief.md` file is required in either mode — it documents the assumptions for later inspection.

---

## 8. Cross-references

- `prompts/01_needs_research.md` — the recipe Phase 1 follows
- `prompts/00_source_analysis.md` — feeds Phase 1 when a source document exists
- `prompts/02_outline_architect.md` — consumes `brief.md` as its first read
- `references/pyramid_principle.md` — explains why `core_thesis` + `proof_pillars` mirrors pyramid structure
