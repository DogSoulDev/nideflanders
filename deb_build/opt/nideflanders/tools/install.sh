#!/usr/bin/env bash
set -euo pipefail

# Simple installer: creates a virtualenv in .venv and installs dev requirements
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

echo "Instalando NiDeFlanders (modo desarrollo)"
AUTO_MODE=0
if [ "${1:-}" = "--auto" ]; then
  AUTO_MODE=1
fi

if [ "$AUTO_MODE" -eq 1 ]; then
  echo "Auto mode: se solicitará sudo una vez para instalar paquetes del sistema (Kali/Debian)."
  sudo apt update
  sudo apt install -y tor privoxy python3-gi gir1.2-gtk-3.0
fi

python3 -m venv "$VENV_DIR"
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
if [ -f requirements-dev.txt ]; then
  pip install -r requirements-dev.txt
else
  echo "requirements-dev.txt no encontrado, instalando dependencias mínimas"
  pip install requests pysocks
fi

# Create a small wrapper script
cat > "$ROOT_DIR/run.py" <<'PY'
#!/usr/bin/env python3
"""Run NiDeFlanders GUI.

Usage: python run.py
"""
import sys
from gi.repository import Gtk  # type: ignore

from interface.main_window import MainWindow

if __name__ == '__main__':
    app = MainWindow()
    app.run()
PY
chmod +x "$ROOT_DIR/run.py"

echo "Instalación completada. Activa el entorno con: source .venv/bin/activate"
echo "Inicia la app con: python run.py"
