# Guía de uso de NiDeFlanders

## Instalación en Kali Linux

1. Instala dependencias del sistema:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-gi gir1.2-gtk-3.0 privoxy tor
   ```
2. Instala dependencias Python:
   ```bash
   pip3 install -r requirements.txt
   ```

## Ejecución

1. Ejecuta la interfaz gráfica:
   ```bash
   python3 interface/main_window.py
   ```
2. Cambia país/IP, activa/desactiva VPN y protección extra desde la GUI.

## Pruebas

1. Ejecuta los tests:
   ```bash
   python3 -m unittest tests/test_vpn_service.py
   ```

## Recomendaciones de seguridad
- Desactiva WebRTC en tu navegador.
- Revisa los logs y elimina rastros con la función de protección extra.

## Soporte
- Documentación: https://dogsouldev.github.io/Web/
- GitHub: https://github.com/DogSoulDev/nideflanders.git
