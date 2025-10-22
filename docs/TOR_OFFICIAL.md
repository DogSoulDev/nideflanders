# Tor — Notas oficiales de uso
==========================

Este documento resume las recomendaciones oficiales del Proyecto Tor para usar Tor de forma segura y correcta.
## 1) Usa el Tor Browser siempre que sea posible

- El Tor Browser es la única forma oficialmente soportada para navegar por la web usando Tor.
## 2) Evita usar Tor a nivel de sistema para navegar por la web

- Tor instalado a nivel de sistema (por ejemplo, mediante `apt install tor`) no se recomienda para navegación web, ya que carece de las protecciones de privacidad del Tor Browser.
## 3) Usa Tor a nivel de sistema para aplicaciones que no sean web

- Tor a nivel de sistema es adecuado para herramientas de línea de comandos, scripts y otras aplicaciones que soportan proxies SOCKS5.
## 4) Nunca uses Tor para BitTorrent u otras aplicaciones P2P

- Tor no está diseñado para tráfico de alto ancho de banda o P2P y puede exponer tu dirección IP.
## 5) No uses Tor para actividades ilegales

- El Proyecto Tor no aprueba el uso ilegal y no te protegerá de la ley.
## 6) Mantén Tor y el software relacionado actualizado

- Actualiza regularmente Tor, el Tor Browser y Privoxy para tener los últimos parches de seguridad.
## 7) Lee la documentación oficial

- https://support.torproject.org/
- https://2019.www.torproject.org/docs/documentation.html.en
---
Este documento es un resumen para usuarios de NiDeFlanders. Para más detalles, consulta siempre la documentación oficial del Proyecto Tor.
# Referencias oficiales y recomendaciones del Proyecto Tor

Este documento reúne notas y enlaces oficiales del Proyecto Tor (Tor Project) para
ayudar a integrar, verificar y usar software y listados de nodos de forma fiable.

Contenido breve:

- Qué es Tor y sus límites
- Cómo verificar descargas (firmas GPG / checksum)
- Puentes (bridges) y pluggable transports
- Búsqueda de relays y métricas oficiales
- Recomendaciones de configuración y advertencias
- Fuentes oficiales

Resumen (puntos clave)

- Tor protege sólo el tráfico que vaya explícitamente a través de él. No "tuneliza"
  automáticamente todo el sistema salvo que configures un cliente/servicio para ello.
- No uses BitTorrent u otros protocolos no compatibles sobre Tor (pueden filtrar IP).
- Evita editar `torrc` sin entender las implicaciones: cambiar rutas, forzar ExitNodes o
  tocar opciones sensibles puede comprometer el anonimato.

Verificar descargas (recomendado cuando uses bundles o Tor Expert Bundle)

1) Importar la llave de los desarrolladores de Tor (ejemplo):

  gpg --auto-key-locate nodefault,wkd --locate-keys torbrowser@torproject.org

2) Verificar firme (ejemplo Windows/macOS con gpgv):

  gpgv --keyring ./tor.keyring Downloads/<archivo>.asc Downloads/<archivo>

Consejo: cuando automatices descargas (por ej. bootstrap de Tor userland), preferir
verificación GPG sobre sólo SHA256. SHA256 es útil como mínima comprobación, pero
la verificación GPG con la llave oficial protege contra descargas maliciosas.

Puentes y pluggable transports

- Las páginas oficiales para obtener puentes y transporte pluggable son:
  - https://bridges.torproject.org/
  - https://tb-manual.torproject.org/bridges/
- Pluggable transports disponibles: obfs4, Snowflake, meek, WebTunnel. Para redes censuradas
  estas suelen ser la vía correcta.

Búsqueda de relays y métricas

- Tor Metrics y Relay Search (consulta oficial de relays / puentes):
  - https://metrics.torproject.org/
  - https://metrics.torproject.org/rs.html
- Datos de métricas ofrecidos bajo dominio público (CC0) por Tor Metrics. Útiles para
  evaluar estabilidad, bandwidth, flags (Guard/Exit/Stable) y otros indicadores.

Recomendaciones explícitas del Proyecto Tor (resumen)

- No fuerces rutas salvo que sepas lo que haces. Desde la documentación oficial:
  "Modifying the way that Tor creates its circuits is strongly discouraged."
- Si la necesidad es geolocalización (ej. recursos restringidos por país), considera
  un VPN en lugar de forzar ExitNodes: un VPN no comparte las mismas propiedades de
  anonimato que Tor, pero resuelve geobloqueos de manera más adecuada.
- Para operaciones en servidores (relays / bridges) seguir la guía oficial para operadores:
  https://community.torproject.org/relay/

Fuentes oficiales (enlaces primarios)

- Manual y FAQ de Tor: https://www.torproject.org/docs/tor-manual.html.en
- Tor Browser manual y verificación de firma: https://tb-manual.torproject.org/
- Bridges: https://bridges.torproject.org/
- Relay Search / Tor Metrics: https://metrics.torproject.org/rs.html
- Instalar Tor desde repositorios oficiales (APT/RPM): https://support.torproject.org/apt/

Integración con este proyecto

1) Plantilla `config/nodes.yml` (ejemplo) creada al lado de este documento. Objetivo:
   - centralizar fuentes confiables (Tor Metrics, BridgeDB, repositorios oficiales)
   - permitir añadir entradas manuales verificadas (bridges, relays, proveedores VPN open-source)

2) Recomendación de automatización segura:
   - Si implementas un "fetcher" automático, que:
     * descargue sólo desde fuentes oficiales o mirrors verificados
     * verifique firmas GPG o checksums firmados
     * registre (localmente) la huella/fecha de la última verificación

3) Advertencia legal/operativa:
   - Ejecutar relays o exits implica responsabilidad legal en algunas jurisdicciones.
   - Nunca instales o configures un exit relay en una red doméstica sin conocer riesgos.

Ejemplo rápido: verificación mínima SHA256 (no sustitutiva de GPG)

  # descargar
  curl -L -o tor-expert-bundle.tar.xz https://www.torproject.org/download/tor/
  # comprobar SHA256 provista por el sitio (manual)
  sha256sum tor-expert-bundle.tar.xz

Mejor práctica: descargar el `.asc` firmado y usar gpgv con la keyring oficial.

Notas finales

- Si quieres que el proyecto descargue y mantenga una lista de nodos, dime si prefieres:
  A) sólo referencias y plantilla (esto), o
  B) un script automático que consulte Tor Metrics / Relay Search y guarde un YAML
     con verificación incremental (requiere network + manejo de claves GPG).

Documento construido desde resúmenes y extractos oficiales del Proyecto Tor
y sus recursos públicos (Tor Project / Tor Metrics / Bridges).
