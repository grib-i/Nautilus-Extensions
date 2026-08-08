import locale
import os
from pathlib import Path

from nautilusextensions.utils.jtools import JsonRegistry
from nautilusextensions.utils.log import logger


class I18n:
    def __init__(self):
        lang_dir = (
            Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
            / "nautilus-extensions++"
            / "lang"
        )

        self.registry = JsonRegistry(lang_dir)
        self.language = self.detect_language()
        self.load_language()

    def detect_language(self):
        system = locale.getdefaultlocale()[0]
        if not system:
            return "en"

        lang = system.lower().split("_")[0]

        if lang in (
            "ru",
            "en",
            "es",
        ):
            return lang

        return "en"

    def load_language(self):
        self.registry.load(f"{self.language}.json", alias="lang")

    def get(self, key):
        value = self.registry.lang
        for part in key.split("."):
            value = getattr(value, part)

        return value
