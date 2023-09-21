class Conditons():

  def __init__(self, conditon_info):
    self.items = []
    self.errors = []
    if conditon_info:
      parts = conditon_info.split(",")
      for part in parts:
        name_value = part.split(":")
        if len(name_value) == 2:
          self.items.append({'name': name_value[0], 'condition': name_value[1]})
        else:
          self.errors.append(f"Could not decode a condition, no ':' foundin '{part}'")
    else:
      pass # Empty, this is OK
