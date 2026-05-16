#!/usr/bin/env bash
# Push DeckForge to a fresh GitHub repo.
#
# Usage:
#   ./push.sh <github-username> [repo-name] [public|private]
#
# Examples:
#   ./push.sh jeff-tpi                       # → public repo named DeckForge
#   ./push.sh jeff-tpi DeckForge private     # → private repo
#
# Requires either:
#   - gh CLI (https://cli.github.com)  — most automatic
#   - OR git installed + you create the empty repo manually first
#
set -euo pipefail

USERNAME="${1:?usage: $0 <github-username> [repo-name] [public|private]}"
REPO_NAME="${2:-DeckForge}"
VISIBILITY="${3:-public}"

cd "$(dirname "$0")"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "Error: $(pwd) is not a git repo. Run this script from the DeckForge/ folder."
  exit 1
fi

if command -v gh >/dev/null 2>&1; then
  echo "→ Using gh CLI to create + push $USERNAME/$REPO_NAME ($VISIBILITY)..."
  gh repo create "$REPO_NAME" \
    "--$VISIBILITY" \
    --source=. \
    --remote=origin \
    --push
  echo ""
  echo "Done. Repo: https://github.com/$USERNAME/$REPO_NAME"
else
  echo "→ gh CLI not found. Falling back to plain git push."
  echo ""
  echo "Step 1: open https://github.com/new and create an empty repo named '$REPO_NAME'"
  echo "        (do NOT initialize with README, LICENSE, or .gitignore)"
  echo ""
  read -r -p "Press Enter once the empty repo exists... "

  REMOTE_URL="https://github.com/$USERNAME/$REPO_NAME.git"
  if git remote get-url origin >/dev/null 2>&1; then
    git remote set-url origin "$REMOTE_URL"
  else
    git remote add origin "$REMOTE_URL"
  fi

  echo "→ Pushing to $REMOTE_URL ..."
  echo "  (when prompted for password, use a GitHub Personal Access Token, not your login password)"
  echo "  (create one at https://github.com/settings/tokens/new with 'repo' scope)"
  git push -u origin main

  echo ""
  echo "Done. Repo: https://github.com/$USERNAME/$REPO_NAME"
fi
