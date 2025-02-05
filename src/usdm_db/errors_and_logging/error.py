import logging


class Error:
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    LABEL = {
        CRITICAL: "critical",
        ERROR: "error",
        WARNING: "warning",
        DEBUG: "debug",
        INFO: "info",
    }

    def __init__(self, message: str, level: int = ERROR):
        self.message = message
        self.level = level

    def to_log(self):
        level = self.__class__.LABEL[self.level].capitalize()
        return f"{level}: {self.message}"

    def to_dict(self):
        return {
            "message": self.message,
            "level": self.__class__.LABEL[self.level].capitalize(),
        }
