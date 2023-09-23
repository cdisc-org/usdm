from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_model.content import Content
from usdm_excel.option_manager import Options, option_manager
import traceback

class StudyDesignContentSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      self.items = []
      super().__init__(file_path=file_path, sheet_name='studyDesignContent', optional=True, converters={"sectionName": str})
      if self.success:
        current_level = 0
        new_level = 0
        current_parent = []
        previous_item = Content(
          id=id_manager.build_id(Content), 
          name="ROOT",
          sectionNumber="0",
          sectionTitle="Root",
          text="",
          contentChildIds=[]
        )
        self.items.append(previous_item)
        for index, row in self.sheet.iterrows():
          section_number = self.read_cell_by_name(index, 'sectionNumber')
          new_level = self._get_level(section_number)
          title = self.read_cell_by_name(index, 'sectionTitle')
          text = self.read_cell_by_name(index, 'text')
          name = self.read_cell_by_name(index, 'name')
          name = f"SECTION {section_number}" if name == "" else name
          try:
            item = Content(
              id=id_manager.build_id(Content), 
              name=name,
              sectionNumber=section_number,
              sectionTitle=title,
              text=text,
              contentChildIds=[]
            )
          except Exception as e:  
            self._general_error(f"Failed to create Content object, exception {e}")
            self._traceback(f"{traceback.format_exc()}")
          self.items.append(item)
          #print(f"ITEM: {item.id}")
          if new_level == current_level:
            # Same level
            parent = current_parent[-1]
            parent.contentChildIds.append(item.id)
          elif new_level > current_level:
            # Down
            if (new_level - current_level) > 1:
              self._error(index, self._get_column_index('sectionNumber'), f"Error with section number incresing by more than one level, section '{section_number}'.")
              raise BaseSheet.FormatError
            current_parent.append(previous_item)
            current_level = new_level
            parent = current_parent[-1]
            parent.contentChildIds.append(item.id)
          else:
            # Up
            for p_count in range(new_level, current_level):
              popped = current_parent.pop()
            parent = current_parent[-1]
            parent.contentChildIds.append(item.id)
            current_level = new_level
          previous_item = item
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

  def _get_level(self, section_number):
    parts = section_number.split('.')
    return len(parts)