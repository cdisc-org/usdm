from usdm_model.identifier import ReferenceIdentifier
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.globals import Globals
from usdm_excel.study_identifiers_sheet.organization import get_organization

class StudyReferencesSheet(BaseSheet):

  SHEET_NAME = 'studyReferences'
  
  def __init__(self, file_path, globals: Globals):
    try:
      self.items = []
      self.organizations = []
      super().__init__(file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME, optional=True)
      if self.success:
        self.process_sheet()
    except Exception as e:
      self._sheet_exception(e)
      
  def process_sheet(self):
    self.items = []
    for index, row in self.sheet.iterrows():
      organisation = get_organization(self, index)
      if organisation:
        self.organizations.append(organisation)
        text = self.read_cell_by_name(index, 'studyIdentifier')
        type = self.read_cdisc_klass_attribute_cell_by_name('ReferenceIdentifier', 'type', index, ['referenceType'])     
        item = self.create_object(ReferenceIdentifier, {'text': text, 'type': type, 'scope': organisation})
        if item:
          self.items.append(item)
          self.globals.cross_references.add(item.text, item)         
