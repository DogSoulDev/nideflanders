
# NiDeFlanders — Guía rápida (modo usuario y Kali)
===============================================

Este documento muestra los pasos más sencillos para dejar NiDeFlanders funcionando en Kali Linux.

## Modos de uso
- **Userland Tor (sin sudo):** Arranca Tor como proceso del usuario, sin instalar paquetes del sistema.
- **Modo --auto (recomendado para usuarios que aceptan un único sudo):** Instala Tor/Privoxy y crea una unidad systemd.

### 1) Preparar entorno Python (aplicable a ambos modos)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2) Userland Tor (sin sudo)

Inicia Tor descargando el Tor Browser Bundle si no existe y arrancándolo como proceso del usuario.

```bash
# Iniciar Tor en modo usuario
python tools/bootstrap_user_tor.py
# Exportar proxy SOCKS para que otras herramientas usen Tor
export TOR_SOCKS5='socks5://127.0.0.1:9050'
# Ejecutar prueba de fugas
python tools/leak_test.py

# Para detener el Tor iniciado por este bootstrapper
python tools/bootstrap_user_tor.py --stop
```

**Notas:**
- Puedes fijar la URL de descarga y la suma SHA256 mediante variables de entorno:
  - `TOR_BOOTSTRAP_URL`: URL completa al tar.xz del Tor Browser Bundle
  - `TOR_BOOTSTRAP_SHA256`: SHA256 del archivo; si se proporciona, el instalador lo verificará antes de extraer
- Los logs y el PID del Tor iniciado se escriben en `$XDG_DATA_HOME/nidef/tor/` (por defecto `~/.local/share/nidef/tor/`)

### 3) Modo --auto (una sola vez pedirá sudo)

```bash
# Instala tor/privoxy y crea un servicio systemd nideflanders
bash tools/install_kali.sh --auto
# Ver estado del servicio
sudo systemctl status nideflanders
```

### 4) Uso del leak-test sin instalar Tor en el sistema

Si prefieres no instalar nada en el sistema, pero tienes un proxy SOCKS5 disponible (por ejemplo Tor iniciado en otra máquina o localhost por el bootstrapper), exporta la variable `TOR_SOCKS5` y ejecuta:

```bash
export TOR_SOCKS5='socks5://127.0.0.1:9050'
python tools/leak_test.py
```

### 5) Consejos y seguridad

- Si el bootstrapper descarga binarios, usa `TOR_BOOTSTRAP_SHA256` para verificar la integridad.
- El modo `--auto` modifica servicios del sistema y requiere sudo; úsalo solo en entornos de confianza (por ejemplo, tu Kali personal o una máquina virtual).

### 6) Problemas comunes

- Si `python3` en tu sistema apunta al instalador de Microsoft Store (Windows), crea un entorno virtual con una instalación real de Python o usa WSL/Kali.
- Para soporte avanzado (AppArmor, hardening, packaging), revisa `tools/apparmor/` y `SECURITY.md`.

---
Guía generada automáticamente por el asistente de desarrollo para NiDeFlanders.
