from usdm_excel.base_sheet import BaseSheet
from usdm_model.narrative_content import NarrativeContent, NarrativeContentItem
from usdm_excel.globals import Globals

class DocumentTemplates():

  def __init__(self, file_path: str, globals: Globals):
    self.items = []
    for sheet_name in globals.template_manager.all():
      self.items.append(DocumentTemplateSheet(file_path, sheet_name, globals))

class DocumentTemplateSheet(BaseSheet):

  def __init__(self, file_path: str, sheet_name: str, globals: Globals):
    try:
      self.items = []
      super().__init__(file_path=file_path, globals=globals, sheet_name=sheet_name, optional=True, converters={"sectionName": str})
      if self.success:
        current_level = 0
        new_level = 0
        current_parent = []
        previous_item = None
        for index, row in self.sheet.iterrows():
          name = self.read_cell_by_name(index, 'name')
          name = f"SECTION {section_number}" if not name else name
          section_number = self.read_cell_by_name(index, 'sectionNumber')
          new_level = self._get_level(section_number)
          title = self.read_cell_by_name(index, 'sectionTitle')
          display_section_number = self.read_boolean_cell_by_name(index, 'displaySectionNumber')
          display_section_title = self.read_boolean_cell_by_name(index, 'displaySectionTitle')
          content_name = self.read_cell_by_name(index, 'content')
          params = {
            'name': name, 
            'sectionNumber': section_number, 
            'displaySectionNumber': display_section_number, 
            'sectionTitle': title, 
            'displaySectionTitle': display_section_title, 
            'contentItemId': self.globals.cross_references.get(NarrativeContentItem, content_name).id
          }
          item = self.create_object(NarrativeContent, params)
          if item:
            self.items.append(item)
            self.globals.cross_references.add(name, item)     
            if new_level == current_level:
              # Same level
              parent = current_parent[-1]
              parent.childIds.append(item.id)
            elif new_level > current_level:
              # Down
              if (new_level - current_level) > 1:
                self._error(index, self._get_column_index('sectionNumber'), f"Error with section number incresing by more than one level, section '{section_number}'.")
                raise BaseSheet.FormatError
              current_parent.append(previous_item)
              current_level = new_level
              parent = current_parent[-1]
              parent.childIds.append(item.id)
            else:
              # Up
              for p_count in range(new_level, current_level):
                popped = current_parent.pop()
              parent = current_parent[-1]
              parent.childIds.append(item.id)
              current_level = new_level
            previous_item = item
          self.double_link(self.items, 'previousId', 'nextId')
    except Exception as e:
      self._sheet_exception(e)

  def _get_level(self, section_number):
    sn = section_number[:-1] if section_number.endswith('.') else section_number
    parts = sn.split('.')
    return len(parts)
