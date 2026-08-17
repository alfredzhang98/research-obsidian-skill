#!/usr/bin/env bash
# Thin wrapper around install/installer.py (the canonical installer).
#
# Usage:
#   ./install/install.sh [VAULT_PATH] [AI_WIKI_NAME] [PAPER_SEARCH_DIR]
#
# Defaults (when arguments are omitted):
#   VAULT_PATH        : the parent of this repository
#   AI_WIKI_NAME      : 0ai_wiki
#   PAPER_SEARCH_DIR  : ~/paper-search-mcp

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$(command -v python3 || command -v python || true)"

if [ -z "$PYTHON" ]; then
  echo "error: python3 not found; install Python 3 then rerun" >&2
  exit 1
fi

exec "$PYTHON" "$REPO_DIR/install/installer.py" "$@"
