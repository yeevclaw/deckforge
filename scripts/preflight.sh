#!/usr/bin/env bash
# Pre-release preflight for DeckForge — step 0 of CLAUDE.md → "Release / ship flow".
#
#   always : scripts/check_docs.py   (doc-drift guard, sub-second)
#   when the rendering surface changed (working tree, or since the last tag):
#            scripts/golden_check.sh (regression-render the example decks)
#   nudge  : ≥3 traces newer than the last analysis → suggest /deckforge-improve
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
fail=0

# Self-heal the one-time hook install — the hook is what makes check_docs.py non-optional.
if [ "$(git config core.hooksPath 2>/dev/null || true)" != "scripts/githooks" ]; then
  echo "⚠ pre-commit hook inactive — run once:  git config core.hooksPath scripts/githooks"
fi

echo "── check_docs.py ──"
python3 scripts/check_docs.py || fail=1

# golden_check renders three decks (slow); run it only when the rendering surface
# moved — uncommitted changes OR anything since the last release tag.
last_tag="$(git describe --tags --abbrev=0 2>/dev/null || echo HEAD)"
changed="$( { git diff HEAD --name-only; git diff "$last_tag"..HEAD --name-only 2>/dev/null; } | sort -u)"
if echo "$changed" | grep -qE '^(scripts/svg_to_pptx\.py|templates/|examples/)'; then
  echo "── golden_check.sh (rendering surface changed) ──"
  bash scripts/golden_check.sh || fail=1
else
  echo "── golden_check.sh skipped (rendering surface unchanged) ──"
fi

# Loop-4 nudge: unanalyzed traces piling up?
if [ -d traces ]; then
  last_analysis="$(ls -t traces/_analysis/*.md 2>/dev/null | head -1 || true)"
  if [ -n "$last_analysis" ]; then
    fresh=$(find traces -mindepth 1 -maxdepth 1 -type d ! -name '_*' -newer "$last_analysis" | wc -l | tr -d ' ')
  else
    fresh=$(find traces -mindepth 1 -maxdepth 1 -type d ! -name '_*' | wc -l | tr -d ' ')
  fi
  if [ "$fresh" -ge 3 ]; then
    echo "💡 $fresh trace(s) await analysis — consider running /deckforge-improve before this release."
  fi
fi

if [ "$fail" -ne 0 ]; then
  echo "✗ preflight FAILED"
  exit 1
fi
echo "✓ preflight passed"
