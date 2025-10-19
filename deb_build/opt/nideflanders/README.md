````markdown
 # NiDeFlanders — Quick Start

NiDeFlanders - a minimal Tor + Privoxy wrapper intended for Kali users.

Goals:
- Run in userland by default (no sudo required).
- Optionally install system-wide using `--auto`/system installer.
- Very small GUI: activate/deactivate + change country.

Quick start (user mode, no sudo):

```bash
git clone https://github.com/DogSoulDev/nideflanders.git
cd nideflanders
bash tools/install.sh   # crea .venv e instala dependencias
source .venv/bin/activate
python run.py           # arranca GUI (o usa CLI: python run.py activate)
```

One-line E2E installer & test (Kali - requires sudo to apt install):

```bash
# As normal user, but allow the script to sudo when needed
sudo bash tools/run_e2e_kali.sh --auto
```

Notes:
- Default behavior tries to avoid requiring root: if no system `tor` is found, the app will attempt
  to start a userland Tor bundle via `tools/bootstrap_user_tor.py`.
- `tools/run_e2e_kali.sh` collects artifacts under `artifacts/e2e-<timestamp>/` (app logs and leak-test logs).
- To run leak-tests manually in the activated venv:

```bash
export TOR_SOCKS5=socks5://127.0.0.1:9050
python tools/leak_test.py
```

Development:
- Create a venv and install dev requirements: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements-dev.txt`
- Run unit tests: `pytest -q`
 - Run static checks (pyright):
   ```bash
   source .venv/bin/activate
   bash tools/run_pyright.sh
   ```

Licencia: GPL v3

One-liner (full, system-wide install on Kali as root):

```bash
sudo bash tools/install_full.sh
```

One-liner (user-level, no sudo):

```bash
bash tools/install.sh && source .venv/bin/activate && python run.py
```

Building a .deb for Kali (on a Debian/Kali host):

```bash
# Ensure you have fakeroot and dpkg-deb installed
sudo apt update && sudo apt install -y fakeroot dpkg-dev
bash tools/build_deb.sh
# Install the generated package
sudo dpkg -i nideflanders_0.1_all.deb
```

What the package does on installation:
- Copies the repository to `/opt/nideflanders`.
- Creates a Python venv in `/opt/nideflanders/.venv` and installs `requirements-dev.txt` (if present) during postinst.
- Installs a wrapper at `/usr/local/bin/nideflanders` that activates the venv and launches the GUI.
- If present, installs the systemd unit `packaging/systemd/nideflanders.service` and enables it.


````
 # NiDeFlanders — Quick Start

 Objetivo: que el usuario solo tenga que clonar, instalar y ejecutar.

 Requisitos mínimos (Kali recomendado):
 - Python 3.10+ (python3)
 - Opcional: tor y privoxy si quieres integración del sistema; por defecto el proyecto usa userland Tor.

 Pasos rápidos (3 comandos):

 ```bash
 git clone https://github.com/DogSoulDev/nideflanders.git
 cd nideflanders
 bash tools/install.sh   # crea .venv e instala dependencias
 source .venv/bin/activate
 python run.py           # arranca GUI (o usa CLI: python run.py activate)
 ```

 Cómo funciona (explicación corta):
 - Si `tor` no está instalado, la aplicación intenta arrancar Tor en modo userland (descarga/extrae y ejecuta localmente).
 - Privoxy se configura para enrutar HTTP(S) a través de Tor.
 - GUI mínima: botón "Activar VPN" / "Desactivar VPN" y opción para cambiar país.

 Si quieres que implemente integración avanzada (systemd, package, o instalador para Kali), dime y la añadimos.

 Licencia: GPL v3

One-liner (full, system-wide install on Kali as root):

```bash
sudo bash tools/install_full.sh
```

One-liner (user-level, no sudo):

```bash
bash tools/install.sh && source .venv/bin/activate && python run.py
```
