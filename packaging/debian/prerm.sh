#!/usr/bin/env bash
set -euo pipefail

# Pre-removal script for the nideflanders package (shell wrapper)
if command -v systemctl >/dev/null 2>&1; then
  if systemctl is-active --quiet nideflanders.service; then
    systemctl stop nideflanders.service || true
  fi
  if systemctl is-enabled --quiet nideflanders.service; then
    systemctl disable nideflanders.service || true
  fi
fi

exit 0
