from usdm_excel.base_sheet import BaseSheet
from usdm_model.assigned_person import AssignedPerson
from usdm_model.organization import Organization
from usdm_model.masking import Masking
from usdm_excel.globals import Globals

class StudyRoleSheet(BaseSheet):

  SHEET_NAME = 'roles'

  def __init__(self, file_path: str, globals: Globals):
    try:
      self.items = []
      super().__init__(file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME, optional=True)
      if self.success:
        for index, row in self.sheet.iterrows():
          name = self.read_cell_by_name(index, 'name')
          description = self.read_cell_by_name(index, 'description', default='')
          label = self.read_cell_by_name(index, 'label', default='')
          masking = self._get_masking(index)
          people = self._get_refs_for(AssignedPerson, index, 'people')
          orgs = self._get_refs_for(Organization, index, 'organizations')
          params = {'name': name, 'descriptiopn': description, 'label': label, 'organizations': orgs, 'assignedPersons': people, 'masking': masking}
          item = self.create_object(AssignedPerson, params)
          if item:
            self.items.append(item)
            self.globals.cross_references.add(name, item)     
    except Exception as e:
      self._sheet_exception(e)

  def _get_masking(self, index):
    masking = None
    masking_text = self.read_cell_by_name(index, 'masking', default='')
    if masking_text:
      masking = self.create_object(Masking, {'description': masking_text})
    return masking
  
  def _get_refs_for(self, klass, index: int, column_name: str):
    collection = []
    refs = self.read_cell_multiple_by_name(index, column_name, must_be_present=False)
    for ref in refs:
      item = self.globals.cross_references.get(klass, ref)
      if item:
        collection.append(item.id)
      else:
        self._warning(index, column_name, f"Failed to find {klass.__name__.lower()} with name '{ref}'")