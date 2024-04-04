import logging
from datetime import date

class Neo4jDict():

  class LogicError(Exception):
    pass
  
  def __init__(self, study, errors):
    self._errors = errors
    self._study = study
    self._references = {}
    self._logger = logging.getLogger(__name__)

  def clear(self):
    self._references = {}

  def create(self):
    node = self._study
    self._process_node(node)
  
  def get(self, klass, id):
    key = self._key(klass, id)
    if key in self._references:
      return self._references[key]
    else:
      return None
      
  def _process_node(self, node):
    if type(node) == list:
      if node:
        for item in node:
          self._process_node(item) 
    elif type(node) == str:
      pass
    elif type(node) == date:
      pass
    elif type(node) == bool:
      pass
    else:
      key = self._key(node.instanceType, node.id)
      self._references[key] = node
      for name, field in node.model_fields.items():
        self._process_node(field)
  
  def _key(self, klass, id):
    klass_name = self._klass_name(klass)
    return f"{klass_name}.{id}"

  def _klass_name(self, klass):
    return klass if isinstance(klass, str) else klass.__name__
