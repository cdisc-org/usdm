def usdm_reference(item, attribute):
  return f'<usdm:ref klass="{item.__class__.__name__}" id="{item.id}" attribute="{attribute}"></usdm:ref>'
