from usdm_excel.errors_and_logging.errors_and_logging import ErrorsAndLogging


class BaseManager:
    def __init__(self, errors_and_logging: ErrorsAndLogging):
        self._errors_and_logging = errors_and_logging
        self._items = {}

    def __iter__(self):
        return iter(self._items)

    def clear(self) -> None:
        self._items = {}

    def add(self, name: str, value: str) -> None:
        self._items[name.upper()] = value

    def get(self, name: str) -> str:
        u_name = name.upper()
        return self._items[u_name] if u_name in self._items else ""

    def includes(self, name) -> bool:
        u_name = name.upper()
        return u_name in self._items

    # def all(self) -> list:
    #   return list(self._items.values())

    def items(self):
        return self._items.items()

    def keys(self):
        return self._items.keys()

    def values(self):
        return self._items.values()
