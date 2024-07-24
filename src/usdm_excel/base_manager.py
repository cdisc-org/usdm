from usdm_excel.errors_and_logging.errors_and_logging import ErrorsAndLogging

class BaseManager():

  def __init__(self, errors_and_logging: ErrorsAndLogging):
    self._errors_and_logging = errors_and_logging
    self._items = {}

  def clear(self):
    self._items = {}

  def add(self, name, value):
    self._items[name.upper()] = value

  def get(self, name):
    u_name = name.upper()
    return self._items[u_name] if u_name in self._items else ''
  
  def all(self):
    return list(self._items.values())
