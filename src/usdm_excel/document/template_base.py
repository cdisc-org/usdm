class TemplateBase():

  def __init__(self):
    self.methods = [func for func in dir(self.__class__) if callable(getattr(self.__class__, func)) and not func.startswith("_")]

  def valid_method(self, name):
    return name in self.methods
  
  def _reference(self, item, attribute):
    return f'<usdm:ref klass="{item.__class__.__name__}" id="{item.id}" attribute="{attribute}"></usdm:ref>'

  def _add_checking_for_tag(self, doc, tag, text):
    if text.startswith(f"<{tag}>"):
      doc.asis(text)
    else:
      with doc.tag('p'):
        doc.asis(text)