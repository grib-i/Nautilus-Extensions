import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import ClassVar


class ColorFormatter(logging.Formatter):
    COLORS: ClassVar[dict[int, str]] = {
        logging.DEBUG: "\033[36m",
        logging.INFO: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[35m",
    }
    RESET = "\033[0m"

    def format(self, record):
        msg = super().format(record)

        if not sys.stderr.isatty():
            return msg

        color = self.COLORS.get(record.levelno, "")
        return f"{color}{msg}{self.RESET}"


def setup_logger(name: str, level: str, file_path: str = ""):
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    if logger.handlers:
        return logger

    fmt = "%(asctime)s %(name)s -> [%(levelname)s] %(message)s"

    console = logging.StreamHandler()
    console.setFormatter(ColorFormatter(fmt, datefmt="%H:%M:%S"))

    if file_path:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            file_path,
            maxBytes=1_000_000,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setFormatter(logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S"))
        logger.addHandler(file_handler)

    logger.addHandler(console)
    logger.propagate = False

    return logger
