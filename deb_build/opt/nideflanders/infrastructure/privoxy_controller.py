"""Controlador mínimo de Privoxy."""
import shutil
import subprocess
import os
from typing import Optional


class PrivoxyController:
    def __init__(self, config_path: str = '/etc/privoxy/config') -> None:
        # Allow a user-local config in XDG_DATA_HOME for zero-permissions mode
        xdg = os.environ.get('XDG_DATA_HOME') or os.path.expanduser('~/.local/share')
        user_conf_dir = os.path.join(xdg, 'nidef', 'privoxy')
        user_conf = os.path.join(user_conf_dir, 'config')
        self.user_conf_dir = user_conf_dir
        self.user_conf = user_conf
        self.config_path = config_path

    def ensure_forward(self, socks_host: str, socks_port: int) -> bool:
        """Asegura que la línea forward-socks5t esté presente en la configuración.

        Intenta escribir directamente y si falla usa sudo + tee como fallback.
        """
        cfg = f"forward-socks5t / {socks_host}:{socks_port} .\n"
        try:
            # Prefer user-local config if system config not writable
            target_conf = self.config_path
            try:
                # If system config exists and is writable and contains forward, we're done
                if os.path.exists(self.config_path):
                    with open(self.config_path, 'r', encoding='utf-8') as f:
                        if 'forward-socks5' in f.read():
                            return True
                    # test writability
                    with open(self.config_path, 'a', encoding='utf-8'):
                        pass
                else:
                    # if parent writable
                    parent = os.path.dirname(self.config_path)
                    if os.access(parent or '/', os.W_OK):
                        target_conf = self.config_path
                    else:
                        target_conf = self.user_conf

                # ensure parent exists
                os.makedirs(os.path.dirname(target_conf), exist_ok=True)
                # If target_conf already contains forward, nothing to do
                if os.path.exists(target_conf):
                    with open(target_conf, 'r', encoding='utf-8') as f:
                        if 'forward-socks5' in f.read():
                            return True
                # write minimal config header and forward rule
                with open(target_conf, 'a', encoding='utf-8') as f:
                    f.write('\n# NiDeFlanders auto-config\n')
                    f.write('listen-address  127.0.0.1:8118\n')
                    f.write(cfg)
                return True
            except (OSError, IOError):
                # fallback: attempt sudo append (best-effort)
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
                # Prefer system config_path if exists, otherwise use user-local config
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
