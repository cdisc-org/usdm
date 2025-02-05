import logging
from .error import Error


class Errors:
    CRITICAL = Error.CRITICAL
    WARNING = Error.WARNING
    ERROR = Error.ERROR
    DEBUG = Error.DEBUG
    INFO = Error.INFO

    def __init__(self):
        self.items = []
        self._logger = logging.getLogger(__name__)

    def clear(self):
        self.items = []

    def add(self, message: str, level: int = Error.ERROR) -> None:
        error = Error(message, level)
        self.items.append(error)
        self._logger.log(level, error.to_log())

    def count(self) -> int:
        return len(self.items)

    def dump(self, level):
        result = []
        for item in self.items:
            if item.level >= level:
                result.append(item.to_dict())
        return result
