# ARQUITECTURA NiDeFlanders

## Hexagonal (Ports & Adapters)
- **domain/**: Entidades y lógica de negocio
- **application/**: Casos de uso y servicios
- **infrastructure/**: Integraciones externas (TOR, Privoxy, VPN, bridges)
- **interface/**: GUI y CLI
- **tests/**: Pruebas unitarias

## Principios
- SOLID, DRY, KISS, Clean Code
- Máxima privacidad y anonimato
- Sin logs ni rastros
- Código seguro y mantenible

## Flujo principal
1. El usuario interactúa con la GUI (interface/main_window.py)
2. La GUI llama a los servicios de VPN y selección de país (application/)
3. Los servicios gestionan nodos, bridges y cambios de IP (infrastructure/)
4. La protección extra y limpieza de logs se realiza desde infrastructure/privacy_guard.py

## Integraciones
- TOR: stem, bridges, cambio de IP
- Privoxy: proxy filtrado
- VPN: nodos open source
- GUI: PyGObject/GTK

## Seguridad
- Todas las dependencias verificadas
- Sin logs, sin cookies, sin rastros
- Protección anti-leaks (DNS, WebRTC)

---
DogSoulDev
