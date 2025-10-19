# SECURITY

This project targets maximal anonymity and minimal traces when run on Kali Linux.

Key recommendations:

- Always run in an isolated VM or dedicated host.
- Do not run the GUI or services as root; use appropriate user accounts (e.g., debian-tor for Tor).
- Enable `CookieAuthentication 1` and `ControlPort 9051` in `/etc/tor/torrc` and secure the control cookie.
- Use virtualenv `.venv` and never install dependencies system-wide unless necessary.
- Avoid writing logs by default; if needed, write encrypted logs with strict permissions.
- Consider AppArmor/SELinux profiles and containerization for extra isolation.

Audits and leak tests:

- Periodically run DNS/IP leak tests and WebRTC leak checks.
- Monitor Tor consensus and guard node behavior.

