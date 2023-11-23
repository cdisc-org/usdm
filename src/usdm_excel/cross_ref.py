from usdm_excel.errors.errors import error_manager

class CrossRef():

  def __init__(self):
    self.references = {}
    self.identifiers = {}

  def clear(self):
    self.references = {}
    self.identifiers = {}

  def add(self, name, object):
    klass = object.__class__
    try:
      key, id_key = self._key(klass, name, object.id)
      if not key in self.references:
        self.references[key] = object
        self.identifiers[id_key] = object
      else:
        error_manager.add(None, None, None, f"Duplicate cross reference detected, class '{self._klass_name(klass)}' with name '{name}'")
    except Exception as e:
      error_manager.add(None, None, None, f"Failed to add cross reference detected, class '{self._klass_name(klass)}' with name '{name}'. Exception {e}")

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
    klass_name = self._klass_name(klass)
    return f"{klass_name}.{name}", f"{klass_name}.{id}"

  def _klass_name(self, klass):
    return klass if isinstance(klass, str) else klass.__name__

cross_references = CrossRef()