from enum import Enum

class Options(Enum):
  PREVIOUS_NEXT = 1
  ROOT = 2

class PrevNextOption(Enum):
  NULL_STRING = 1
  NONE = 2

class RootOption(Enum):
  SDR_COMPATABLE = 1
  API_COMPLIANT = 2

class OptionManager():

  def __init__(self):
    self.items = {}

  def clear(self):
    self.items = {}

  def set(self, name, value):
    self.items[name] = value

  def get(self, name):
    if name in self.items:
      return self.items[name]
    else:
      return ""
    
option_manager = OptionManager()

