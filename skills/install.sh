#!/bin/bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="$HOME/.agents/skills"

echo "Installing ddip skills to $TARGET ..."

for skill_dir in "$REPO_DIR/skills"/*/; do
  name=$(basename "$skill_dir")
  [ -f "$skill_dir/SKILL.md" ] || continue
  cp -r "$skill_dir" "$TARGET/"
  echo "  [OK] $name"
done

echo ""
echo "Done. All skills installed."
echo "Try: '有哪些 image', '加 image', 'build image'"
