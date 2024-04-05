import logging

class CTVersionManager():

  def __init__(self, logger: logging):
    self._versions = {}
    self._logger = logger

  def clear(self):
    self._versions = {}

  def add(self, name, value):
    self._versions[name] = value

  def get(self, name):
    if name in self._versions:
      return self._versions[name]
    else:
      return "None set"
    

