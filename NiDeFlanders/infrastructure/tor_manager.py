"""
Módulo para gestionar la conexión y control de Tor desde Python usando stem.
Cumple arquitectura hexagonal y clean code.
"""
from stem import Signal
from stem.control import Controller

class TorManager:
    def __init__(self, port=9051, password=None):
        self.port = int(port)
        self.password = password

    def change_ip(self):
        """Solicita un nuevo circuito/IP a Tor."""
        try:
            with Controller.from_port(port=self.port) as controller:
                if self.password:
                    controller.authenticate(password=self.password)
                else:
                    controller.authenticate()
                # Signal.NEWNYM es correcto en stem
                controller.signal(Signal.NEWNYM)
            return True
        except ImportError as e:
            print(f"Error importando stem: {e}")
            return False
        except OSError as e:
            print(f"Error de sistema: {e}")
            return False
        except Exception as e:
            print(f"Error cambiando IP de Tor: {e}")
            return False

    def test_connection(self):
        """Verifica si Tor está corriendo y el puerto de control responde."""
        try:
            with Controller.from_port(port=self.port) as controller:
                if self.password:
                    controller.authenticate(password=self.password)
                else:
                    controller.authenticate()
                return True
        except ImportError as e:
            print(f"Error importando stem: {e}")
            return False
        except OSError as e:
            print(f"Error de sistema: {e}")
            return False
        except Exception as e:
            print(f"Error de conexión con Tor: {e}")
            return False
