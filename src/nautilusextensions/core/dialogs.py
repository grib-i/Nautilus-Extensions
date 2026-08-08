import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gtk


def show_error(parent, title, text):
    dialog = Adw.AlertDialog()
    dialog.set_heading(title)
    dialog.set_body(text)
    dialog.add_response("ok", "ОК")
    dialog.set_default_response("ok")
    dialog.set_close_response("ok")

    if parent:
        dialog.present(parent)

    else:
        dialog.present(None)


def show_info(parent, title, text):
    dialog = Adw.AlertDialog()
    dialog.set_heading(title)
    dialog.set_body(text)
    dialog.add_response("ok", "ОК")
    dialog.set_default_response("ok")
    dialog.present(parent)


def show_confirm(
    parent, title, text, confirm_text="Подтвердить", cancel_text="Отмена", callback=None
):
    dialog = Adw.AlertDialog()
    dialog.set_heading(title)
    dialog.set_body(text)
    dialog.add_response("cancel", cancel_text)
    dialog.add_response("confirm", confirm_text)
    dialog.set_response_appearance("confirm", Adw.ResponseAppearance.SUGGESTED)

    def response(dialog, response):
        if response == "confirm":
            if callback:
                callback()

    dialog.connect("response", response)
    dialog.present(parent)


def show_input(parent, title, placeholder="", callback=None):
    dialog = Adw.AlertDialog()
    dialog.set_heading(title)
    entry = Gtk.Entry()
    entry.set_placeholder_text(placeholder)
    dialog.set_extra_child(entry)
    dialog.add_response("cancel", "Отмена")
    dialog.add_response("ok", "ОК")
    dialog.set_response_appearance("ok", Adw.ResponseAppearance.SUGGESTED)

    def response(dialog, response):
        if response == "ok":
            if callback:
                callback(entry.get_text())

    dialog.connect("response", response)
    dialog.present(parent)
    entry.grab_focus()
