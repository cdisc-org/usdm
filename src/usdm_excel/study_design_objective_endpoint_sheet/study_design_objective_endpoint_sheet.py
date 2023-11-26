from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
from usdm_model.objective import Objective
from usdm_model.endpoint import Endpoint
from usdm_model.syntax_template_dictionary import SyntaxTemplateDictionary

import traceback
import re

class StudyDesignObjectiveEndpointSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesignOE')
      self.objectives = []
      current = None
      for index, row in self.sheet.iterrows():
        o_text = self.read_cell_by_name(index, 'objectiveText') 
        ep_name = self.read_cell_by_name(index, ['endpointXref', 'endpointName'])
        ep_description = self.read_cell_by_name(index, 'endpointDescription')
        ep_label = self.read_cell_by_name(index, ["endpointLabel"], must_be_present=False) 
        ep_text = self.read_cell_by_name(index, 'endpointText') 
        ep_purpose = self.read_cell_by_name(index, ['endpointPurposeDescription', 'endpointPurpose'], default='None provided')
        ep_level = self.read_cdisc_klass_attribute_cell_by_name('Endpoint', 'endpointLevel', index, "endpointLevel")
        ep_dictionary_name = self.read_cell_by_name(index, 'endpointDictionary', must_be_present=False)
        self._validate_references(index, 'endpointText', ep_text, ep_dictionary_name)

        if o_text:
          o_name = self.read_cell_by_name(index, ["objectiveXref", "objectiveName"]) 
          o_description = self.read_cell_by_name(index, 'objectiveDescription')
          o_label = self.read_cell_by_name(index, ["objectiveLabel"], must_be_present=False) 
          o_level = self.read_cdisc_klass_attribute_cell_by_name('Objective', 'objectiveLevel', index, "objectiveLevel")
          o_dictionary_name = self.read_cell_by_name(index, 'objectiveDictionary', must_be_present=False)
          self._validate_references(index, 'objectiveText', o_text, o_dictionary_name)
          try:
            dictionary_id = self._get_dictionary_id(o_dictionary_name)
            current = Objective(id=id_manager.build_id(Objective),
              instanceType="OBJECTIVE",
              name=o_name,
              description=o_description, 
              label=o_label,
              text=o_text,
              level=o_level,
              endpoints=[],
              dictionaryId=dictionary_id
            )
          except Exception as e:
            self._general_error(f"Failed to create Objective object, exception {e}")
            self._traceback(f"{traceback.format_exc()}")
          else:
            self.objectives.append(current)
            cross_references.add(o_name, current)
        if current is not None:
          try:
            dictionary_id = self._get_dictionary_id(ep_dictionary_name)
            ep = Endpoint(id=id_manager.build_id(Endpoint),
              instanceType="ENDPOINT",
              name=ep_name,
              description=ep_description,
              label=ep_label,
              text=ep_text, 
              purpose=ep_purpose, 
              level=ep_level,
              dictionaryId=dictionary_id
            )  
          except Exception as e:
            self._general_error(f"Failed to create Endpoint object, exception {e}")
            self._traceback(f"{traceback.format_exc()}")
          else:
            current.endpoints.append(ep)
            cross_references.add(ep_name, ep)
        else:
          self._general_error("Failed to add Endpoint, no Objective set")

    except Exception as e:
      self._general_error(f"Exception '{e}' raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

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
