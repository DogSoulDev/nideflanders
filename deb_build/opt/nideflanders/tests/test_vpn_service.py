from application.vpn_service import VPNService


class DummyTor:
    def __init__(self):
        self.socks_host = '127.0.0.1'
        self.socks_port = 9050
        self.changed = False

    def test_connection(self) -> bool:
        return True

    def change_ip(self, _country: str | None = None) -> bool:
        self.changed = True
        return True


class DummyPrivoxy:
    def __init__(self):
        self.started = False
        self.stopped = False
        self.forwards = False

    def ensure_forward(self, _socks_host: str, _socks_port: int) -> bool:
        self.forwards = True
        return True

    def start(self) -> bool:
        self.started = True
        return True

    def stop(self) -> bool:
        self.stopped = True
        return True


def test_activate_deactivate(monkeypatch):
    tor = DummyTor()
    priv = DummyPrivoxy()

    monkeypatch.setattr('application.vpn_service.TorController', lambda *a, **k: tor)
    monkeypatch.setattr('application.vpn_service.PrivoxyController', lambda *a, **k: priv)

    svc = VPNService()
    assert not svc.is_active()
    assert svc.activate() is True
    assert svc.is_active() is True
    assert priv.forwards is True and priv.started is True

    assert svc.deactivate() is True
    assert svc.is_active() is False
    assert priv.stopped is True


def test_change_country(monkeypatch):
    tor = DummyTor()
    priv = DummyPrivoxy()
    monkeypatch.setattr('application.vpn_service.TorController', lambda *a, **k: tor)
    monkeypatch.setattr('application.vpn_service.PrivoxyController', lambda *a, **k: priv)

    svc = VPNService()
    ok = svc.change_country('US')
    assert ok is True
    assert tor.changed is True
