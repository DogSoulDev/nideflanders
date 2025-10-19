# Arquitectura de NiDeFlanders

## Hexagonal (Ports & Adapters)
- **domain/**: Entidades y lógica de negocio
- **application/**: Casos de uso y servicios
- **infrastructure/**: Integraciones externas (Tor, Privoxy, VPN, bridges, privacidad)
- **interface/**: GUI principal y CLI
- **tests/**: Pruebas unitarias y de integración
- **assets/**: Imágenes y recursos gráficos
- **docs/**: Documentación interna

## Principios aplicados
- **SOLID**: Clases y módulos desacoplados, responsabilidad única
- **DRY**: Sin duplicidad de lógica
- **KISS**: Código simple y fácil de mantener
- **Clean Code**: Nombres claros, comentarios útiles, modularidad

## Flujo principal
1. El usuario abre la GUI y selecciona país/IP y bridge TOR
2. El sistema obtiene nodos VPN open source y bridges TOR automáticamente
3. Se configura Tor y Privoxy para enrutar tráfico por el país y bridge elegidos
4. Se activa protección extra (anti-leaks, sin logs)
5. Todo el tráfico se enruta por Tor y VPN, sin rastros ni fugas

## Seguridad
- Sin logs ni cookies
- DNS seguro por Tor
- Bridges TOR automáticos
- Recomendación de desactivar WebRTC
- Dependencias verificadas y actualizadas

---
DogSoulDev
