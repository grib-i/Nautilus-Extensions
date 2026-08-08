from gi.repository import Gio


def file_exists(path):
    file = Gio.File.new_for_path(path)
    return file.query_exists()


def create_file(path):
    file = Gio.File.new_for_path(path)
    file.create(Gio.FileCreateFlags.NONE, None)
