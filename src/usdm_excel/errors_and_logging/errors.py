from .error import Error


class Errors:
    WARNING = Error.WARNING
    ERROR = Error.ERROR
    DEBUG = Error.DEBUG
    INFO = Error.INFO

    def __init__(self):
        self.items = []

    def clear(self):
        self.items = []

    def add(
        self, sheet: str, row: int, column: int, message: str, level: int = Error.ERROR
    ) -> None:
        error = Error(sheet, row, column, message, level)
        self.items.append(error)

    def count(self) -> int:
        return len(self.items)

    def dump(self, level):
        result = []
        for item in self.items:
            if item.level >= level:
                result.append(item.to_dict())
        return result
