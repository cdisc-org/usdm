from .error import Error
from usdm_excel.logger import package_logger

class Errors():

  def __init__(self):
    self.items = []

  def clear(self):
    self.items = []

  def add(self, sheet: str, row: int, column: int, message: str) -> None:
    error = Error(sheet, row, column, message)
    self.items.append(error)
    package_logger.warning(error.to_log())

  def count(self) -> int:
    return len(self.items)
  
error_manager = Errors()