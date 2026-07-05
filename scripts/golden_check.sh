#!/usr/bin/env bash
# Golden-deck regression for DeckForge — maintainer / CI tool (export-ignored).
#
# Automates the DETERMINISTIC half of the Phase 4→5 check: the committed sample
# SVGs and the flow-anim demos must render + assemble cleanly through the
# converter, and the demos must stay free of flow-anim lint warnings. This
# guards against converter/template regressions silently breaking the examples.
#
# The VISUAL grade (prompts/06_visual_grader.md scoring the rendered PNGs against
# references/rubric.md "Phase 5 — VISUAL") is an LLM/agent step and is
# deliberately NOT wired in here — running a model inside a shell / CI loop means
# an API bill. After this passes, do the visual grade from Claude.
#
# Scope (be honest about it): this guards RENDERING, not Socratic/planning
# quality. Golden brief/planning inputs live in evals/ — the change-time
# verification loop (.claude/skills/deckforge-verify) runs phase-isolated
# evals against them when a prompt changes; that's an LLM step, not this one.
#
# Usage:  bash scripts/golden_check.sh
set -uo pipefail
cd "$(dirname "$0")/.."   # repo root

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
fail=0

# run_deck  <name>  <pages-dir>  <must_lint_clean: 0|1>
run_deck () {
  local name="$1" dir="$2" lint_clean="$3"
  echo "=== $name ($dir) ==="
  if python3 scripts/svg_to_pptx.py --pages-dir "$dir" \
        --output "$TMP/$name.pptx" --workdir "$TMP/$name" \
        > "$TMP/$name.out" 2> "$TMP/$name.err"; then
    echo "  build: OK"
  else
    echo "  build: FAILED"; sed 's/^/    /' "$TMP/$name.err"; fail=1; return
  fi
  if [ "$lint_clean" = "1" ] \
        && grep -q "flow-anim" "$TMP/$name.err" && grep -q "⚠" "$TMP/$name.err"; then
    echo "  flow-anim lint: WARNINGS (a demo must stay clean)"
    grep "flow-anim" "$TMP/$name.err" | sed 's/^/    /'
    fail=1
  fi
}

run_deck sample-deck           examples/sample-deck           0
run_deck flow-anim-demo        examples/flow-anim-demo        1
run_deck flow-anim-demo-fresh  examples/flow-anim-demo-fresh  1

echo
if [ "$fail" -ne 0 ]; then
  echo "❌ Golden check FAILED."
  exit 1
fi
echo "✅ Golden check passed — all sample decks build."
echo "   Visual grade (optional agent step): render a deck's _renders/*.png and run"
echo "   prompts/06_visual_grader.md against references/rubric.md (Phase 5 — VISUAL)."
exit 0
