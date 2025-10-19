#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PKG_DIR="$ROOT_DIR/deb_build"
rm -rf "$PKG_DIR"
mkdir -p "$PKG_DIR/DEBIAN"
mkdir -p "$PKG_DIR/opt/nideflanders"

# copy project into /opt/nideflanders (exclude the deb_build dest)
if command -v rsync >/dev/null 2>&1; then
	rsync -a --exclude 'deb_build' --exclude '.git' --exclude '__pycache__' "$ROOT_DIR/" "$PKG_DIR/opt/nideflanders/"
else
	echo "rsync not found; falling back to cp -a (may include extra files)"
	mkdir -p "$PKG_DIR/opt/nideflanders"
	# Use a temporary tarball to avoid copying into the destination directory
	TMP_TAR=$(mktemp --suffix=.tar || mktemp -t nidef.tar)
	(cd "$ROOT_DIR" && tar --exclude='./deb_build' --exclude='.git' -cf "$TMP_TAR" .)
	mkdir -p "$PKG_DIR/opt/nideflanders"
	(cd "$PKG_DIR/opt/nideflanders" && tar -xf "$TMP_TAR")
	rm -f "$TMP_TAR"
fi

# copy debian maintainer scripts if present
if [ -f "$ROOT_DIR/packaging/debian/postinst" ]; then
	cp "$ROOT_DIR/packaging/debian/postinst" "$PKG_DIR/DEBIAN/postinst"
	chmod 755 "$PKG_DIR/DEBIAN/postinst"
fi
if [ -f "$ROOT_DIR/packaging/debian/prerm" ]; then
	cp "$ROOT_DIR/packaging/debian/prerm" "$PKG_DIR/DEBIAN/prerm"
	chmod 755 "$PKG_DIR/DEBIAN/prerm"
elif [ -f "$ROOT_DIR/packaging/debian/prerm.sh" ]; then
	cp "$ROOT_DIR/packaging/debian/prerm.sh" "$PKG_DIR/DEBIAN/prerm"
	chmod 755 "$PKG_DIR/DEBIAN/prerm"
fi
if [ -f "$ROOT_DIR/packaging/debian/postrm" ]; then
  cp "$ROOT_DIR/packaging/debian/postrm" "$PKG_DIR/DEBIAN/postrm"
  chmod 755 "$PKG_DIR/DEBIAN/postrm"
fi

# write control
cat > "$PKG_DIR/DEBIAN/control" <<CTRL
Package: nideflanders
Version: 0.1
Section: net
Priority: optional
Architecture: all
Depends: python3, python3-venv, python3-gi, adduser
Recommends: tor, privoxy
Maintainer: DogSoulDev <noreply@example.com>
Description: NiDeFlanders - simple Tor-based VPN wrapper for Kali
 NiDeFlanders installs under /opt/nideflanders and provides /usr/local/bin/nideflanders
CTRL

# set permissions
chmod -R 755 "$PKG_DIR/opt/nideflanders" || true

# build (requires fakeroot & dpkg-deb installed on host)
if ! command -v dpkg-deb >/dev/null 2>&1; then
	echo "dpkg-deb not found. Install 'dpkg-dev' (on Debian/Kali) and rerun this script." >&2
	exit 2
fi
if ! command -v fakeroot >/dev/null 2>&1; then
	echo "fakeroot not found. Install 'fakeroot' (on Debian/Kali) and rerun this script." >&2
	exit 2
fi

fakeroot dpkg-deb --build "$PKG_DIR" "$ROOT_DIR/nideflanders_0.1_all.deb"
echo "DEB built: $ROOT_DIR/nideflanders_0.1_all.deb"
