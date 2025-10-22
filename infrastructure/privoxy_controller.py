"""Controlador mínimo de Privoxy."""
import shutil
import subprocess
import os
from typing import Optional


class PrivoxyController:
    def __init__(self, config_path: str = '/etc/privoxy/config') -> None:
    # Permite una configuración local del usuario en XDG_DATA_HOME para modo sin permisos
        xdg = os.environ.get('XDG_DATA_HOME') or os.path.expanduser('~/.local/share')
        user_conf_dir = os.path.join(xdg, 'nidef', 'privoxy')
        user_conf = os.path.join(user_conf_dir, 'config')
        self.user_conf_dir = user_conf_dir
        self.user_conf = user_conf
        self.config_path = config_path

    def ensure_forward(self, socks_host: str, socks_port: int) -> bool:
        """Asegura que la línea forward-socks5t esté presente en la configuración.

        Intenta escribir directamente y si falla usa sudo + tee como alternativa.
        """
        cfg = f"forward-socks5t / {socks_host}:{socks_port} .\n"
        try:
            # Prefiere la configuración local del usuario si la del sistema no es escribible
            target_conf = self.config_path
            try:
                # Si la configuración del sistema existe, es escribible y contiene forward, ya está listo
                if os.path.exists(self.config_path):
                    with open(self.config_path, 'r', encoding='utf-8') as f:
                        if 'forward-socks5' in f.read():
                            return True
                    # prueba si es escribible
                    with open(self.config_path, 'a', encoding='utf-8'):
                        pass
                else:
                    # si el directorio padre es escribible
                    parent = os.path.dirname(self.config_path)
                    if os.access(parent or '/', os.W_OK):
                        target_conf = self.config_path
                    else:
                        target_conf = self.user_conf

                # asegura que el directorio padre exista
                os.makedirs(os.path.dirname(target_conf), exist_ok=True)
                # Si target_conf ya contiene forward, no hay nada que hacer
                if os.path.exists(target_conf):
                    with open(target_conf, 'r', encoding='utf-8') as f:
                        if 'forward-socks5' in f.read():
                            return True
                # escribe cabecera mínima de configuración y regla forward
                with open(target_conf, 'a', encoding='utf-8') as f:
                    f.write('\n# NiDeFlanders auto-config\n')
                    f.write('listen-address  127.0.0.1:8118\n')
                    f.write(cfg)
                return True
            except (OSError, IOError):
                # alternativa: intenta añadir con sudo (mejor esfuerzo)
                try:
                    cmd = ("printf '%s' " + repr('\n# NiDeFlanders auto-config\nlisten-address 127.0.0.1:8118\n' + cfg) + f" | sudo tee -a {self.config_path} > /dev/null")
                    subprocess.run(['bash', '-lc', cmd], check=True)
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    return False
        except (OSError, IOError):
            return False

    def start(self) -> bool:
        """Intenta iniciar Privoxy usando systemctl o ejecutable directo."""
        if shutil.which('systemctl'):
            try:
                subprocess.run(['sudo', 'systemctl', 'start', 'privoxy'], check=True)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False

        binp: Optional[str] = shutil.which('privoxy')
        if binp:
            try:
                # Prefiere config_path del sistema si existe, si no usa la configuración local del usuario
                conf = self.config_path if os.path.exists(self.config_path) else self.user_conf
                os.makedirs(os.path.dirname(conf), exist_ok=True)
                subprocess.Popen([binp, conf, '--no-daemon'])
                return True
            except (OSError, FileNotFoundError):
                return False
        return False

    def stop(self) -> bool:
        """Detiene Privoxy si es posible."""
        if shutil.which('systemctl'):
            try:
                subprocess.run(['sudo', 'systemctl', 'stop', 'privoxy'], check=True)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False
        return False
