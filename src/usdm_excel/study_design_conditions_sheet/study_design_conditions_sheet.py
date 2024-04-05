import traceback
from usdm_excel.base_sheet import BaseSheet
#from usdm_excel.cross_ref import cross_references
from usdm_model.condition import Condition

class StudyDesignConditionSheet(BaseSheet):

  def __init__(self, file_path, manager):
    try:
      super().__init__(file_path=file_path, manager=manager, sheet_name='studyDesignConditions', optional=True)
      self.items = []
      if self.success:
        for index, row in self.sheet.iterrows():
          name = self.read_cell_by_name(index, 'name')
          description = self.read_cell_by_name(index, 'description')
          label = self.read_cell_by_name(index, 'label')
          text = self.read_cell_by_name(index, 'text')
          context = self.read_cell_by_name(index, 'context')
          context_refs = self._process_context_references(context, index)
          applies_to = self.read_cell_by_name(index, 'appliesTo')
          applies_refs = self._process_applies_to_references(applies_to, index)
          params = {'name': name, 'description': description, 'label': label, 'text': text, 'appliesToIds': applies_refs, 'contextIds': context_refs}
          item = self.create_object(Condition, params)
          if item:
            self.items.append(item)
            self.managers.cross_references.add(name, item)     
    except Exception as e:
      self._general_error(f"Exception '{e}' raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

  def _process_context_references(self, references_list, index):
    return self._process_references(references_list, ['ScheduledActivityInstance', 'Activity'], index, 'context', False)
  
  def _process_applies_to_references(self, references_list, index):
    return self._process_references(references_list, ['Procedure', 'Activity', 'BiomedicalConcept', 'BiomedicalConceotCategory', 'BiomedicalConceptSurrogate'], index, 'appliesTo')
  
  def _process_references(self, references_list, klasses, index, column_name, references_required=True):
    references = [x.strip() for x in references_list.split(',')]
    results = []
    for reference in references:
      if reference:
        found = False
        for klass in klasses:
          xref = self.managers.cross_references.get(klass, reference)
          if xref:
            results.append(xref.id)
            found = True
            break
        if not found:
          self._error(index, self._get_column_index(column_name), f"Could not resolve condition reference '{reference}'")
    if not results and references_required:
      self._error(index, self._get_column_index(column_name), f"No condition references found for '{references_list}', at least one required")
    return results
