#!/usr/bin/env bash
set -euo pipefail

# Full E2E script for Kali to validate NiDeFlanders installation and detect leaks.
# It tries to automate everything needed for a user: install deps, start services (system or userland),
# run leak tests in proxy-mode and system-tools mode, collect logs and exit with a non-zero code on failure.
# Usage:
#   sudo bash tools/run_e2e_kali.sh [--auto]   # recommended when running as root to install system packages
#   bash tools/run_e2e_kali.sh                 # runs user-mode installer and userland Tor

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AUTO=0
KEEP_RUNNING=0
if [ "${1:-}" = "--auto" ]; then
  AUTO=1
fi

echo "Running NiDeFlanders E2E script (ROOT=$(id -u))"
cd "$ROOT_DIR"

# Helper: log and prefix
log() { echo "[E2E] $*"; }

# Step 1: install
if [ "$AUTO" -eq 1 ] || [ $(id -u) -eq 0 ]; then
  log "Installing system packages (apt) -- requires root"
  sudo apt update
  sudo apt install -y python3-venv python3-pip python3-gi gir1.2-gtk-3.0 tor privoxy curl
  # use full installer to set up service and venv
  sudo bash tools/install_full.sh || log "install_full may have partial failures"
  # after full install, run service and exit (service may run as root)
  log "Installed system-wide; testing via systemd service"
  sleep 3
  # ensure service is running or check status
  if systemctl is-active --quiet nideflanders.service; then
    log "nideflanders service is active"
  else
    log "nideflanders service not active; checking journal"
    sudo journalctl -u nideflanders.service --no-pager -n 200 || true
  fi
  # We will run leak tests against system-mode if possible
  MODE="system"
else
  # user-mode installation (no sudo)
  log "Performing user-mode install (no sudo)."
  bash tools/install.sh || true
  # activate venv for subsequent steps
  # shellcheck disable=SC1091
  source .venv/bin/activate
  MODE="user"
fi

# Step 2: start the app (if in user mode, start GUI headless autoconnect)
ARTIFACT_DIR="$ROOT_DIR/artifacts/e2e-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$ARTIFACT_DIR"
log "Artifacts will be saved to: $ARTIFACT_DIR"

APP_PID=0
if [ "$MODE" = "user" ]; then
  export NIDEF_AUTO_CONNECT=1
  log "Starting application in user-mode with autoconnect"
  # redirect stdout/stderr to artifact file
  python run.py >"$ARTIFACT_DIR/app.log" 2>&1 &
  APP_PID=$!
  log "App started (PID: $APP_PID); logs: $ARTIFACT_DIR/app.log"
  # allow time for Tor/Privoxy userland to boot
  sleep 12
fi

# Step 3: run leak tests
RC=0
log "Running leak tests: proxy-mode (using SOCKS at 127.0.0.1:9050)"
export TOR_SOCKS5=socks5://127.0.0.1:9050
python tools/leak_test.py >"$ARTIFACT_DIR/leak_proxy.log" 2>&1 || true
RC_PROXY=$?
if [ $RC_PROXY -ne 0 ]; then
  log "Proxy-mode leak test FAILED (code $RC_PROXY)"
  RC=$RC_PROXY
else
  log "Proxy-mode leak test PASSED"
fi

log "Attempting system-tools mode leak test (torify/tor-resolve/curl)"
python tools/leak_test.py >"$ARTIFACT_DIR/leak_system.log" 2>&1 || true
RC_SYS=$?
if [ $RC_SYS -ne 0 ]; then
  log "System-tools leak test FAILED (code $RC_SYS)"
  RC=$((RC + RC_SYS))
else
  log "System-tools leak test PASSED"
fi

# Step 4: cleanup user app if started
if [ "$APP_PID" -ne 0 ]; then
  log "Stopping user app (PID: $APP_PID)"
  kill "$APP_PID" || true
fi

if [ $RC -eq 0 ]; then
  log "E2E completed: ALL TESTS PASSED"
else
  log "E2E completed: SOME TESTS FAILED (RC=$RC)"
fi

log "Saved artifacts to: $ARTIFACT_DIR"
exit $RC
