import traceback
from usdm_excel.errors.errors import error_manager

class CrossRef():

  class PathError(Exception):
    pass

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

  def get_by_path(self, klass, name, path):
    instance = self.get(klass, name)
    if instance:
      parts = path.split("/")
      attribute = parts[0].replace('@', '')  
      if len(parts) == 1:
        return instance, attribute
      elif len(parts) % 2 == 1:
        for index in range(1,len(parts),2):
          try:
            instance = getattr(instance, attribute)
          except AttributeError as e:
            raise self.PathError(f"Failed to translate reference path '{path}', attribute '{attribute}' was not found")
          attribute = parts[index+1].replace('@', '')
          if not parts[index] == instance.__class__.__name__:
            raise self.PathError(f"Failed to translate reference path '{path}', class mismtach, expecting '{parts[index]}', found '{instance.__class__.__name__}'")
        if instance and attribute:
          if not cross_references.get_by_id(instance.__class__, instance.id):
            cross_references.add(instance.id, instance)
          return instance, attribute
        else:
          raise self.PathError(f"Failed to translate reference path '{path}', path was not found")
      else:
        raise self.PathError(f"Failed to translate reference path '{path}', format error")
    else:
      raise self.PathError(f"Failed to translate reference path '{path}', could not find start instance '{klass}', '{name}'")

  def _key(self, klass, name, id):
    klass_name = self._klass_name(klass)
    return f"{klass_name}.{name}", f"{klass_name}.{id}"

  def _klass_name(self, klass):
    return klass if isinstance(klass, str) else klass.__name__

cross_references = CrossRef()