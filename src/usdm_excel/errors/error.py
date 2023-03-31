class Error():

  def __init__(self, sheet: str, row: int, column: int, message: str):
    self.sheet = sheet
    self.row = row
    self.column = column
    self.message = message
