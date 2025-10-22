
# Notas de seguridad

Este documento resume los aspectos relacionados con la seguridad de NiDeFlanders.

## AppArmor

Se proporcionan perfiles de AppArmor en `packaging/apparmor/` y `tools/apparmor/`.

## Systemd

El archivo de unidad systemd se encuentra en `packaging/systemd/nideflanders.service`.

## Empaquetado Debian

Los archivos de empaquetado Debian están en `packaging/debian/` y `deb_build/`.

## Prueba de fugas

El script de prueba de fugas (`tools/leak_test.py`) verifica fugas de DNS e IP al usar Tor.

## Privoxy

Privoxy se utiliza para filtrar y anonimizar el tráfico HTTP.

## Tor

Tor se utiliza para anonimizar el tráfico de red.

## PyGObject

PyGObject se usa para la interfaz GTK.

## Recomendaciones

- Verifica siempre la integridad de los binarios descargados (usa SHA256).
- Utiliza AppArmor y systemd para reforzar la seguridad.
- Ejecuta pruebas de fugas regularmente.
- Mantén todas las dependencias actualizadas.

---
Este documento es un resumen para usuarios de NiDeFlanders. Para más detalles, consulta la documentación oficial de cada tecnología.

