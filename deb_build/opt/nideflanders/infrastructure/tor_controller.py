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
        # Test the SOCKS port (Tor proxy) to ensure Tor is proxying traffic
        try:
            with socket.create_connection((self.socks_host, self.socks_port), timeout=1):
                return True
        except (OSError, ConnectionError):
            return False

    def change_ip(self, country: str | None = None) -> bool:
        """Request Tor to build new circuits. Optionally set ExitNodes country (ISO 2-letter).

        Requires Tor with ControlPort enabled. Uses stem.Controller to authenticate and send
        SETCONF / SIGNAL NEWNYM commands.
        """
        if not _STEM:
            return False
        try:
            # type: ignore[arg-type]
            with Controller.from_port(port=self.control_port) as c:  # type: ignore[arg-type]
                # try to authenticate using available methods (cookie/password)
                try:
                    c.authenticate()  # type: ignore[attr-defined]
                except (OSError, RuntimeError):
                    # authentication may fail if Tor control is not configured; return False
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
            # Unexpected runtime error while controlling Tor
            return False


__all__ = ['TorController']
