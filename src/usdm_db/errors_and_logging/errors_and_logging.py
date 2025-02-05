import logging
import traceback
import warnings
from usdm_db.errors_and_logging.errors import Errors


class ErrorsAndLogging:
    WARNING = Errors.WARNING
    ERROR = Errors.ERROR
    DEBUG = Errors.DEBUG
    INFO = Errors.INFO

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._errors = Errors()

    def errors(self):
        return self._errors

    def debug(self, message: str):
        self._logger.debug(message)

    def info(self, message: str):
        self._logger.info(message)

    def exception(self, message: str, e: Exception):
        self._errors.add(
            f"Exception. {message}. See log for additional details.", self._errors.ERROR
        )
        self._logger.error(
            f"Exception '{e}' raised\n\n{message}\n\n{traceback.format_exc()}"
        )

    def warning(self, message: str):
        self._errors.add(message, self._errors.WARNING)
        self._logger.warning(message)

    def error(self, message: str):
        self._errors.add(message, self._errors.ERROR)
        self._logger.error(message)

    def deprecated(self, message: str):
        warnings.warn(message, DeprecationWarning)
        self.warning(message)
