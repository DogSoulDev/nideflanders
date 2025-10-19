import importlib
import sys
from typing import Any

modules = [
    'application.vpn_service',
    'infrastructure.tor_controller',
    'infrastructure.privoxy_controller',
    'interface.main_window',
]

failed: list[tuple[str, Any]] = []
for m in modules:
    try:
        importlib.import_module(m)
        print(f'OK: {m}')
    except ImportError as e:
        print(f'ERR IMPORT: {m} -> {e}')
        failed.append((m, e))
    except (AttributeError, SyntaxError, RuntimeError, SystemError) as e:  # pragma: no cover - diagnostic
        # Narrow the catch to common import-time failures while allowing
        # BaseException subclasses like KeyboardInterrupt/SystemExit to propagate.
        print(f'ERR RUN: {m} -> {e}')
        failed.append((m, e))

if failed:
    sys.exit(1)
else:
    sys.exit(0)
