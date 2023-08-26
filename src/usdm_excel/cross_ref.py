class CrossRef():

  def __init__(self):
    self.references = {}
    self.identifiers = {}

  def clear(self):
    self.references = {}
    self.identifiers = {}

  def add(self, name, object):
    klass = object.__class__
    key, id_key = self._key(klass, name, object.id)
    if not key in self.references:
      self.references[key] = object
      self.identifiers[id_key] = object
    else:
      pass # Need exception here

  def get(self, klass, name):
    key, id_key = self._key(klass, name, "")
    if key in self.references:
      return self.references[key]
    else:
      return None

  def get_by_id(self, klass, id):
    key, id_key = self._key(klass, "", id)
    if id_key in self.identifiers:
      return self.identifiers[id_key]
    else:
      return None

  def _key(self, klass, name, id):
    if isinstance(klass, str):
      key = f"{klass}.{name}" 
      id_key = f"{klass}.{id}"
    else:
      key = f"{klass.__name__}.{name}"
      id_key = f"{klass.__name__}.{id}"
    return key, id_key
  
cross_references = CrossRef()