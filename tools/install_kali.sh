#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

echo "Modo zero-permissions: no se ejecutarán apt/sudo ni se instalarán servicios del sistema."
echo "Si necesitas instalar Tor/Privoxy a nivel sistema, ejecuta el instalador con privilegios en una máquina Kali separada."

echo "Creando virtualenv $VENV_DIR si no existe y activando..."
if [[ ! -d "$VENV_DIR" ]]; then
  python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
echo "Instalando dependencias Python en .venv (requests, PySocks si está disponible)..."
python -m pip install --upgrade pip
python -m pip install requests pysocks || python -m pip install requests || true

echo "Nota: este instalador no intentará configurar Tor/Privoxy en el sistema a menos que uses --auto."
echo "Si quieres que el programa use Tor sin instalar nada a nivel sistema, puedes ejecutar:
  - un proxy SOCKS5 local y exportar TOR_SOCKS5=socks5://127.0.0.1:9050
  - o exportar HTTP_PROXY/HTTPS_PROXY apuntando a un proxy que encamine tráfico por Tor"

echo "Asegurando permisos para scripts en tools/"
if [ -d "tools" ]; then
  chmod +x tools/*.sh tools/*.py || true
fi

echo "Si existe un hidden service, ajustando permisos..."
## Si quieres ajustar permisos de hidden_service realiza esto manualmente con sudo
## sudo chown -R debian-tor:debian-tor /var/lib/tor/hidden_service
## sudo chmod 700 /var/lib/tor/hidden_service
## sudo chmod 600 /var/lib/tor/hidden_service/*

echo "Instalación/comprobación finalizada. Recuerda activar el virtualenv antes de usar las herramientas:"
echo "  source $VENV_DIR/bin/activate"

# Optional: create an unprivileged user to run the service
if [[ "${1:-}" == "--create-user" ]]; then
  SERVICE_USER="nidef"
  if id -u "$SERVICE_USER" >/dev/null 2>&1; then
    echo "Usuario $SERVICE_USER ya existe. Skipping creation."
  else
    echo "Creando usuario no-root: $SERVICE_USER"
    sudo useradd --system --no-create-home --shell /usr/sbin/nologin "$SERVICE_USER" || true
    echo "Usuario $SERVICE_USER creado (system)."
  fi
  echo "Recuerda ajustar el owner de los recursos (por ejemplo: sudo chown -R $SERVICE_USER:$SERVICE_USER $ROOT_DIR)"
fi

# Minimal hardening template files
HARDEN_DIR="$ROOT_DIR/tools/apparmor"
mkdir -p "$HARDEN_DIR"
cat > "$HARDEN_DIR/nidef.service.apparmor" <<'EOF'
# Minimal AppArmor profile for NiDeFlanders service
# Place this at /etc/apparmor.d/usr.bin.nidef and adjust paths as needed
profile usr.bin.nidef flags=(attach_disconnected) {
  # allow read-only access to code
  /usr/bin/python3 r,
  "$ROOT_DIR"/** r,
  # allow runtime write only to /var/lib/nidef
  /var/lib/nidef/** rw,
  # network access for tor/proxy
  network,
  capability net_bind_service,
}
EOF

echo "Plantillas de hardening creadas en $HARDEN_DIR"

echo "Si quieres crear un usuario no-root y aplicar el perfil AppArmor, ejecuta:"
echo "  sudo bash $0 --create-user"

# --auto mode: perform system installation (one sudo prompt) to make the project easy to use on Kali
if [[ "${1:-}" == "--auto" ]]; then
  echo "Entrando en modo --auto: se pedirá sudo una sola vez para instalar Tor/Privoxy y configurar el sistema."
  sudo apt update
  sudo apt install -y tor privoxy python3-gi python3-pip

  echo "Instalando paquetes Python en .venv..."
  source "$VENV_DIR/bin/activate"
  python -m pip install --upgrade pip
  python -m pip install -r "$ROOT_DIR/requirements.txt" || python -m pip install requests pysocks || true

  echo "Creando usuario de servicio y asignando permisos..."
  SERVICE_USER="nidef"
  if ! id -u "$SERVICE_USER" >/dev/null 2>&1; then
    sudo useradd --system --no-create-home --shell /usr/sbin/nologin "$SERVICE_USER" || true
  fi
  sudo mkdir -p /var/lib/nidef
  sudo chown -R $SERVICE_USER:$SERVICE_USER /var/lib/nidef || true

  echo "Configurando Tor (ControlPort + CookieAuthentication)"
  sudo bash -c 'grep -q "ControlPort 9051" /etc/tor/torrc || echo "ControlPort 9051" >> /etc/tor/torrc'
  sudo bash -c 'grep -q "CookieAuthentication 1" /etc/tor/torrc || echo "CookieAuthentication 1" >> /etc/tor/torrc'
  sudo systemctl restart tor

  echo "Instalando unidad systemd para NiDeFlanders"
  UNIT_PATH="/etc/systemd/system/nideflanders.service"
  sudo bash -c "cat > $UNIT_PATH" <<EOF
[Unit]
Description=NiDeFlanders service
After=network.target tor.service

[Service]
Type=simple
User=nidef
Group=nidef
WorkingDirectory=$ROOT_DIR
ExecStart=$ROOT_DIR/.venv/bin/python -m interface.main_window
Restart=on-failure
ProtectSystem=full
PrivateTmp=yes
NoNewPrivileges=yes

[Install]
WantedBy=multi-user.target
EOF

  sudo systemctl daemon-reload
  sudo systemctl enable --now nideflanders.service || true

  echo "Modo --auto finalizado. El servicio se intentó habilitar (ver: sudo systemctl status nideflanders)."
fi

# Start userland tor from venv
if [[ "${1:-}" == "--bootstrap-tor" ]]; then
  echo "Arrancando Tor en userland desde .venv..."
  source "$VENV_DIR/bin/activate"
  python "$ROOT_DIR/tools/bootstrap_user_tor.py"
fi

if [[ "${1:-}" == "--bootstrap-tor-stop" ]]; then
  echo "Deteniendo Tor arrancado por bootstrap (si existe pidfile)..."
  source "$VENV_DIR/bin/activate"
  python "$ROOT_DIR/tools/bootstrap_user_tor.py" --stop
fi

