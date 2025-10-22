#!/usr/bin/env python3
"""Entry point for NiDeFlanders: launches GUI if available, else provides CLI."""
from __future__ import annotations
import sys
import logging
from typing import List

logger = logging.getLogger('nideflanders.cli')
logger.addHandler(logging.NullHandler())


# Comprobación de dependencias para la GUI
try:
    import gi  # type: ignore
    try:
        from gi import require_version  # type: ignore
        require_version('Gtk', '3.0')
    except Exception:
        pass  # Si falla, continuar sin interrumpir
    from gi.repository import Gtk  # type: ignore
    from interface.main_window import main as gui_main  # type: ignore
    GUI_OK = True
except (ImportError, ModuleNotFoundError):
    print("[NiDeFlanders] Dependencia faltante: PyGObject (gi) o GTK. Instala 'python3-gi' y 'gir1.2-gtk-3.0' usando apt en Debian/Kali.")
    GUI_OK = False

from application.vpn_service import VPNService


def cli_main(argv: List[str]) -> int:
    svc = VPNService()
    if len(argv) < 2:
        logger.info('Uso: run.py [activate|deactivate|status|change-country <CC>]')
        return 0
    cmd = argv[1]
    if cmd == 'activate':
        ok = svc.activate()
        logger.info('Activado' if ok else 'Error')
        return 0 if ok else 2
    if cmd == 'deactivate':
        ok = svc.deactivate()
        logger.info('Desactivado' if ok else 'Error')
        return 0 if ok else 2
    if cmd == 'status':
        print('Activo' if svc.is_active() else 'Inactivo')
        return 0
    if cmd == 'change-country' and len(argv) >= 3:
        ok = svc.change_country(argv[2])
        logger.info('Cambio OK' if ok else 'Error')
        return 0 if ok else 2
    logger.warning('Comando desconocido')
    return 1


if __name__ == '__main__':
    if GUI_OK:
        gui_main()
    else:
        sys.exit(cli_main(sys.argv))
