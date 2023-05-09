from .error import Error
from usdm_excel.logger import package_logger

class Errors():

  WARNING = Error.WARNING
  ERROR = Error.ERROR
  DEBUG = Error.DEBUG

  def __init__(self):
    self.items = []

  def clear(self):
    self.items = []

  def add(self, sheet: str, row: int, column: int, message: str, level: int=Error.ERROR) -> None:
    error = Error(sheet, row, column, message, level)
    self.items.append(error)      
    package_logger.log(level, error.to_log())

  def count(self) -> int:
    return len(self.items)
  
  def dump(self):
    result = []
    for item in self.items:
      result.append(item.__dict__)
    return result

error_manager = Errors()