---
name: deckforge-improve
description: Run DeckForge's Loop-4 analysis pass — read the traces/ corpus, cluster recurring failure modes across runs, fold in check_docs.py drift findings, and emit a ranked harness-edit proposal file to traces/_analysis/. Proposes only; never edits the harness. Maintainer tool for improving DeckForge itself — use when asked to run the improvement loop, analyze traces, or propose harness edits. Requires a repo-root session.
---

# DeckForge improvement analysis pass (Loop 4)

You are the analysis half of DeckForge's hill-climbing loop. `references/improvement_loop.md` holds the why; this file is the how. You read retained run traces and propose harness edits — **you never apply them**; the ship gate is human.

## Hard rules

1. **Propose, don't edit.** In this pass, do not modify `SKILL.md`, `prompts/`, `references/`, `templates/`, or `scripts/`. Your only write target is `traces/_analysis/`.
2. **Don't reopen settled theses.** Traces contain user-approved briefs; "the thesis is wrong" is never a finding (the same red line the content grader has).
3. **Evidence or it didn't happen.** Every proposal cites the trace(s) and verdicts it comes from.

## Procedure

1. **Inventory.** List `traces/*/`, ignoring any `_*/` directory (the `_analysis/` output, `_smoke-*` fixtures). If the corpus is empty, stop and say so — it is filled by `bash scripts/collect_trace.sh <working-dir> <short-name>` after worthwhile deck sessions; there is nothing to analyze yet.
2. **Read each trace**: `meta.md` (topic, `deckforge_version` stamp, hand-filled handoff-revision points, why-kept), `_qa/grade_p3.json` and `_qa/grade_p5.json` (grader verdicts — what failed, where, the fix), and `planning.json` (layouts, `card_variant`/`flow_variant`, motion). Open a page's SVG or the `brief.md` only when a verdict or note points at it.
3. **Cluster failure modes across traces**: group by `rubric_id` × phase × layout/template/variant. One-off misses are noise; recurrences are signal. Use the `deckforge_version` stamps to note whether a mode improved or regressed across releases — the corpus doubles as the longitudinal record.
4. **Fold in the mechanical half**: run `python3 scripts/check_docs.py` and include anything it flags. The clustering above is the judgement half — also watch for rules that are *consistent everywhere but wrong*, the drift class the checker cannot see.
5. **Write the proposal file** to `traces/_analysis/YYYY-MM-DD-proposals.md` (today's date; create the dir if absent). Ranked, highest-leverage first. Each proposal states:
   - **priority** — P1 / P2 / P3
   - **file** — the harness file to edit
   - **change** — the concrete edit
   - **evidence** — the trace(s), grader verdicts, or handoff notes showing the problem
   - **expected effect** — what should stop happening
6. **Stop.** Present the ranked list to the maintainer. Approved edits land through the normal release flow (`CLAUDE.md` → "Release / ship flow"), guarded by the pre-commit hook and `scripts/preflight.sh`.
