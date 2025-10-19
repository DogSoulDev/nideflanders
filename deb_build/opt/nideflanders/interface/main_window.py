# type: ignore
"""Interfaz mínima GTK para Kali: ventana pequeña con 2 botones."""
try:
    import gi  # type: ignore
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk  # type: ignore
    GUI_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    GUI_AVAILABLE = False
    # rely on typings/gi.pyi for static resolution when GTK is not installed

from application.vpn_service import VPNService


class MainWindow:
    def __init__(self):
        if not GUI_AVAILABLE:
            raise RuntimeError('GTK no disponible')
        self.vpn = VPNService()
        self.win = Gtk.Window(title='NiDeFlanders')
        self.win.set_default_size(300, 120)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.win.add(vbox)

        self.status_label = Gtk.Label(label='Estado: Desconectado')
        vbox.pack_start(self.status_label, True, True, 0)

        self.toggle_btn = Gtk.Button(label='Activar VPN')
        self.toggle_btn.connect('clicked', self.on_toggle)
        vbox.pack_start(self.toggle_btn, True, True, 0)

        self.country_btn = Gtk.Button(label='Cambiar País')
        self.country_btn.connect('clicked', self.on_change)
        vbox.pack_start(self.country_btn, True, True, 0)

        # ComboBox para selección rápida de país (automatizable)
        countries = ['Random', 'US', 'NL', 'DE', 'FR', 'ES', 'BR']
        store = Gtk.ListStore(str)
        for c in countries:
            store.append([c])
        self.country_combo = Gtk.ComboBox.new_with_model(store)
        renderer_text = Gtk.CellRendererText()
        self.country_combo.pack_start(renderer_text, True)
        self.country_combo.add_attribute(renderer_text, 'text', 0)
        self.country_combo.set_active(0)
        vbox.pack_start(self.country_combo, True, True, 0)

        # minimal UI: only status, toggle and country selector

    def on_toggle(self, _):
        if not self.vpn.is_active():
            ok = self.vpn.activate()
            if ok:
                self.status_label.set_text('Estado: Conectado')
                self.toggle_btn.set_label('Desactivar VPN')
            else:
                self.status_label.set_text('Error al conectar')
        else:
            ok = self.vpn.deactivate()
            if ok:
                self.status_label.set_text('Estado: Desconectado')
                self.toggle_btn.set_label('Activar VPN')
            else:
                self.status_label.set_text('Error al desconectar')

    def on_change(self, _):
        # Dialog para pedir país
        dialog = Gtk.MessageDialog(transient_for=self.win, flags=0, message_type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.OK_CANCEL, text='Introduce país')
        entry = Gtk.Entry()
        dialog.vbox.pack_end(entry, False, False, 0)
        dialog.show_all()
        resp = dialog.run()
        if resp == Gtk.ResponseType.OK:
            country = entry.get_text().strip()
            if country:
                ok = self.vpn.change_country(country)
                self.status_label.set_text('IP cambiada' if ok else 'Error')
        dialog.destroy()

    def on_autostart(self, _):
        # deprecated in minimal UI
        pass

    def on_menu_status(self, _):
        # comprobar si tor está en PATH
        import shutil
        tor = shutil.which('tor')
        self.status_label.set_text('tor en PATH: ' + (tor or 'no'))

    def on_menu_autostart(self, _):
        # no-op for minimal UI
        pass

    def on_button_press(self, _widget, _event):
        # botón derecho muestra menu contextual
        # no contextual menu in minimal UI
        return


def main():
    if not GUI_AVAILABLE:
        print('GTK no disponible. Usa CLI.')
        return
    mw = MainWindow()
    mw.win.connect('destroy', Gtk.main_quit)
    mw.win.show_all()
    # Autoconnect support: set NIDEF_AUTO_CONNECT=1 to auto-activate on startup
    import os
    if os.environ.get('NIDEF_AUTO_CONNECT') == '1':
        try:
            mw.on_toggle(None)
        except (RuntimeError, OSError):
            # ignore startup activation failures; user can retry manually
            pass
    Gtk.main()

if __name__ == '__main__':
    main()
