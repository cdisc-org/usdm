from usdm_excel.errors_and_logging.errors_and_logging import ErrorsAndLogging
from enum import Enum

class Options(Enum):
  EMPTY_NONE = 'empty_none'
  USDM_VERSION = 'usdm_version'

class EmptyNoneOption(Enum):
  EMPTY = 'empty_string'
  NONE = 'none_value'

class OptionManager():

  def __init__(self, errors_and_logging: ErrorsAndLogging):
    self._errors_and_logging = errors_and_logging
    self._items = {}

  def clear(self):
    self._items = {}

  def set(self, name, value):
    name = self._to_string(name)
    value = self._to_string(value)
    self._items[name] = value

  def get(self, name):
    name = self._to_string(name)
    if name in self._items:
      return self._items[name]
    else:
      return ""
  
  def _to_string(self, item):
    if isinstance(item, Enum):
      return item.value
    else:
      return str(item)
    

