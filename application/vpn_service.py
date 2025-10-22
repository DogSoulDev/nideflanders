"""Servicio principal: orquesta Tor + Privoxy (mínimo y dirigido a Kali Linux)."""
from typing import Optional
import logging

from infrastructure import TorController
from infrastructure.privoxy_controller import PrivoxyController

 # Logger seguro: por defecto no emite logs (NullHandler). Los proyectos que deseen logs
 # pueden configurarlo explícitamente (archivo/handler), pero se recomienda evitar registrar datos sensibles.
logger = logging.getLogger('nideflanders')
logger.addHandler(logging.NullHandler())


class VPNService:
    def __init__(self, tor_control_port: int = 9051, tor_socks_port: int = 9050) -> None:
        self.tor = TorController(control_port=tor_control_port, socks_port=tor_socks_port)
        self.privoxy = PrivoxyController()
        self.active = False
        self.selected_country: Optional[str] = None

    def activate(self) -> bool:
        """Activa el reenvío por Tor y arranca Privoxy. Requiere Tor y Privoxy instalados en Kali."""
        if not self.tor.test_connection():
            logger.debug('tor.test_connection failed, intentando bootstrap userland')
            # intenta arrancar Tor en modo usuario (sin sudo) usando el script proporcionado
            try:
                import subprocess
                import sys
                import os
                import socket
                import time

                repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                bootstrap = os.path.join(repo_root, 'tools', 'bootstrap_user_tor.py')
                if not os.path.isfile(bootstrap):
                    logger.debug('bootstrap script not found: %s', bootstrap)
                    return False
                subprocess.run([sys.executable, bootstrap], check=True)

                # espera a que el puerto socks esté disponible (mejor esfuerzo)
                waited = 0
                timeout = 30
                while waited < timeout:
                    try:
                        with socket.create_connection((self.tor.socks_host, self.tor.socks_port), timeout=3):
                            break
                    except OSError:
                        time.sleep(1)
                        waited += 1

            except (subprocess.CalledProcessError, FileNotFoundError, OSError):
                logger.debug('userland bootstrap failed')
                return False
            # vuelve a comprobar la conexión
            if not self.tor.test_connection():
                logger.debug('tor still not available after bootstrap')
                return False
        if not self.privoxy.ensure_forward(self.tor.socks_host, self.tor.socks_port):
            logger.debug('privoxy.ensure_forward failed')
            return False
        if not self.privoxy.start():
            logger.debug('privoxy.start failed')
            return False
        self.active = True
        return True

    def deactivate(self) -> bool:
        if self.privoxy.stop():
            self.active = False
            return True
        return False

    def change_country(self, country: str) -> bool:
        self.selected_country = country
        return self.tor.change_ip(country)

    def is_active(self) -> bool:
        return self.active
