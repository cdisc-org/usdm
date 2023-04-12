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
    self.versions = {}

  def clear(self):
    self.versions = {}

  def set(self, name, value):
    self.versions[name] = value

  def get(self, name):
    if name in self.versions:
      return self.versions[name]
    else:
      return ""
    
option_manager = OptionManager()

