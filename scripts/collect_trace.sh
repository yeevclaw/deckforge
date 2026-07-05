#!/usr/bin/env bash
# Collect a deck-building session's working dir into the Loop-4 trace corpus.
#
# Usage (from the repo root):
#   bash scripts/collect_trace.sh <working-dir> <short-name>
#
# Copies <working-dir> to traces/<short-name>/ (gitignored, one folder per run)
# and writes a meta.md stub: date, DeckForge version, and blanks for the signals
# that live only in the conversation — handoff-revision points and why the run
# was worth keeping. The corpus feeds the analysis pass: see
# references/improvement_loop.md and the /deckforge-improve dev skill.
#
# A complete trace (what a working dir contains after a full run):
#   analysis.md / brief.md / outline.json / planning.json / pages/*.svg
#   the produced .pptx / .pdf / .notes.md
#   _qa/grade_p3.json + _qa/grade_p5.json — grader verdicts, saved by SKILL.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [ $# -ne 2 ]; then
  echo "usage: bash scripts/collect_trace.sh <working-dir> <short-name>" >&2
  exit 1
fi

SRC="$1"
NAME="$2"
DEST="$ROOT/traces/$NAME"

[ -d "$SRC" ] || { echo "error: working dir not found: $SRC" >&2; exit 1; }
[ -e "$DEST" ] && { echo "error: traces/$NAME already exists" >&2; exit 1; }

mkdir -p "$ROOT/traces"
cp -R "$SRC" "$DEST"

# Warn, don't fail: a trace without verdicts is still useful, but _qa/ is the
# highest-value signal (an older run, or a session where the graders were skipped).
[ -d "$DEST/_qa" ] || echo "⚠ no _qa/ in this working dir — grader verdicts missing"

VERSION="$(git -C "$ROOT" describe --tags 2>/dev/null || echo unknown)"

cat > "$DEST/meta.md" <<EOF
# Trace: $NAME

- collected: $(date +%Y-%m-%d)
- deckforge_version: $VERSION   <!-- version at collection time; correct by hand if the deck was built earlier -->
- topic: <!-- one line: what deck was this -->

## Handoff-revision points (fill by hand — this signal lives only in the conversation)

<!-- Where did the user choose「我要先修改」at a phase handoff? What did they change? -->

## Why kept

<!-- What surprised you about this run — grader failure, user correction, layout miss? -->
EOF

echo "✓ trace collected → traces/$NAME/ — now fill in meta.md"
