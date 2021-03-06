import logging
import os.path
from typing import Callable, Literal, TypeAlias

from kl_site_common.const import LOG_TO_DIR


LogLevels: TypeAlias = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]


_logger = logging.getLogger("KL-Site-Back")

_log_func_map: dict[LogLevels, Callable[[str], None]] = {
    "CRITICAL": _logger.critical,
    "ERROR": _logger.error,
    "WARNING": _logger.warning,
    "INFO": _logger.info,
    "DEBUG": _logger.debug,
}

if LOG_TO_DIR:
    _handler = logging.FileHandler(
        filename=os.path.join(LOG_TO_DIR, "server.log"), encoding="utf-8",
    )
    _handler.setFormatter(logging.Formatter(
        fmt="%(levelname)8s %(asctime)s.%(msecs)03d: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))

    _logger.addHandler(_handler)
    _logger.setLevel(logging.DEBUG)  # All messages should be logged


def log_message_to_file(level: LogLevels, message: str):
    if level not in _log_func_map:
        raise ValueError(f"Invalid log level: {level}")

    if not LOG_TO_DIR:
        raise ValueError("Logging to file not enabled. Check config option: `log.output-directory`.")

    _log_func_map[level](message)
