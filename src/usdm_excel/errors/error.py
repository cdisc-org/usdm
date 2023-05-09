import logging

class Error():

  ERROR = logging.ERROR
  WARNING = logging.WARNING
  DEBUG = logging.DEBUG
  LABEL = { ERROR: "error", WARNING: "warning", DEBUG: "debug" }

  def __init__(self, sheet: str, row: int, column: int, message: str, level: int=ERROR):
    self.sheet = sheet
    self.row = row
    self.column = column
    self.message = message
    self.level = level

  def to_log(self):
    type = self.__class__.LABEL[self.level].capitalize()  
    if self.sheet == None:
      return f"{type}: {self.message}"
    elif self.row == None:
      return f"{type} in sheet {self.sheet}: {self.message}"
    else:
      return f"{type} in sheet {self.sheet} at [{self.row},{self.column}]: {self.message}"
