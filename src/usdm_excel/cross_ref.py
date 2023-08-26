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
    print(f"CR GBI 1: klass={klass} id={id}")
    key, id_key = self._key(klass, "", id)
    print(f"CR GBI 2: id key={id_key}")
    if id_key in self.identifiers:
      return self.identifiers[id_key]
    else:
      print(f"CR GBI 3: {self.identifiers}")
      return None

  def _key(self, klass, name, id):
    print(f"CR K 1:")
    key = f"{klass}.{name}" if isinstance(klass, str) else f"{klass.__name__}.{name}"
    print(f"CR K 2: {key}")
    id_key = f"{klass.__name__}.{id}"
    return key, id_key
  
cross_references = CrossRef()