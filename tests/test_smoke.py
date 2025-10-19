def test_smoke_imports():
    import importlib
    importlib.import_module('application.vpn_service')
    importlib.import_module('infrastructure.tor_controller')
    importlib.import_module('infrastructure.privoxy_controller')
    # GUI may not be available on CI
    try:
        importlib.import_module('interface.main_window')
    except (ImportError, ModuleNotFoundError):
        pass
    assert True
