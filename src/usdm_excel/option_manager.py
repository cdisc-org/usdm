from enum import Enum

class Options(Enum):
  PREVIOUS_NEXT = 'previous'
  ROOT = 'root'
  DESCRIPTION = 'description'

class PrevNextOption(Enum):
  NULL_STRING = 'null_string'
  NONE = 'none'

class RootOption(Enum):
  SDR_COMPATABLE = 'sdr_compatable'
  API_COMPLIANT = 'api_compliant'

class OptionManager():

  def __init__(self):
    self.items = {}

  def clear(self):
    self.items = {}

  def set(self, name, value):
    name = self._to_string(name)
    value = self._to_string(value)
    self.items[name] = value

  def get(self, name):
    name = self._to_string(name)
    if name in self.items:
      return self.items[name]
    else:
      return ""
  
  def _to_string(self, item):
    if isinstance(item, Enum):
      return item.value
    else:
      return str(item)
    
option_manager = OptionManager()

