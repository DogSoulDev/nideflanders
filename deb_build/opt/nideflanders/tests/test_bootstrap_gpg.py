from tools import bootstrap_user_tor as b


def test_verify_archive_no_checks(tmp_path, monkeypatch):
    # Create a dummy archive file
    archive = tmp_path / 'dummy.tar.xz'
    archive.write_bytes(b'content')

    # No gpg, no sha provided
    monkeypatch.setattr(b, 'gpg_available', lambda: False)
    ok = b.verify_archive(str(archive), asc_url=None, archive_dir=str(tmp_path), expected_sha=None, strict_gpg=False)
    assert ok is True


def test_verify_archive_gpg_success(tmp_path, monkeypatch):
    archive = tmp_path / 'dummy.tar.xz'
    archive.write_bytes(b'content')

    monkeypatch.setattr(b, 'gpg_available', lambda: True)
    monkeypatch.setattr(b, 'download_if_exists', lambda url, dest: True)
    monkeypatch.setattr(b, 'verify_with_gpg', lambda asc, art: True)

    ok = b.verify_archive(str(archive), asc_url='http://example/x.asc', archive_dir=str(tmp_path), expected_sha=None, strict_gpg=True)
    assert ok is True


def test_verify_archive_gpg_fail_sha_success(tmp_path, monkeypatch):
    archive = tmp_path / 'dummy.tar.xz'
    archive.write_bytes(b'content')

    # GPG available but verification fails
    monkeypatch.setattr(b, 'gpg_available', lambda: True)
    monkeypatch.setattr(b, 'download_if_exists', lambda url, dest: True)
    monkeypatch.setattr(b, 'verify_with_gpg', lambda asc, art: False)

    # Provide correct SHA
    import hashlib
    h = hashlib.sha256()
    h.update(b'content')
    sha = h.hexdigest()

    ok = b.verify_archive(str(archive), asc_url='http://example/x.asc', archive_dir=str(tmp_path), expected_sha=sha, strict_gpg=False)
    assert ok is True