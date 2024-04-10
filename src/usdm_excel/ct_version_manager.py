from usdm_excel.errors_and_logging.errors_and_logging import ErrorsAndLogging

class CTVersionManager():

  def __init__(self, errors_and_logging: ErrorsAndLogging):
    self._errors_and_logging = errors_and_logging
    self._versions = {}


  def clear(self):
    self._versions = {}

  def add(self, name, value):
    self._versions[name] = value

  def get(self, name):
    if name in self._versions:
      return self._versions[name]
    else:
      return "None set"
    

