#!/usr/bin/env bash
# Build deckforge.zip for Claude Desktop's Upload a skill flow.
#
# Run from anywhere inside the project; output: ../deckforge.zip
# (one directory above the project root).
#
# Usage:  bash scripts/package.sh

set -e

# Resolve project root (parent of scripts/)
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Read the canonical skill name from SKILL.md frontmatter so the zip's
# top-level folder matches what Claude Desktop expects.
SKILL_NAME="$(awk '/^---$/{n++; next} n==1 && /^name:/ {sub(/^name:[[:space:]]*/,""); print; exit}' "$ROOT/SKILL.md")"
if [ -z "$SKILL_NAME" ]; then
  echo "❌ Could not read 'name:' from SKILL.md frontmatter." >&2
  exit 1
fi

OUT="$(dirname "$ROOT")/${SKILL_NAME}.zip"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

# Stage: copy source into a directory named after the skill (not the repo folder name)
mkdir -p "$STAGE/$SKILL_NAME"
rsync -a \
  --exclude='.git/' \
  --exclude='.DS_Store' \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  --exclude='_renders/' \
  "$ROOT/" "$STAGE/$SKILL_NAME/"

# Build the zip
rm -f "$OUT"
(cd "$STAGE" && zip -rq "$OUT" "$SKILL_NAME")

echo "✅ Wrote $OUT"
echo "   wrapper folder inside zip: ${SKILL_NAME}/ (matches SKILL.md name)"
echo ""
echo "Next: open Claude Desktop → Customize → Skills →"
echo "      + → Create skill → Upload a skill → pick this zip."
