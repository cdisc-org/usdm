class DocumentBase():

  def __init__(self):
    self.methods = [func for func in dir(self.__class__) if callable(getattr(self.__class__, func)) and not func.startswith("_")]

  def valid_method(self, name):
    return name in self.methods