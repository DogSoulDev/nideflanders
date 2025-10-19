#!/bin/bash
set -euo pipefail

# Small runner to activate project in .venv and start GUI (if available)
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
fi

python3 -m interface.main_window
