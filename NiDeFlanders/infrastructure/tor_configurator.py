
"""
Configura el archivo torrc para aplicar bridges y opciones de privacidad automáticamente.
"""


class TorConfigurator:
    def __init__(self, torrc_path="/etc/tor/torrc"):
        self.torrc_path = torrc_path

    def apply_bridge(self, bridge_line):
        """Agrega un bridge al archivo torrc si no existe."""
        try:
            with open(self.torrc_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            if bridge_line + "\n" not in lines:
                with open(self.torrc_path, "a", encoding="utf-8") as f:
                    f.write(f"\nBridge {bridge_line}\n")
            return True
        except (OSError, IOError) as e:
            print(f"Error aplicando bridge a torrc: {e}")
            return False

    def set_privacy_options(self):
        """Configura opciones de privacidad recomendadas en torrc."""
        privacy_lines = [
            "AvoidDiskWrites 1",
            "DisableNetwork 0",
            "Log notice stdout",
            "SafeLogging 1",
            "CookieAuthentication 1",

            """
            "ClientUseIPv6 0",
