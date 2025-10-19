#!/bin/bash
# Instalador y lanzador automático para NiDeFlanders en Kali Linux
set -e

# Instalar dependencias del sistema
sudo apt update
sudo apt install -y python3 python3-pip python3-gi gir1.2-gtk-3.0 privoxy tor

# Instalar dependencias Python
pip3 install -r requirements.txt

# Lanzar la aplicación
python3 interface/main_window.py
