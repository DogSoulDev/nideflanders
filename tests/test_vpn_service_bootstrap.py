import subprocess

from application.vpn_service import VPNService


class DummyTorController:
    def __init__(self):
        self.calls = 0
        self.socks_host = '127.0.0.1'
        self.socks_port = 9050

    def test_connection(self):
        # first call: no tor; after a bootstrap (simulated) we return True
        self.calls += 1
        return self.calls > 1

    def change_ip(self, country: str):
        _country = country
        return True


class DummyPrivoxy:
    def ensure_forward(self, host, port):
        _host = host
        _port = port
        return True

    def start(self):
        return True

    def stop(self):
        return True


def test_vpnservice_invokes_bootstrap(monkeypatch):
    # Arrange: monkeypatch TorController and PrivoxyController used inside VPNService
    dummy_tor = DummyTorController()
    monkeypatch.setattr('application.vpn_service.TorController', lambda *a, **k: dummy_tor)
    monkeypatch.setattr('application.vpn_service.PrivoxyController', lambda *a, **k: DummyPrivoxy())

    called = {}

    def fake_run(cmd, check=False, **kwargs):
        # Ensure that we are called with python <path>/tools/bootstrap_user_tor.py
        assert 'bootstrap_user_tor.py' in cmd[-1]
        called['ran'] = True
        _ = check
        _ = kwargs
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(subprocess, 'run', fake_run)

    # Act
    svc = VPNService()
    ok = svc.activate()

    # Assert
    assert called.get('ran', False) is True
    assert ok is True
