
<div align="center">
   <img src="../assets/nideflanders.png" alt="NiDeFlanders" style="max-width:300px; display:block; margin:auto;" />
</div>

# Guía de uso de NiDeFlanders

## Requisitos
- Kali Linux
- Python 3.12+
- Tor y Privoxy instalados
- PyGObject/GTK instalado (`sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0`)

## Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/DogSoulDev/nideflanders.git
   ```
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Instala Tor y Privoxy:
   ```bash
   sudo apt install tor privoxy
   ```

## Ejecución
1. Ejecuta el programa principal:
   ```bash
   python3 interface/main_window.py
   ```
2. Usa la ventana para:
   - Activar/desactivar la VPN
   - Seleccionar país/IP
   - Elegir bridge TOR
   - Activar protección extra (anti-leaks)

## Carpeta de imágenes
Guarda capturas de pantalla y recursos gráficos en `assets/`.

## Documentación avanzada
Consulta la web oficial: [https://dogsouldev.github.io/Web/](https://dogsouldev.github.io/Web/)

---
DogSoulDev
