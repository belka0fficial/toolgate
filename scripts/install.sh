#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLI_SOURCE="$REPO_ROOT/cli/toolgate"
TARGET_DIR="${HOME}/.local/bin"
TARGET="$TARGET_DIR/toolgate"

mkdir -p "$TARGET_DIR"

if [[ -e "$TARGET" ]]; then
  rm -f "$TARGET"
fi

ln -s "$CLI_SOURCE" "$TARGET"

if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$HOME/.bashrc"; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi

export PATH="$HOME/.local/bin:$PATH"

echo "ToolGate CLI installed to $TARGET"
echo "Run: toolgate"
echo
echo "If command is not found in a new shell, run:"
echo 'export PATH="$HOME/.local/bin:$PATH"'
