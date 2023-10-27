from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_model.syntax_template_dictionary import SyntaxTemplateDictionary

import traceback

class StudyDesignDictionarySheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='dictionaries', optional=True)
      self.items = []
      if self.success:
        print(f"INIT1:")
        current_name = None
        current_dictionary = None
        current_map = {}
        for index, row in self.sheet.iterrows():
          name = self.read_cell_by_name(index, 'name')
          print(f"INIT2: {name}")
          if name:
            if name != current_name:
              current_name = name
              if current_dictionary:
                print(f"INIT3:")
                current_dictionary.parameterMap = current_map
                current_map = {}
              description = self.read_cell_by_name(index, 'description')
              label = self.read_cell_by_name(index, 'label')
              print(f"INIT4: {description}, {label}")
              current_dictionary = self._dictionary(name, description, label)
              self.items.append(current_dictionary)
          key = self.read_cell_by_name(index, 'key')
          klass = self.read_cell_by_name(index, 'class')
          xref_name = self.read_cell_by_name(index, 'xref_or_name')
          attribute = self.read_cell_by_name(index, 'attribute')
          current_map[key] = {'klass': klass, 'id': xref_name, 'attribute': attribute}
      current_dictionary.parameterMap = current_map
        
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

  def _dictionary(self, name, description, label):
    print(f"DICT1: {name}, {description}, {label}")
    try:
      item = SyntaxTemplateDictionary(
        id=id_manager.build_id(SyntaxTemplateDictionary), 
        name=name,
        description=description,
        label=label,
        parameterMap={}
      )
    except Exception as e:
      self._general_error(f"Failed to create SyntaxTemplateDictionary object, exception {e}")
      self._traceback(f"{traceback.format_exc()}")
      print(f"DICT2: {traceback.format_exc()}")
      return None
    else:
      return item

