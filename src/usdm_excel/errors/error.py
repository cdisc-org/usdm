class Error():

  def __init__(self, sheet: str, row: int, column: int, message: str):
    self.sheet = sheet
    self.row = row
    self.column = column
    self.message = message

  def to_log(self):
    return "Warning in sheet %s at [%s,%s]: %s" % (self.sheet, self.row, self.column, self.message)