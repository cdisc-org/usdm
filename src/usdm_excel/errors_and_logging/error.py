import logging


class Error:
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    LABEL = {ERROR: "error", WARNING: "warning", DEBUG: "debug", INFO: "info"}

    def __init__(
        self, sheet: str, row: int, column: int, message: str, level: int = ERROR
    ):
        self.sheet = sheet
        self.row = row
        self.column = column
        self.message = message
        self.level = level

    def to_log(self):
        level = self.__class__.LABEL[self.level].capitalize()
        if self.sheet == None:
            return f"{level}: {self.message}"
        elif self.row == None:
            return f"{level} in sheet {self.sheet}: {self.message}"
        else:
            return f"{level} in sheet {self.sheet} at [{self.row},{self.column}]: {self.message}"

    def to_dict(self):
        return {
            "sheet": self.sheet,
            "row": self.row,
            "column": self.column,
            "message": self.message,
            "level": self.__class__.LABEL[self.level].capitalize(),
        }
