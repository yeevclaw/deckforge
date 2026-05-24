#!/usr/bin/env bash
# Build deckforge.zip for Claude Desktop's Upload a skill flow.
#
# Run from anywhere inside the project; output: ../deckforge.zip
# (one directory above the project root).
#
# Usage:  bash scripts/package.sh
#
# Implementation note: we use `git archive` (not rsync from the working
# tree) so the release zip is byte-equivalent to GitHub's auto-generated
# "Code → Download ZIP" — only tracked files, no .gitignored scratch
# files leaking in. This avoids a class of bugs where macOS NFD-encoded
# filenames (e.g. Chinese-named scratch docs) end up mangled in the zip
# and break extraction on other systems / inside Claude Desktop.

set -e

# Resolve project root (parent of scripts/)
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Must be inside a git working tree — package.sh assumes git is the
# source of truth for what ships.
if ! git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "❌ $ROOT is not inside a git working tree." >&2
  echo "   package.sh ships from git, not the working directory." >&2
  exit 1
fi

# Read the canonical skill name from SKILL.md frontmatter so the zip's
# top-level folder matches what Claude Desktop expects.
SKILL_NAME="$(awk '/^---$/{n++; next} n==1 && /^name:/ {sub(/^name:[[:space:]]*/,""); print; exit}' "$ROOT/SKILL.md")"
if [ -z "$SKILL_NAME" ]; then
  echo "❌ Could not read 'name:' from SKILL.md frontmatter." >&2
  exit 1
fi

OUT="$(dirname "$ROOT")/${SKILL_NAME}.zip"
rm -f "$OUT"

# Warn if there are uncommitted changes — they will NOT be in the zip.
if ! git -C "$ROOT" diff-index --quiet HEAD --; then
  echo "⚠️  Working tree has uncommitted changes. The zip will only contain"
  echo "    committed files. Commit first if you want the changes to ship."
  echo ""
fi

# Build the zip via `git archive`. The --prefix puts everything inside
# a top-level folder matching the skill name.
git -C "$ROOT" archive --format=zip --prefix="${SKILL_NAME}/" -o "$OUT" HEAD

echo "✅ Wrote $OUT"
echo "   wrapper folder inside zip: ${SKILL_NAME}/ (matches SKILL.md name)"
echo "   contents sourced from: git HEAD (same as GitHub auto-zip)"
echo ""
echo "Next: open Claude Desktop → Customize → Skills →"
echo "      + → Create skill → Upload a skill → pick this zip."
