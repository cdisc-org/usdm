from .error import Error

class Errors():

  def __init__(self):
    self.items = []

  def add(self, sheet: str, row: int, column: int, message: str) -> None:
    self.items.append(Error(sheet, row, column, message))