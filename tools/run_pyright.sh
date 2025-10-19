#!/usr/bin/env bash
set -euo pipefail

# Helper: install pyright in the current venv and run it.
# Usage: source .venv/bin/activate && bash tools/run_pyright.sh

if ! command -v pyright >/dev/null 2>&1; then
  echo "pyright not found; attempting to install via pip in the active venv"
  python -m pip install -U pyright
fi

pyright
