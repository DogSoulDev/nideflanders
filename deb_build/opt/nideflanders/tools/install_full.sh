#!/usr/bin/env bash
set -euo pipefail

# Full installer for Kali: installs system packages, copies files, creates a simple launcher
# Usage: sudo bash tools/install_full.sh

if [ $(id -u) -ne 0 ]; then
  echo "This script must be run as root: sudo bash tools/install_full.sh"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

apt update
apt install -y python3-venv python3-pip python3-gi tor privoxy

# create system user to run service (optional)
#install -d -m 0755 /opt/nideflanders
rm -rf /opt/nideflanders
cp -r "$ROOT_DIR" /opt/nideflanders

# create virtualenv
python3 -m venv /opt/nideflanders/.venv
source /opt/nideflanders/.venv/bin/activate
pip install --upgrade pip
pip install -r /opt/nideflanders/requirements-dev.txt || true

# create wrapper executable
cat > /usr/local/bin/nideflanders <<'PY'
#!/usr/bin/env bash
source /opt/nideflanders/.venv/bin/activate
python /opt/nideflanders/run.py
PY
chmod +x /usr/local/bin/nideflanders

# install systemd unit
cp "$ROOT_DIR/packaging/systemd/nideflanders.service" /etc/systemd/system/nideflanders.service
systemctl daemon-reload
systemctl enable --now nideflanders.service || true

echo "Installed NiDeFlanders system-wide. Service enabled (may have failed to start)."
