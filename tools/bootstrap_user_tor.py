#!/usr/bin/env python3
"""Bootstrap Tor in userland (no sudo).

Behavior:
- If `tor` exists in PATH, prints the path and exits 0.
- Else tries to find a tor-browser Linux bundle on dist.torproject.org and download the latest tor-browser-linux64-*.tar.xz.
- Alternatively, respects `TOR_BOOTSTRAP_URL` environment variable to use a specific archive URL.
- Extracts the bundle to `$XDG_DATA_HOME/nidef/tor` (or ~/.local/share/nidef/tor), finds the tor binary, makes it executable and starts it as a subprocess with SocksPort and ControlPort on localhost.

This is intended to be run by the user on a Kali machine to start Tor without installing system packages.
"""

from __future__ import annotations

import os
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
import hashlib
import argparse
import urllib.request
from typing import Optional


DIST_INDEX = 'https://dist.torproject.org/torbrowser/'


def has_tor() -> Optional[str]:
    path = shutil.which('tor')
    return path


def fetch_index(url: str) -> str:
    with urllib.request.urlopen(url, timeout=20) as r:
        return r.read().decode('utf-8', errors='ignore')


def find_latest_torbrowser_link(index_html: str) -> Optional[str]:
    # find tor-browser-linux64-*.tar.xz links
    matches = re.findall(r'href="(tor-browser-linux64-[^\"]+\.tar\.xz)"', index_html)
    if not matches:
        return None
    # choose the lexicographically last (usually latest)
    matches = sorted(matches)
    return DIST_INDEX + matches[-1]


def download_url(url: str, dest: str) -> None:
    print(f'Descargando {url} -> {dest}')
    with urllib.request.urlopen(url, timeout=60) as r, open(dest, 'wb') as out:
        shutil.copyfileobj(r, out)


def download_if_exists(url: str, dest: str) -> bool:
    """Intenta descargar `url` en `dest`. Devuelve True si HTTP 200, False si fallo de red o 404."""
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            if r.status != 200:
                return False
            with open(dest, 'wb') as out:
                shutil.copyfileobj(r, out)
            return True
    except (urllib.error.URLError, OSError, ValueError):
        # Best-effort download: network errors, URL errors or write errors
        # are treated as non-fatal for optional .asc fetches.
        return False


def extract_archive(archive_path: str, dest_dir: str) -> None:
    print(f'Extrayendo {archive_path} -> {dest_dir}')
    with tarfile.open(archive_path, 'r:*') as tf:
        tf.extractall(dest_dir)


def find_tor_binary(extracted_root: str) -> Optional[str]:
    # Tor binary inside tor-browser bundle is usually at <bundle>/Browser/TorBrowser/Tor/tor
    for root, _, files in os.walk(extracted_root):
        if 'tor' in files:
            candidate = os.path.join(root, 'tor')
            # quick check: file exists and is executable or can be made so
            if os.path.isfile(candidate):
                return candidate
    return None


def make_executable(path: str) -> None:
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)


def start_tor(tor_path: str, data_dir: str, socks_port: int = 9050, control_port: int = 9051, log_path: Optional[str] = None, pid_path: Optional[str] = None) -> subprocess.Popen:
    os.makedirs(data_dir, exist_ok=True)
    cmd = [tor_path, '--SocksPort', f'127.0.0.1:{socks_port}', '--ControlPort', f'127.0.0.1:{control_port}', '--DataDirectory', data_dir]
    print('Iniciando Tor:', ' '.join(cmd))
    # redirect logs to a file if provided
    out_handle = subprocess.DEVNULL
    err_handle = subprocess.DEVNULL
    logf = None
    if log_path:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        logf = open(log_path, 'ab')
        out_handle = logf  # type: ignore
        err_handle = logf  # type: ignore

    p = subprocess.Popen(cmd, stdout=out_handle, stderr=err_handle)
    # write pid
    if pid_path:
        with open(pid_path, 'w', encoding='utf-8') as f:
            f.write(str(p.pid))
    # wait a bit for startup
    time.sleep(2)
    if logf:
        logf.close()
    return p


def gpg_available() -> bool:
    return shutil.which('gpg') is not None or shutil.which('gpgv') is not None


def import_tor_browser_key() -> bool:
    """Try to import Tor Browser signing key via WKD with gpg if available."""
    gpg = shutil.which('gpg')
    if not gpg:
        return False
    try:
        # Use WKD to locate the key (best-effort). Use check=True so CalledProcessError is raised on failure
        subprocess.run([gpg, '--auto-key-locate', 'nodefault,wkd', '--locate-keys', 'torbrowser@torproject.org'], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except OSError:
        return False


def verify_with_gpg(asc_path: str, archive_path: str) -> bool:
    """Verify archive with accompanying .asc using system GPG. Returns True if verified."""
    gpg = shutil.which('gpg')
    if not gpg:
        gpg = shutil.which('gpgv')
    if not gpg:
        return False
    try:
        # Ensure key is available (best-effort)
        import_tor_browser_key()
        # Run gpg --verify <asc> <archive>
        res = subprocess.run([gpg, '--verify', asc_path, archive_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        return res.returncode == 0
    except OSError:
        return False


def verify_archive(archive_path: str, asc_url: Optional[str] = None, archive_dir: Optional[str] = None, expected_sha: Optional[str] = None, strict_gpg: bool = False) -> bool:
    """Verify downloaded archive using optional .asc (GPG) or SHA256 fallback.

    Returns True if verification succeeds or no checks were requested.
    Raises OSError on IO problems.
    """
    verified = False
    asc_tmp = None
    try:
        # Try GPG verification if available and asc_url provided (prefer network .asc)
        if gpg_available() and asc_url:
            # only attempt to download asc if asc_url looks like an URL
            if asc_url.startswith('http') and archive_dir:
                fd2, asc_tmp = tempfile.mkstemp(suffix='.asc', dir=archive_dir)
                os.close(fd2)
                if download_if_exists(asc_url, asc_tmp):
                    verified = verify_with_gpg(asc_tmp, archive_path)
            else:
                # asc_url provided but not an http URL: skip network fetch (best-effort)
                pass
        # SHA256 fallback
        if not verified and expected_sha:
            h = hashlib.sha256()
            with open(archive_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    h.update(chunk)
            got = h.hexdigest()
            verified = (got == expected_sha.lower())

        if strict_gpg and not verified:
            return False

        return True if (not strict_gpg and (verified or not expected_sha and asc_tmp is None)) or verified else False
    finally:
        # cleanup asc tmp if created
        if asc_tmp and os.path.exists(asc_tmp):
            try:
                os.remove(asc_tmp)
            except OSError:
                pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--stop', action='store_true', help='Stop a tor process previously started by this script (uses pidfile)')
    parser.add_argument('--strict-gpg', action='store_true', help='Require GPG verification to succeed')
    parser.add_argument('--sha256', dest='sha256', help='Expected SHA256 hex digest for archive')
    parser.add_argument('--asc-url', dest='asc_url', help='Explicit URL for the .asc signature')
    args = parser.parse_args()

    if args.stop:
        xdg = os.environ.get('XDG_DATA_HOME') or os.path.expanduser('~/.local/share')
        pidfile = os.path.join(xdg, 'nidef', 'tor', 'tor.pid')
        if os.path.isfile(pidfile):
            try:
                with open(pidfile, 'r', encoding='utf-8') as f:
                    pid = int(f.read().strip())
                print('Deteniendo tor PID', pid)
                os.kill(pid, 15)
                try:
                    os.remove(pidfile)
                except OSError:
                    pass
                return 0
            except (OSError, ValueError) as e:
                print('Error deteniendo tor:', e)
                return 2
        else:
            print('No se encontró pidfile', pidfile)
            return 1

    # 1) if tor in PATH, done
    tor = has_tor()
    if tor:
        print('tor encontrado en PATH:', tor)
        print('Puedes exportar: export TOR_SOCKS5=socks5://127.0.0.1:9050')
        return 0

    # 2) determine data dir
    xdg = os.environ.get('XDG_DATA_HOME') or os.path.expanduser('~/.local/share')
    base = os.path.join(xdg, 'nidef')
    archive_dir = os.path.join(base, 'archive')
    install_dir = os.path.join(base, 'tor')
    os.makedirs(archive_dir, exist_ok=True)
    os.makedirs(install_dir, exist_ok=True)

    # 3) locate URL
    url = os.environ.get('TOR_BOOTSTRAP_URL')
    if not url:
        try:
            idx = fetch_index(DIST_INDEX)
            url = find_latest_torbrowser_link(idx)
            if url:
                print('Encontrado bundle tor-browser en:', url)
        except (urllib.error.URLError, OSError) as e:
            print('No se pudo consultar dist.torproject.org:', e)
            url = None

    if not url:
        print('No se encontró Tor en PATH ni URL automática. Para descargar automát., exporta TOR_BOOTSTRAP_URL con la URL del tar.xz del Tor Browser bundle.')
        return 1

    # 4) download
    try:
        fd, tmp = tempfile.mkstemp(suffix='.tar.xz', dir=archive_dir)
        os.close(fd)
        download_url(url, tmp)
    except (urllib.error.URLError, OSError) as e:
        print('Error descargando archivo:', e)
        return 2
    # 4.b) verification: respect CLI flags, then env vars
    asc_url = args.asc_url or os.environ.get('TOR_BOOTSTRAP_ASC_URL')
    expected_sha = args.sha256 or os.environ.get('TOR_BOOTSTRAP_SHA256')
    strict_gpg = args.strict_gpg or (os.environ.get('TOR_BOOTSTRAP_STRICT_GPG') == '1')

    # If we have a download URL in env, and no explicit asc_url, derive it as url + '.asc'
    env_url = os.environ.get('TOR_BOOTSTRAP_URL')
    if not asc_url and env_url and env_url.startswith('http'):
        asc_url = env_url + '.asc'

    print('Verificando archive (GPG/SHA options):', {'asc_url': bool(asc_url), 'sha256': bool(expected_sha), 'strict_gpg': strict_gpg})

    try:
        ok = verify_archive(tmp, asc_url=asc_url, archive_dir=archive_dir, expected_sha=expected_sha, strict_gpg=strict_gpg)
    except OSError as e:
        print('Error durante verificación de archive:', e)
        return 8
    if not ok:
        print('Verificación fallida (GPG/SHA)')
        return 7

    # 5) extract
    try:
        extract_archive(tmp, install_dir)
    except (tarfile.TarError, OSError) as e:
        print('Error extrayendo:', e)
        return 3

    # 6) find tor
    tor_bin = find_tor_binary(install_dir)
    if not tor_bin:
        print('No se encontró binario tor dentro del bundle extraído. Revisa:', install_dir)
        return 4

    make_executable(tor_bin)

    # 7) start tor
    data_dir = os.path.join(install_dir, 'data')
    xdg = os.environ.get('XDG_DATA_HOME') or os.path.expanduser('~/.local/share')
    log_path = os.path.join(xdg, 'nidef', 'tor', 'tor.log')
    pid_path = os.path.join(xdg, 'nidef', 'tor', 'tor.pid')
    try:
        p = start_tor(tor_bin, data_dir, log_path=log_path, pid_path=pid_path)
    except OSError as e:
        print('Error al iniciar tor:', e)
        return 6

    print('Tor arrancado (PID {}). Si necesitas detenerlo: python tools/bootstrap_user_tor.py --stop'.format(p.pid))
    print('Logs en:', log_path)
    print('Exporta: export TOR_SOCKS5=socks5://127.0.0.1:9050')
    return 0


if __name__ == '__main__':
    rc = main()
    sys.exit(rc)
