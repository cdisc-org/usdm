from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_model.eligibility_criteria import EligibilityCriteria
from usdm_model.syntax_template_dictionary import SyntaxTemplateDictionary

import traceback
import re

class StudyDesignEligibilityCriteriaSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesignEligibilityCriteria', optional=True)
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
          criteria = self._criteria(name, description, label, text, category, identifier, dictionary_name)
          if criteria:
            self.items.append(criteria)
        
    except Exception as e:
      self._general_error(f"Exception '{e}' raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

  def _criteria(self, name, description, label, text, category, identifier, dictionary_name):
    try:
      dictionary_id = self._get_dictionary_id(dictionary_name)
      # dictionary = cross_references.get(SyntaxTemplateDictionary, dictionary_name)
      # if dictionary:
      #   dictionary_id = dictionary.id
      # else:
      #   self._general_error(f"Unable to find dictionary with name '{dictionary_name}'")
      #   dictionary_id = None
      item = EligibilityCriteria(
        id=id_manager.build_id(EligibilityCriteria),
        name=name,
        description=description,
        label=label,
        text=text,
        category=category,
        identifier=identifier,
        dictionaryId=dictionary_id
      )
    except Exception as e:
      self._general_error(f"Failed to create EligibilityCriteria object, exception {e}")
      self._traceback(f"{traceback.format_exc()}")
      return None
    else:
      cross_references.add(item.id, item)
      return item

  def _validate_references(self, row, column_name, text, dictionary_name):
    if dictionary_name:
      column = self.column_present(column_name)
      dictionary = cross_references.get(SyntaxTemplateDictionary, dictionary_name)
      if not dictionary:
        self._warning(row, column, f"Dictionary '{dictionary_name}' not found")
        return
      tags = re.findall(r'\[([^]]*)\]',text)
      for tag in tags:
        if not tag in dictionary.parameterMap:
          self._warning(row, column, f"Failed to find '{tag}' in dictionary '{dictionary_name}'")
  
  def _get_dictionary_id(self, dictionary_name):
    if dictionary_name:
      dictionary = cross_references.get(SyntaxTemplateDictionary, dictionary_name)
      if dictionary:
        return dictionary.id
      else:
        self._general_error(f"Unable to find dictionary with name '{dictionary_name}'")
    return None
