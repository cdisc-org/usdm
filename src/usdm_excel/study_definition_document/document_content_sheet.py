from usdm_excel.base_sheet import BaseSheet
from usdm_model.narrative_content import NarrativeContentItem
from usdm_excel.globals import Globals
from usdm_excel.document.macros import Macros

class DocumentContentSheet(BaseSheet):

  SHEET_NAME = 'documentContent'
  DIV_OPEN_NS = '<div xmlns="http://www.w3.org/1999/xhtml">'
  DIV_OPEN = '<div>'
  DIV_CLOSE = '</div>'

  def __init__(self, file_path: str, globals: Globals):
    try:
      self.items = []
      super().__init__(file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME, optional=True)
      if self.success:
        for index, row in self.sheet.iterrows():
          text = self.read_cell_by_name(index, 'text')
          name = self.read_cell_by_name(index, 'name')
          item = self.create_object(NarrativeContentItem, {'name': name, 'text': self._wrap_div(text)})
          if item:
            self.items.append(item)
            self.globals.cross_references.add(name, item)     
    except Exception as e:
      self._sheet_exception(e)

  def resolve(self, study):
    macros = Macros(self, study)
    for item in self.items:
      item.text = macros.resolve(item.text)

  def _wrap_div(self, text):
    if text.startswith(self.DIV_OPEN_NS):
      return text
    elif text.startswith(self.DIV_OPEN):
      return text.replace(self.DIV_OPEN, self.DIV_OPEN_NS)
    else:
      return f'{self.DIV_OPEN_NS}{text}{self.DIV_CLOSE}'
  
