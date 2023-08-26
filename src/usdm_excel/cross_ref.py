class CrossRef():

  def __init__(self):
    self.references = {}

  def clear(self):
    self.references = {}

  def add(self, name, object):
    klass = object.__class__
    key = self._key(klass, name)
    if not key in self.references:
      print(f"CR: Adding {key}")
      self.references[key] = object
    else:
      pass # Need exception here

  def get(self, klass, name):
    key = self._key(klass, name)
    if key in self.references:
      print(f"CR: Get {key} OK")
      return self.references[key]
    else:
      print(f"CR: Get {key} failed")
      return None

  def _key(self, klass, name):
    return f"{klass.__name__}.{name}"
  
cross_references = CrossRef()