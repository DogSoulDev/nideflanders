# Remaining work and prioritized plan

1) CI and tests (high)
   - GitHub Actions workflow added (mocked tests + linting)
2) Hardening (high)
   - AppArmor/SELinux, non-root execution, systemd units with least privilege
3) Leak testing (medium)
   - Automated leak tests and integration tests on a Kali VM
4) Packaging (medium)
   - Debian package, installation scripts, systemd unit creation
5) UX and documentation (low)
   - Better GUI feedback, documentation for bridges and hidden services

If you want I can start implementing any of these in order; por ejemplo puedo empezar con las pruebas de fuga o con la creación de paquetes .deb.
