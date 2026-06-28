# DeckForge Improvement Loop (hill climbing)

DeckForge's harness — `SKILL.md`, `prompts/`, `references/`, `templates/`,
`scripts/svg_to_pptx.py` — gets better the way LangChain's "loop engineering"
describes the outer loop: real runs leave traces, the traces reveal recurring
failure modes, and those feed edits back **into** the harness. This file makes that
a repeatable procedure instead of an ad-hoc habit.

This is a **maintainer** process (export-ignored; it never ships in the skill zip).
It is run by a human + an analysis sub-agent on a manual cadence — no trace database,
no automation, no LLM in CI.

## Traces — the currency (already on disk)

Every run already produces its own trace; you log nothing new. A trace is the run's
working directory:

- `analysis.md` / `brief.md` / `outline.json` / `planning.json` / `pages/*.svg`
- the produced `.pptx` / `.pdf` / `.notes.md`
- the grader JSON from both fresh-eyes graders — Phase 3 content (`prompts/07_content_grader.md`) and Phase 5 visual (`prompts/06_visual_grader.md`) — what failed + the fix
- **where the user chose "我要先修改"** at a phase handoff — the cheapest signal that
  the harness produced something the user had to correct

The handoff-revision points and the grader failures are the highest-value signal:
they mark exactly where the harness under-delivered.

## Retention (thin)

When a run is worth learning from, copy its working dir into `traces/<short-name>/`
(gitignored — local corpus, one folder per run). No schema, no DB. Keep the ones
that surprised you; drop the rest.

## Analysis pass (periodic)

On a cadence you choose (after N decks, or a `/schedule` cron), spawn an **analysis
sub-agent** over the retained traces:

1. Read the traces + their grader JSONs.
2. Cluster recurring failure modes — e.g. "users keep editing `belief_shift` at the
   Phase 1 handoff → Phase 1 under-asks there"; "the Phase 5 grader keeps flagging
   P5-01 text overflow on `mini_grid` → that template needs more `<tspan>` room".
3. Emit a **ranked list of proposed harness edits**, each with: which file, what
   change, the evidence trace, the expected effect. This is exactly the shape of the
   hand-written `DeckForge_改善建議與理由.md` already in the tree — formalize that
   habit, don't reinvent it.
4. Include doc-drift findings: `scripts/check_docs.py` is the mechanical half (a copy
   that fell out of sync); the analysis pass is the judgement half (a rule that's
   consistent everywhere but wrong).

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
