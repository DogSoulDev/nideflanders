# NiDeFlanders

Proyecto universitario para la privacidad y anonimato en Kali Linux.

## Descripción
NiDeFlanders es una VPN para Kali Linux, diseñada con arquitectura hexagonal, principios SOLID, DRY, KISS y Clean Code. El objetivo es ofrecer máxima privacidad, anonimato y facilidad de uso, integrando la red TOR y nodos open source para cambiar país/IP, sin dejar rastros ni logs.

- Solo para Kali Linux (no Windows)
- Interfaz gráfica sencilla, anclada en la barra de tareas
- Cambiar país/IP, activar/desactivar VPN
- Todo el tráfico pasa por TOR y Privoxy
- Sin logs, cookies ni rastros
- Código seguro y verificado (2025)

## Repositorio y documentación
- GitHub: https://github.com/DogSoulDev/nideflanders.git
- Documentación: https://dogsouldev.github.io/Web/

## Estructura del proyecto
- domain/: Lógica de negocio y entidades
- application/: Casos de uso y servicios
- infrastructure/: Integraciones externas (TOR, Privoxy, VPN, etc.)
- interface/: Interfaz gráfica y CLI
- tests/: Pruebas unitarias y de integración

## Dependencias recomendadas

![NiDeFlanders Logo](assets/nideflanders.png)

# NiDeFlanders

Proyecto universitario para la privacidad y anonimato en Kali Linux.

## Instalación y ejecución automática
1. Descarga el repositorio desde GitHub.
2. Ejecuta en terminal:
	```bash
	bash run_nideflanders.sh
	```
Esto instalará dependencias y abrirá la interfaz gráfica automáticamente.

## Descripción
NiDeFlanders es una VPN para Kali Linux, diseñada con arquitectura hexagonal, principios SOLID, DRY, KISS y Clean Code. El objetivo es ofrecer máxima privacidad, anonimato y facilidad de uso, integrando la red TOR y nodos open source para cambiar país/IP, sin dejar rastros ni logs.

- Solo para Kali Linux (no Windows)
- Interfaz gráfica sencilla, anclada en la barra de tareas
- Cambiar país/IP, activar/desactivar VPN
- Todo el tráfico pasa por TOR y Privoxy
- Sin logs, cookies ni rastros
- Código seguro y verificado (2025)

## Repositorio y documentación
- GitHub: https://github.com/DogSoulDev/nideflanders.git
- Documentación: https://dogsouldev.github.io/Web/

## Estructura del proyecto
- domain/: Lógica de negocio y entidades
- application/: Casos de uso y servicios
- infrastructure/: Integraciones externas (TOR, Privoxy, VPN, etc.)
- interface/: Interfaz gráfica y CLI
- tests/: Pruebas unitarias y de integración

## Dependencias recomendadas
- Python 3.12+
- stem (control de TOR)
- requests (HTTP anónimo)
- toripchanger (cambio de IP)
- privoxy se instala por sistema (no por pip)

## Seguridad
Todas las dependencias serán verificadas para evitar vulnerabilidades conocidas en 2025.

## Licencia
GNU GPL v3

---
DogSoulDev
