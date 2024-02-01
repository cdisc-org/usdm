from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_model.syntax_template_dictionary import SyntaxTemplateDictionary

import traceback

class StudyDesignDictionarySheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='dictionaries', optional=True)
      self.items = []
      if self.success:
        current_name = None
        current_dictionary = None
        current_map = {}
        for index, row in self.sheet.iterrows():
          name = self.read_cell_by_name(index, 'name')
          if name:
            if name != current_name:
              current_name = name
              if current_dictionary:
                current_dictionary.parameterMap = current_map
                current_map = {}
              description = self.read_cell_by_name(index, 'description')
              label = self.read_cell_by_name(index, 'label')
              current_dictionary = self._dictionary(name, description, label)
          key = self.read_cell_by_name(index, 'key')
          klass = self.read_cell_by_name(index, 'class')
          xref_name = self.read_cell_by_name(index, 'xref')
          attribute_path = self.read_cell_by_name(index, ['attribute', 'path'])
          #item = cross_references.get(klass, xref_name)
          #if item:
            # instance, attribute = self._process_path(index, col, item, attribute_path)
          instance = None
          try:
            instance, attribute = cross_references.get_by_path(klass, xref_name, attribute_path)
          except Exception as e:
            col = self.column_present(['attribute', 'path'])
            self._error(index, col, str(e))
          if instance:
            current_map[key] = {'klass': instance.__class__.__name__, 'id': instance.id, 'attribute': attribute}
          #else:
          #  self._warning(index, col, f"Unable to resolve dictionary reference klass: '{klass}', name: '{xref_name}', attribute: '{attribute_path}'")
        # Clean up last dictionary if present
        if current_dictionary:
          current_dictionary.parameterMap = current_map
        
    except Exception as e:
      self._general_error(f"Exception '{e}' raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

  def _dictionary(self, name, description, label):
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
      return None
    else:
      self.items.append(item)
      cross_references.add(name, item)
      return item

  # def _process_path(self, row, col, instance, path):
  #   try:
  #     parts = path.split("/")
  #     attribute = parts[0].replace('@', '')  
  #     if len(parts) == 1:
  #       return instance, attribute
  #     elif len(parts) % 2 == 1:
  #       for index in range(1,len(parts),2):
  #         instance = getattr(instance, attribute)
  #         attribute = parts[index+1].replace('@', '')
  #       if instance and attribute:
  #         if not cross_references.get_by_id(instance.__class__, instance.id):
  #           cross_references.add(instance.id, instance)
  #         return instance, attribute
  #       else:
  #         self._error(row, col, f"Failed to translate reference path, not found '{path}'. Ignoring value")
  #         return None, None
  #     else:
  #       self._error(row, col, f"Failed to translate reference path, format '{path}'. Ignoring value")
  #       return None, None
  #   except Exception as e:
  #     self._error(row, col, f"Exception raised translating reference path '{path}'\n{traceback.format_exc()}")
  #     return None, None
