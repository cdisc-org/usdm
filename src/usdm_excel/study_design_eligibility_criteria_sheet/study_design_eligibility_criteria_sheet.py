from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_model.eligibility_criteria import EligibilityCriteria
from usdm_model.syntax_template_dictionary import SyntaxTemplateDictionary

import traceback

class StudyDesignEligibilityCriteriaSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='StudyDesignEligibilityCriteria', optional=True)
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
          criteria = self._criteria(name, description, label, text, category, identifier, dictionary_name)
          self.items.append(criteria)
        
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

  def _criteria(self, name, description, label, text, category, identifier, dictionary_name):
    try:
      dictionary = cross_references.get(SyntaxTemplateDictionary, dictionary_name)
      if not dictionary:
        self._general_warning(f"Dictionary '{dictionary_name}' not found")
      item = EligibilityCriteria(
        id=id_manager.build_id(EligibilityCriteria),
        instanceType='ELIGIBILITY_CRITERIA', 
        name=name,
        description=description,
        label=label,
        text=text,
        category=category,
        identifier=identifier,
        dictionary=dictionary
      )
    except Exception as e:
      self._general_error(f"Failed to create EligibilityCriteria object, exception {e}")
      self._traceback(f"{traceback.format_exc()}")
      return None
    else:
      return item
