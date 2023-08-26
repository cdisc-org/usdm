class CrossRef():

  def __init__(self):
    self.references = {}

  def clear(self):
    self.references = {}

  def add(self, name, object):
    klass = object.__class__
    key = self._key(klass, name)
    if not key in self.references:
      self.references[key] = object
    else:
      pass # Need exception here

  def get(self, klass, name):
    key = self._key(klass, name)
    if key in self.references:
      return self.references[key]
    else:
      return None

  def _key(self, klass, name):
    key = f"{klass.__name__}.{name}"
    return key
  
cross_references = CrossRef()