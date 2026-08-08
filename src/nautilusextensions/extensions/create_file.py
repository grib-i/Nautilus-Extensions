import os

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Nautilus", "4.0")

from gi.repository import Adw, GObject, Gtk, Nautilus

from nautilusextensions.core.dialogs import show_error
from nautilusextensions.core.gio import create_file, file_exists
from nautilusextensions.core.i18n import I18n
from nautilusextensions.core.nautilus import find_nautilus_window
from nautilusextensions.utils.log import logger

i18n = I18n()


class CreateFileExtension(GObject.GObject, Nautilus.MenuProvider):
    def get_background_items(self, current_folder):
        logger.debug("Creating CreateFile menu item")

        # item = Nautilus.MenuItem(
        #     name="NautilusCreateFile::CreateFile",
        #     label=f"{i18n.get('create_file.title')}\t{i18n.get('create_file.shortcut')}",
        #     tip=f"{i18n.get('create_file.tip')} ({i18n.get('create_file.shortcut')})",
        # )

        item = Nautilus.MenuItem(
            name="NautilusCreateFile::CreateFile",
            label=i18n.get("create_file.title"),
            tip="",
        )

        item.connect("activate", self.on_create_file, current_folder)

        return [item]

    def on_create_file(self, menu_item, folder):
        logger.debug("Create file activated")

        folder_path = folder.get_location().get_path()

        logger.debug(f"Folder path: {folder_path}")

        if not folder_path:
            logger.warning("Folder path is empty")
            return

        dialog = Adw.Dialog()
        dialog.set_content_width(380)

        header = Adw.HeaderBar()
        cancel = Gtk.Button(label=i18n.get("create_file.cancel"))
        create = Gtk.Button(label=i18n.get("create_file.create"))

        create.add_css_class("suggested-action")
        create.set_sensitive(False)

        header.pack_start(cancel)
        header.pack_end(create)

        entry = Gtk.Entry()
        entry.set_placeholder_text(i18n.get("create_file.name"))

        entry.set_margin_top(12)
        entry.set_margin_bottom(12)
        entry.set_margin_start(12)
        entry.set_margin_end(12)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        box.append(entry)

        toolbar = Adw.ToolbarView()
        toolbar.add_top_bar(header)
        toolbar.set_content(box)

        dialog.set_child(toolbar)

        def update(entry):
            create.set_sensitive(bool(entry.get_text().strip()))

        entry.connect("changed", update)

        def make_file(*args):
            name = entry.get_text().strip()

            logger.debug(f"Creating file: {name}")

            if "/" in name:
                logger.warning(f"Invalid filename: {name}")

                show_error(dialog, "Ошибка", "Недопустимое имя")
                return

            path = os.path.join(folder_path, name)

            logger.debug(f"File path: {path}")

            if file_exists(path):
                logger.warning(f"File already exists: {path}")

                show_error(dialog, i18n.get("create_file.exists"), name)

                return

            try:
                create_file(path)

                logger.info(f"File created: {path}")

                dialog.close()

            except Exception:
                logger.exception(f"Failed creating file: {path}")

        create.connect("clicked", make_file)
        entry.connect("activate", make_file)
        cancel.connect("clicked", lambda x: dialog.close())

        logger.debug("Presenting dialog")

        dialog.present(find_nautilus_window())
        entry.grab_focus()
