# type: ignore
"""Controlador mínimo para Tor (usa `stem` si está instalado)."""
import socket
try:
    from stem import Signal  # type: ignore[reportMissingTypeStubs]
    from stem.control import Controller  # type: ignore[reportMissingTypeStubs]
    _STEM = True
except (ImportError, ModuleNotFoundError):
    _STEM = False


class TorController:
    def __init__(self, control_port: int = 9051, socks_port: int = 9050) -> None:
        self.control_port = control_port
        self.socks_port = socks_port
        self.socks_host = '127.0.0.1'

    def test_connection(self) -> bool:
    # Prueba el puerto SOCKS (proxy Tor) para asegurar que Tor está reenviando el tráfico
        try:
            with socket.create_connection((self.socks_host, self.socks_port), timeout=1):
                return True
        except (OSError, ConnectionError):
            return False

    def change_ip(self, country: str | None = None) -> bool:
    """Solicita a Tor construir nuevos circuitos. Opcionalmente fija el país de salida (código ISO 2 letras).

    Requiere Tor con ControlPort habilitado. Usa stem.Controller para autenticar y enviar
    comandos SETCONF / SIGNAL NEWNYM.
    """
        if not _STEM:
            return False
        try:
            # type: ignore[arg-type]
            with Controller.from_port(port=self.control_port) as c:  # type: ignore[arg-type]
                # intenta autenticar usando los métodos disponibles (cookie/contraseña)
                try:
                    c.authenticate()  # type: ignore[attr-defined]
                except (OSError, RuntimeError):
                    # la autenticación puede fallar si el control de Tor no está configurado; retorna False
                    return False

                if country:
                    try:
                        c.set_conf('ExitNodes', '{%s}' % country)  # type: ignore[attr-defined]
                        c.set_conf('StrictNodes', '1')  # type: ignore[attr-defined]
                    except (OSError, RuntimeError):
                        return False

                try:
                    c.signal(Signal.NEWNYM)  # type: ignore[attr-defined]
                except (OSError, RuntimeError, AttributeError):
                    return False
            return True
        except (OSError, RuntimeError) as _:
            # Error inesperado en tiempo de ejecución al controlar Tor
            return False


__all__ = ['TorController']
