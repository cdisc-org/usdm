import re
import traceback
from usdm_excel.base_sheet import BaseSheet
from usdm_model.code import Code
from usdm_model.eligibility_criterion import EligibilityCriterion
from usdm_model.syntax_template_dictionary import SyntaxTemplateDictionary
from usdm_excel.globals import Globals

class StudyDesignEligibilityCriteriaSheet(BaseSheet):

  SHEET_NAME = 'studyDesignEligibilityCriteria'
  
  def __init__(self, file_path: str, globals: Globals):
    try:
      super().__init__(file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME, optional=True)
      self.items = []
      if self.success:
        for index, row in self.sheet.iterrows():
          category = self.read_cdisc_klass_attribute_cell_by_name('EligibilityCriteria', 'category', index, 'category')
          identifier = self.read_cell_by_name(index, 'identifier')
          name = self.read_cell_by_name(index, 'name')
          description = self.read_cell_by_name(index, 'description')
          label = self.read_cell_by_name(index, 'label')
          text = self.read_cell_by_name(index, 'text')
          dictionary_name = self.read_cell_by_name(index, 'dictionary')
          self._validate_references(index, 'text', text, dictionary_name)
          item = self._criteria(name, description, label, text, category, identifier, dictionary_name)
          if item:
            self.globals.cross_references.add(item.name, item)
            self.items.append(item)
    except Exception as e:
      self._sheet_exception(e)

  def _criteria(self, name: str, description: str, label: str, text: str, category: Code, identifier: str, dictionary_name: str) -> EligibilityCriterion:
    dictionary_id = self._get_dictionary_id(dictionary_name)
    params = {'name': name, 'description': description, 'label': label, 'text': text, 'category': category, 'identifier': identifier, 'dictionaryId': dictionary_id}
    return self.create_object(EligibilityCriterion, params)

  def _validate_references(self, row: int, column_name: str, text: str, dictionary_name: str) -> None:
    if dictionary_name:
      column = self.column_present(column_name)
      dictionary = self.globals.cross_references.get(SyntaxTemplateDictionary, dictionary_name)
      if not dictionary:
        self._warning(row, column, f"Dictionary '{dictionary_name}' not found")
        return
      tags = re.findall(r'\[([^]]*)\]',text)
      for tag in tags:
        entry = next((item for item in dictionary.parameterMaps if item.tag == tag), None)
        if not entry:
        #if not tag in dictionary.parameterMap:
          self._warning(row, column, f"Failed to find '{tag}' in dictionary '{dictionary_name}'")
  
  def _get_dictionary_id(self, dictionary_name: str) -> str:
    if dictionary_name:
      dictionary = self.globals.cross_references.get(SyntaxTemplateDictionary, dictionary_name)
      if dictionary:
        return dictionary.id
      else:
        self._general_error(f"Unable to find dictionary with name '{dictionary_name}'")
    return None
