# DeckForge Improvement Loop (hill climbing)

DeckForge's harness — `SKILL.md`, `prompts/`, `references/`, `templates/`,
`scripts/svg_to_pptx.py` — gets better the way LangChain's "loop engineering"
describes the outer loop: real runs leave traces, the traces reveal recurring
failure modes, and those feed edits back **into** the harness. This file makes that
a repeatable procedure instead of an ad-hoc habit.

This is a **maintainer** process (export-ignored; it never ships in the skill zip).
It is run by a human + an analysis sub-agent on a manual cadence — no trace database,
no LLM in CI. The mechanical half is automated (a pre-commit hook runs
`scripts/check_docs.py` on every commit); the judgement half stays human-triggered.

## Traces — the currency (already on disk)

Every run already produces its own trace; you log nothing new. A trace is the run's
working directory:

- `analysis.md` / `brief.md` / `outline.json` / `planning.json` / `pages/*.svg`
- the produced `.pptx` / `.pdf` / `.notes.md`
- `_qa/grade_p3.json` / `_qa/grade_p5.json` — the persisted verdicts from the two fresh-eyes graders, Phase 3 content (`prompts/07_content_grader.md`) and Phase 5 visual (`prompts/06_visual_grader.md`) — what failed + the fix
- **where the user chose "我要先修改"** at a phase handoff — the cheapest signal that
  the harness produced something the user had to correct

The handoff-revision points and the grader failures are the highest-value signal:
they mark exactly where the harness under-delivered.

## Retention (thin)

When a run is worth learning from, run `bash scripts/collect_trace.sh <working-dir>
<short-name>` — it copies the dir into `traces/<short-name>/` (gitignored — local
corpus, one folder per run) and stamps a `meta.md`: date, DeckForge version, and
blanks for the one signal that lives only in the conversation — the handoff points
where the user chose 「我要先修改」. No schema, no DB. Keep the ones that surprised
you; drop the rest.

## Analysis pass (periodic)

On a cadence you choose — after a few collected traces, or when `scripts/preflight.sh`
nudges you at release time — run the **`/deckforge-improve`** dev skill
(`.claude/skills/deckforge-improve/`; needs a repo-root session). It reads the
retained traces, clusters recurring failure modes, folds in `scripts/check_docs.py`
findings (the mechanical half — the clustering is the judgement half), and emits a
ranked proposal file to `traces/_analysis/`, each proposal carrying: which file, what
change, the evidence trace, the expected effect — the shape of the hand-written
`DeckForge_改善建議與理由.md`, formalized rather than reinvented. The step-by-step
procedure lives in the skill file only (single statement, no drift pair); this file
keeps the why.

## Ship gate (human, always)

The analysis sub-agent **proposes**; it never edits prompts. A human reviews the
ranked list, approves what's worth doing, and the edits land via the normal release
flow (`CLAUDE.md` → "Release / ship flow", tagged `vX.Y.Z`). The return arrow reaches
into the inner loops — proposals change `prompts/`, `references/rubric.md`,
`templates/`, or the grader — but a person always pulls the trigger.

## Why this exists

Today the harness improves reactively: someone notices a problem, edits a prompt, tags
a release; several past releases exist solely to fix doc drift. This loop turns that
reactive habit into a standing discipline, and makes "find drift and weak spots across
the whole corpus" a repeatable target instead of a thing you happen to remember.
