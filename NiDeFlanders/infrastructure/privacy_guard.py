"""
Módulo para protección extra: anti-leaks (DNS, WebRTC), sin logs, sin rastros.
"""
import subprocess

class PrivacyGuard:
    @staticmethod
    def prevent_dns_leaks():
        """Configura resolv.conf para usar solo DNS seguro por Tor."""
        try:
            subprocess.run(["sudo", "sh", "-c", "echo 'nameserver 127.0.0.1' > /etc/resolv.conf"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error configurando DNS seguro: {e}")
            return False

    @staticmethod
    def disable_webrtc():
        """Recomienda desactivar WebRTC en navegadores (no se puede forzar por Python)."""
        print("Desactiva WebRTC en la configuración de tu navegador para evitar fugas de IP.")
        return True

    @staticmethod
    def clean_logs():
        """Elimina logs y rastros del sistema relacionados con la VPN y Tor."""
        try:
            subprocess.run(["sudo", "sh", "-c", "rm -rf /var/log/tor/* /var/log/privoxy/*"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error eliminando logs: {e}")
            return False
