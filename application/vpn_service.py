"""
Servicio principal de la VPN: orquesta la activación/desactivación, cambio de país/IP y protección de privacidad.
Cumple arquitectura hexagonal y clean code.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from infrastructure.tor_manager import TorManager
from infrastructure.privoxy_manager import PrivoxyManager

class VPNService:
    def __init__(self, tor_password=None):
        self.tor = TorManager(password=tor_password)
        self.privoxy = PrivoxyManager()
        self.active = False

    def activate_vpn(self):
        """Activa la VPN: inicia Tor y Privoxy, enruta tráfico."""
        if self.tor.test_connection():
            if self.privoxy.start_privoxy():
                self.active = True
                return True
        return False

    def deactivate_vpn(self):
        """Desactiva la VPN: detiene Privoxy."""
        if self.privoxy.stop_privoxy():
            self.active = False
            return True
        return False

    def change_country_ip(self):
        """Solicita nuevo circuito/IP a Tor."""
        return self.tor.change_ip()

    def is_active(self):
        return self.active
