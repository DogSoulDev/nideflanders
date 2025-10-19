NiDeFlanders — Quick start (userland Tor / easy Kali)
===============================================

Este documento muestra los pasos más sencillos para dejar NiDeFlanders funcionando en Kali.

Resumen de modos
- Userland Tor (sin sudo): arranca Tor como proceso del usuario, sin instalar paquetes del sistema.
- Modo --auto (recomendado para un usuario que acepta un único sudo): instala Tor/Privoxy y crea una unidad systemd.

1) Preparar entorno Python (aplicable a ambos modos)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2) Userland Tor (sin sudo)

- Inicia Tor descargando el Tor Browser bundle si no existe y arrancándolo como proceso del usuario.

```bash
# iniciar Tor en userland
python tools/bootstrap_user_tor.py
# exportar proxy SOCKS para que otras herramientas usen Tor
export TOR_SOCKS5='socks5://127.0.0.1:9050'
# correr leak-test
python tools/leak_test.py

# para detener el tor arrancado por este bootstrapper
python tools/bootstrap_user_tor.py --stop
```

Notas:
- Puedes fijar la URL de descarga y la suma SHA256 mediante variables de entorno:
  - `TOR_BOOTSTRAP_URL` : URL completa al tar.xz del Tor Browser bundle
  - `TOR_BOOTSTRAP_SHA256` : sha256 del archivo; si se proporciona, el instalador lo verificará antes de extraer
- Logs y PID del Tor arrancado se escriben en `$XDG_DATA_HOME/nidef/tor/` (por defecto `~/.local/share/nidef/tor/`)

3) Modo --auto (una sola vez pedirá sudo)

```bash
# instala tor/privoxy y crea un servicio systemd nideflanders
bash tools/install_kali.sh --auto
# ver estado del servicio
sudo systemctl status nideflanders
```

4) Uso del leak-test sin instalar Tor en el sistema

- Si prefieres no instalar nada en el sistema, pero tienes un proxy SOCKS5 disponible (por ejemplo Tor arrancado en otra máquina o localhost por el bootstrapper), exporta la variable `TOR_SOCKS5` y ejecuta:

```bash
export TOR_SOCKS5='socks5://127.0.0.1:9050'
python tools/leak_test.py
```

5) Consejos y seguridad

- Si el bootstrapper descarga binarios, usa `TOR_BOOTSTRAP_SHA256` para verificar integridad.
- El modo `--auto` modifica servicios del sistema y requiere sudo; úsalo sólo en entornos de confianza (por ejemplo tu Kali personal o una VM).

6) Problemas comunes
- Si `python3` en tu sistema apunta al instalador de Microsoft Store (Windows), crea un venv con una instalación de Python real o usa WSL/Kali.
- Para soporte avanzado (AppArmor, hardening, packaging), revisa `tools/apparmor/` y `SECURITY.md`.

---
Documentación generada automáticamente por el asistente de desarrollo para NiDeFlanders.
