import logging
import traceback
import warnings
from usdm_excel.errors_and_logging.errors import Errors


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

    def debug(
        self, message: str, sheet: str = None, row: int = None, column: int = None
    ):
        self._logger.debug(self._format(message, sheet, row, column))

    def info(
        self, message: str, sheet: str = None, row: int = None, column: int = None
    ):
        self._logger.info(self._format(message, sheet, row, column))

    def exception(
        self,
        message: str,
        e: Exception,
        sheet: str = None,
        row: int = None,
        column: int = None,
    ):
        self._errors.add(
            sheet,
            row,
            column,
            f"Exception. {message}. See log for additional details.",
            self._errors.ERROR,
        )
        self._logger.error(
            f"Exception '{e}' raised\n\n{self._format(message, sheet, row, column)}\n\n{traceback.format_exc()}"
        )

    def warning(
        self, message: str, sheet: str = None, row: int = None, column: int = None
    ):
        self._errors.add(sheet, row, column, message, self._errors.WARNING)
        self._logger.warning(self._format(message, sheet, row, column))

    def error(
        self, message: str, sheet: str = None, row: int = None, column: int = None
    ):
        self._errors.add(sheet, row, column, message, self._errors.ERROR)
        self._logger.error(self._format(message, sheet, row, column))

    def deprecated(self, message):
        warnings.warn(message, DeprecationWarning)
        self._logger.warning(self._format(message, None, None, None))

    def _format(self, message, sheet, row, column):
        if not sheet:
            return f"{message}"
        elif row == None:
            return f"In sheet {sheet}: {message}"
        else:
            return f"In sheet {sheet} at [{row},{column}]: {message}"
