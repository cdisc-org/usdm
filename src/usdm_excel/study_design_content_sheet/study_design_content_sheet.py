from usdm_excel.base_sheet import BaseSheet
from usdm_excel.option_manager import Options
from usdm_model.narrative_content import NarrativeContent
from usdm_excel.globals import Globals
from usdm_excel.document.macros import Macros

class StudyDesignContentSheet(BaseSheet):

  #SHEET_NAME = 'studyDesignContent'

  def __init__(self, file_path: str, globals: Globals):
    try:
      self.items = []
      template = globals.option_manager.get(Options.USE_TEMPLATE)
      sheet_name = globals.template_manager.get(template)
      globals.errors_and_logging.info(f"About to read content sheet '{sheet_name}' based on template '{template}'")  
      print(f"TEMPLATE: {template}")
      print(f"SHEET NAME: {template}")
      super().__init__(file_path=file_path, globals=globals, sheet_name=sheet_name, optional=True, converters={"sectionName": str})
      if self.success:
        current_level = 0
        new_level = 0
        current_parent = []
        previous_item = NarrativeContent(
          id=self.globals.id_manager.build_id(NarrativeContent), 
          name="ROOT",
          sectionNumber="0",
          sectionTitle="Root",
          text="",
          childIds=[]
        )
        self.items.append(previous_item)
        for index, row in self.sheet.iterrows():
          section_number = self.read_cell_by_name(index, 'sectionNumber')
          new_level = self._get_level(section_number)
          title = self.read_cell_by_name(index, 'sectionTitle')
          text = self.read_cell_by_name(index, 'text')
          name = self.read_cell_by_name(index, 'name')
          name = f"SECTION {section_number}" if not name else name
          try:
            item = NarrativeContent(
              id=self.globals.id_manager.build_id(NarrativeContent), 
              name=name,
              sectionNumber=section_number,
              sectionTitle=title,
              text=self._wrap_div(text),
              childIds=[]
            )
          except Exception as e:  
            self._general_exception(f"Failed to create Content object", e)
          else:
            self.items.append(item)
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

  def resolve(self, study):
    macros = Macros(self, study)
    for item in self.items:
      item.text = macros.resolve(item.text)

  def _get_level(self, section_number):
    sn = section_number[:-1] if section_number.endswith('.') else section_number
    parts = sn.split('.')
    return len(parts)

  def _wrap_div(self, text):
    return text if text.startswith("<div>") else f"<div>{text}</div>"
  
