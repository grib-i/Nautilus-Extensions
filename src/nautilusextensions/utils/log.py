from pathlib import Path

from nautilusextensions.utils.logger import setup_logger

LOG_PATH = Path.home() / ".cache" / "nautilus-extensions" / "nautilus-extensions.log"


logger = setup_logger("NautilusExtensions", "DEBUG", str(LOG_PATH))
