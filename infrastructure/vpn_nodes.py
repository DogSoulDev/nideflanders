"""
Gestor de nodos VPN open source: obtiene y gestiona la lista de nodos disponibles por país.
"""
import requests


class VPNNodeManager:
    def __init__(self):
        self.nodes = []
        self.tor_bridges = []

    def fetch_openvpn_nodes(self):
        """Obtiene nodos OpenVPN públicos desde varias fuentes open source automáticas."""
        self.nodes = []
        # Fuente 1: vpngate.net
        try:
            url = "https://www.vpngate.net/api/iphone/"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                self.nodes += self.parse_vpngate_response(response.text)
        except requests.RequestException as e:
            print(f"Error obteniendo nodos VPNGate: {e}")

        # Fuente 2: FreeVPN.me (OpenVPN)
        try:
            url = "https://www.freevpn.me/accounts/"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                self.nodes += self.parse_freevpnme_response(response.text)
        except requests.RequestException as e:
            print(f"Error obteniendo nodos FreeVPN.me: {e}")

        # Fuente 3: Lista pública de GitHub (ejemplo)
        try:
            url = "https://raw.githubusercontent.com/freedomofopenvpn/openvpn-list/main/openvpn.csv"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                self.nodes += self.parse_csv_response(response.text)
        except requests.RequestException as e:
            print(f"Error obteniendo nodos GitHub: {e}")

        # Fuente 4: Bridges de TOR (automático)
        self.tor_bridges = self.fetch_tor_bridges()

        return bool(self.nodes)

    def parse_vpngate_response(self, text):
        nodes = []
        for line in text.splitlines():
            if line.startswith('*') or line.startswith('Title'):
                continue
            parts = line.split(',')
            if len(parts) > 6:
                node = {
                    'ip': parts[1],
                    'country': parts[6],
                    'score': parts[2],
                    'ping': parts[3],
                    'speed': parts[4],
                    'type': parts[5],
                }
                nodes.append(node)
        return nodes

    def parse_freevpnme_response(self, text):
        # Busca IPs y países en el HTML
        import re
        nodes = []
        matches = re.findall(r'<strong>Server IP:</strong> ([\d\.]+).*?<strong>Country:</strong> ([A-Za-z ]+)', text, re.DOTALL)
        for ip, country in matches:
            nodes.append({'ip': ip, 'country': country, 'score': '', 'ping': '', 'speed': '', 'type': 'OpenVPN'})
        return nodes

    def parse_csv_response(self, text):
        nodes = []
        for line in text.splitlines():
            parts = line.split(',')
            if len(parts) >= 2:
                nodes.append({'ip': parts[0], 'country': parts[1], 'score': '', 'ping': '', 'speed': '', 'type': 'OpenVPN'})
        return nodes

    def fetch_tor_bridges(self):
        """Obtiene bridges de TOR automáticamente desde bridges.torproject.org."""
        bridges = []
        try:
            url = "https://bridges.torproject.org/bridges?transport=obfs4"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Extrae bridges obfs4 del HTML
                import re
                bridges += re.findall(r'obfs4 [^\s]+ [^\s]+ [^\s]+ [^\s]+', response.text)
        except requests.RequestException as e:
            print(f"Error obteniendo bridges TOR: {e}")
        return bridges

    def get_nodes_by_country(self, country):
        return [n for n in self.nodes if n['country'].lower() == country.lower()]

    def get_tor_bridges(self):
        return self.tor_bridges
