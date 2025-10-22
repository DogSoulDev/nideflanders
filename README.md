
# NiDeFlanders — Inicio rápido

NiDeFlanders es un wrapper minimalista para Tor + Privoxy, pensado para usuarios de Kali Linux.

## Objetivos
- Ejecutarse en modo usuario por defecto (sin requerir sudo).
- Opcionalmente instalarse a nivel sistema usando `--auto` o el instalador.
- GUI muy sencilla: activar/desactivar y cambiar país.

## Instalación rápida (modo usuario, sin sudo)

```bash
git clone https://github.com/DogSoulDev/nideflanders.git
cd nideflanders
bash tools/install.sh   # crea el entorno virtual y las dependencias
source .venv/bin/activate
python run.py           # inicia la GUI (o usa CLI: python run.py activate)
```

> **Nota:** No es necesario dar permisos manualmente con `chmod` a los scripts. Los instaladores gestionan automáticamente los permisos de ejecución en Kali/Debian.

## Instalación completa (Kali, requiere sudo)

```bash
sudo bash tools/install_full.sh
```

## Instalador E2E y prueba automática (Kali)

```bash
sudo bash tools/run_e2e_kali.sh --auto
```

## Notas
- El comportamiento por defecto evita requerir root: si no se encuentra `tor` en el sistema, la aplicación intentará descargar y ejecutar Tor en modo usuario usando `tools/bootstrap_user_tor.py`.
- `tools/run_e2e_kali.sh` guarda los logs y resultados en `artifacts/e2e-<timestamp>/`.
- Para ejecutar pruebas de fuga manualmente en el entorno virtual activado:

```bash
export TOR_SOCKS5=socks5://127.0.0.1:9050
python tools/leak_test.py
```

## Desarrollo

- Crear entorno virtual e instalar dependencias de desarrollo:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements-dev.txt
  ```
- Ejecutar pruebas unitarias:
  ```bash
  pytest -q
  ```
- Ejecutar análisis estático:
  ```bash
  source .venv/bin/activate
  bash tools/run_pyright.sh
  ```

## Empaquetado .deb para Kali/Debian

```bash
sudo apt update && sudo apt install -y fakeroot dpkg-dev
bash tools/build_deb.sh
sudo dpkg -i nideflanders_0.1_all.deb
```

### ¿Qué hace el paquete al instalarse?
- Copia el repositorio a `/opt/nideflanders`.
- Crea un entorno virtual en `/opt/nideflanders/.venv` e instala las dependencias.
- Instala un wrapper en `/usr/local/bin/nideflanders` que activa el entorno y lanza la GUI.
- Si existe, instala y habilita la unidad systemd `packaging/systemd/nideflanders.service`.

---

## Personalización avanzada

### Configuración de nodos y bridges
El archivo `config/nodes.yml` permite definir relays Tor, bridges y proveedores VPN open-source personalizados. Puedes editarlo manualmente o usar el script `tools/fetch_tor_relays.py` para actualizar la lista automáticamente desde fuentes oficiales.

Ejemplo de entrada:
```yaml
tor_relays:
  - nickname: "ejemplo-relay"
    fingerprint: "9695DFC3..."
    ip: "198.51.100.23"
    country: "US"
    flags: ["Guard","Fast","Stable"]
    source: "https://metrics.torproject.org/rs.html"
```

### Icono personalizado
Puedes personalizar el icono de la ventana principal de la GUI colocando una imagen PNG en `assets/nideflanders.png`. Si el archivo existe, se usará automáticamente como icono.

### Integración de assets
La carpeta `assets/` puede usarse para añadir imágenes, logotipos o recursos adicionales para la interfaz gráfica o documentación.

### Scripts útiles
- `tools/fetch_tor_relays.py`: actualiza automáticamente la lista de relays en `config/nodes.yml`.
- `tools/leak_test.py`: ejecuta pruebas de fuga de IP/DNS usando Tor/Privoxy.
- `tools/check_imports.py`: verifica que los módulos principales se pueden importar correctamente.

¿Quieres más ejemplos o integración avanzada? Dímelo y lo añado.
