class CrossRef():

  def __init__(self):
    self.references = {}

  def clear(self):
    self.references = {}

  def add(self, key, value):
    if not key in self.references:
      self.references[key] = value
    else:
      pass # Need exception here

  def get(self, key):
    if key in self.references:
      return self.references[key]
    else:
      return None

cross_references = CrossRef()