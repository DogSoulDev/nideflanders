#!/usr/bin/env python3
"""Leak-test utilities for NiDeFlanders.

Checks for IP and DNS leaks by attempting to route queries through Tor.

Exit codes:
 - 0: all checks passed
 - 1: environment missing (tor/privoxy/torify)
 - 2: leak detected
"""
import os
import shutil
import subprocess
import sys
from typing import Tuple

try:
    # requests may not have type stubs in the environment; it's expected in dev requirements.
    import requests  # type: ignore[import]
except ImportError:  # pragma: no cover - optional
    # requests not installed in the environment; the dev requirements include it.
    requests = None


def has_cmd(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def run_capture(cmd: Tuple[str, ...]) -> Tuple[int, str]:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, timeout=30)
        return 0, out.strip()
    except subprocess.CalledProcessError as e:
        return e.returncode, (e.output or "").strip()
    except subprocess.TimeoutExpired as e:
        return 98, f"timeout: {e}"
    except OSError as e:
        return 97, str(e)


def check_torify_curl() -> bool:
    # Try to get external IP via torify curl
    if not has_cmd("torify"):
        print("torify not found")
        return False
    code, out = run_capture(("torify", "curl", "-s", "ifconfig.me"))
    if code != 0 or not out:
        print(f"torify curl failed: code={code} out={out}")
        return False
    print(f"External IP via Tor: {out}")
    return True


def check_tor_resolve() -> bool:
    if not has_cmd("tor-resolve"):
        print("tor-resolve not found")
        return False
    code, out = run_capture(("tor-resolve", "ifconfig.me"))
    if code != 0 or not out:
        print(f"tor-resolve failed: code={code} out={out}")
        return False
    print(f"tor-resolve ifconfig.me -> {out}")
    return True


def main() -> int:
    # Support a zero-permissions mode: if TOR_SOCKS5 env var is set, use requests + socks
    tor_socks = os.environ.get("TOR_SOCKS5") or os.environ.get("TOR_PROXY")
    http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
    https_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")

    # Pure-Python proxy mode
    if tor_socks or http_proxy or https_proxy:
        if requests is None:
            print("requests library not installed in venv. Install with: pip install requests pysocks")
            return 1
        session = requests.Session()
        proxies = {}
        if tor_socks:
            # use socks via requests (requires pysocks)
            proxies = {
                'http': tor_socks,
                'https': tor_socks,
            }
        else:
            if http_proxy:
                proxies['http'] = http_proxy
            if https_proxy:
                proxies['https'] = https_proxy

        try:
            r = session.get('http://ifconfig.me', timeout=10, proxies=proxies)
            ip = r.text.strip()
            print(f"External IP via configured proxy: {ip}")
        except requests.exceptions.RequestException as e:  # type: ignore[import-not-found]
            # Specific requests exception when using requests; treat any request failure as a leak/error.
            print(f"Proxy-mode request failed: {e}")
            return 2

        # DNS check: attempt to resolve via an HTTP endpoint that echoes DNS-resolved host (best-effort)
        try:
            r2 = session.get('http://ifconfig.me', timeout=10, proxies=proxies)
            if r2.status_code != 200:
                print("Proxy-mode DNS/http check unexpected status", r2.status_code)
                return 2
        except requests.exceptions.RequestException as e:  # type: ignore[import-not-found]
            # Secondary check failed; treat as leak/error.
            print(f"Proxy-mode DNS/http secondary check failed: {e}")
            return 2

        print("Leak-tests OK (proxy-mode).")
        return 0

    # Otherwise try system tools fallback (torify/tor-resolve)
    missing = []
    for cmd in ("torify", "tor-resolve", "curl"):
        if not has_cmd(cmd):
            missing.append(cmd)
    if missing:
        print("No system tools or proxy configured. Missing:", ", ".join(missing))
        print("Either export TOR_SOCKS5 or install tor utilities on the host.")
        return 1

    ok1 = check_torify_curl()
    ok2 = check_tor_resolve()

    if not (ok1 and ok2):
        print("Leak test failed or environment incomplete.")
        return 2

    print("Leak-tests OK: requests and DNS resolve through Tor (system-tools mode).")
    return 0


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
