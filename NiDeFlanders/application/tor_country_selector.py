"""
Selector de país/IP usando la red TOR y nodos VPN open source.
Permite enrutar el tráfico por el país elegido, combinando TOR y nodos VPN.
"""
from infrastructure.vpn_nodes import VPNNodeManager
from infrastructure.tor_manager import TorManager

class TorCountrySelector:
    def __init__(self, tor_password=None):
        self.vpn_nodes = VPNNodeManager()
        self.tor = TorManager(password=tor_password)
        self.selected_country = None

    def update_nodes(self):
        """Actualiza la lista de nodos VPN open source."""
        return self.vpn_nodes.fetch_openvpn_nodes()

    def select_country(self, country):
        """Selecciona un país y obtiene nodos disponibles."""
        self.selected_country = country
        nodes = self.vpn_nodes.get_nodes_by_country(country)
        return nodes

    def change_tor_ip(self):
        """Solicita nuevo circuito/IP a Tor."""
        return self.tor.change_ip()

    def get_current_country(self):
        return self.selected_country