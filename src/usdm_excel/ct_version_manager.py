class CTVersionManager():

  def __init__(self):
    self.versions = {}

  def clear(self):
    self.versions = {}

  def add(self, name, value):
    self.versions[name] = value

  def get(self, name):
    if name in self.versions:
      return self.versions[name]
    else:
      return "None set"
    
ct_version_manager = CTVersionManager()

