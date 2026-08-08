from gi.repository import Gtk


def find_nautilus_window():
    for window in Gtk.Window.list_toplevels():
        if not window.get_visible():
            continue

        app = window.get_application()

        if app is None:
            continue

        if app.get_application_id() == "org.gnome.Nautilus":
            return window

    return None
