from usdm_model.identifier import StudyIdentifier
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.globals import Globals
from usdm_excel.study_identifiers_sheet.organization import get_organization

class StudyIdentifiersSheet(BaseSheet):

  SHEET_NAME = 'studyIdentifiers'
  
  def __init__(self, file_path, globals: Globals):
    try:
      self.identifiers = []
      super().__init__(file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME)
      self.process_sheet()
    except Exception as e:
      self._sheet_exception(e)
      
  def process_sheet(self):
    self.identifiers = []
    for index, row in self.sheet.iterrows():
      organisation = get_organization(self, index)
      if organisation:
        item = self.create_object(StudyIdentifier, {'text': self.read_cell_by_name(index, 'studyIdentifier'), 'scope': organisation})
        if item:
          self.identifiers.append(item)
          self.globals.cross_references.add(item.text, item)         
