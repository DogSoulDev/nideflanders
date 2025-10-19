
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from infrastructure.privacy_guard import PrivacyGuard
from infrastructure.tor_configurator import TorConfigurator
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from application.vpn_service import VPNService
from application.tor_country_selector import TorCountrySelector


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="NiDeFlanders VPN")
        self.set_border_width(10)
        self.set_default_size(350, 220)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(vbox)

        self.status_label = Gtk.Label(label="Estado: Desconectado")
        vbox.pack_start(self.status_label, True, True, 0)

        self.toggle_button = Gtk.Button(label="Activar/Desactivar VPN")
        self.toggle_button.connect("clicked", self.on_toggle_vpn)
        vbox.pack_start(self.toggle_button, True, True, 0)

        self.country_entry = Gtk.Entry()
        self.country_entry.set_placeholder_text("Introduce país (ej: Japan, Spain, US)")
        vbox.pack_start(self.country_entry, True, True, 0)

        self.country_button = Gtk.Button(label="Seleccionar País/IP")
        self.country_button.connect("clicked", self.on_select_country)
        vbox.pack_start(self.country_button, True, True, 0)


        self.nodes_label = Gtk.Label(label="Nodos disponibles: -")
        vbox.pack_start(self.nodes_label, True, True, 0)

        self.bridge_combo = Gtk.ComboBoxText()
        self.bridge_combo.set_entry_text_column(0)
        self.bridge_combo.set_tooltip_text("Selecciona un bridge TOR (opcional)")
        vbox.pack_start(self.bridge_combo, True, True, 0)


        self.bridge_button = Gtk.Button(label="Actualizar Bridges TOR")
        self.bridge_button.connect("clicked", self.on_update_bridges)
        # Inicialización de atributos
        self.vpn_service = VPNService()
        self.tor_selector = TorCountrySelector()
        self.tor_configurator = TorConfigurator()
        self.vpn_active = False
        self.bridges = []
        vbox.pack_start(self.bridge_button, True, True, 0)

        self.privacy_button = Gtk.Button(label="Activar Protección Extra (Anti-Leaks)")
        self.privacy_button.connect("clicked", self.on_activate_privacy)
        vbox.pack_start(self.privacy_button, True, True, 0)


    def on_activate_privacy(self, _):
        dns_ok = PrivacyGuard.prevent_dns_leaks()
        logs_ok = PrivacyGuard.clean_logs()
        PrivacyGuard.disable_webrtc()
        msg = "Protección extra activada: "
        msg += "DNS seguro, " if dns_ok else "DNS error, "
        msg += "logs eliminados." if logs_ok else "error al eliminar logs."
        self.status_label.set_text(msg)

        self.vpn_service = VPNService()
        self.tor_selector = TorCountrySelector()
        self.tor_configurator = TorConfigurator()
        self.vpn_active = False
        self.bridges = []

    def on_toggle_vpn(self, _):
        if not self.vpn_active:
            if self.vpn_service.activate_vpn():
                self.status_label.set_text("Estado: Conectado")
                self.vpn_active = True
            else:
                self.status_label.set_text("Error al conectar VPN")
        else:
            if self.vpn_service.deactivate_vpn():
                self.status_label.set_text("Estado: Desconectado")
                self.vpn_active = False
            else:
                self.status_label.set_text("Error al desconectar VPN")

    def on_select_country(self, _):
        country = self.country_entry.get_text().strip()
        if not country:
            self.nodes_label.set_text("Introduce un país válido.")
            return
        self.nodes_label.set_text("Buscando nodos...")
        if self.tor_selector.update_nodes():
            nodes = self.tor_selector.select_country(country)
            if nodes:
                self.nodes_label.set_text(f"Nodos en {country}: {len(nodes)} disponibles")
                self.status_label.set_text(f"Seleccionado país: {country}")
                # Configurar bridge TOR si el usuario seleccionó uno
                selected_bridge = self.bridge_combo.get_active_text()
                if selected_bridge:
                    if self.tor_configurator.apply_bridge(selected_bridge):
                        self.status_label.set_text(f"Bridge TOR aplicado: {selected_bridge}")
                    else:
                        self.status_label.set_text("Error aplicando bridge TOR")
                # Configurar opciones de privacidad recomendadas
                self.tor_configurator.set_privacy_options()
                # Cambiar IP por TOR
                if self.tor_selector.change_tor_ip():
                    self.status_label.set_text(f"IP cambiada por TOR en {country}")
                else:
                    self.status_label.set_text("Error al cambiar IP por TOR")
            else:
                self.nodes_label.set_text(f"No hay nodos disponibles en {country}")
        else:
            self.nodes_label.set_text("Error obteniendo nodos VPN")

    def on_update_bridges(self, _):
        self.bridge_combo.remove_all()
        bridges = self.tor_selector.vpn_nodes.fetch_tor_bridges()
        if bridges:
            self.bridges = bridges
            for b in bridges:
                self.bridge_combo.append_text(b)
            self.status_label.set_text(f"{len(bridges)} bridges TOR disponibles.")
        else:
            self.status_label.set_text("No se encontraron bridges TOR.")

    # Eliminado método duplicado

    def on_change_country(self, _):
        self.status_label.set_text("Cambiando país/IP...")
        if self.vpn_service.change_country_ip():
            self.status_label.set_text("IP/Pais cambiado correctamente")
        else:
            self.status_label.set_text("Error al cambiar IP/Pais")

if __name__ == "__main__":
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
