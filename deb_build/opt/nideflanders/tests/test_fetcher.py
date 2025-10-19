import urllib.request

from tools import fetch_tor_relays


def test_fetch_top_relays_empty(monkeypatch):
    # Simulate an empty onionoo response
    class DummyResp:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return b'{}'

    def fake_urlopen(*_args, **_kwargs):
        # Accept arbitrary args/kwargs to mirror urllib.request.urlopen signature
        return DummyResp()

    monkeypatch.setattr(urllib.request, 'urlopen', fake_urlopen)
    relays = fetch_tor_relays.fetch_top_relays(_limit=10)
    assert isinstance(relays, list)
    assert relays == []