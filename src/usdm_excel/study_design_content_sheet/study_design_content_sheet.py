from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
import traceback
from usdm_model.content import Content

class StudyDesignContentSheet(BaseSheet):

  SECTION_LEVELS = 3

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesignContent')
      self.items = []
      current_level = 0
      new_level = 0
      current_parent = []
      previous_item = Content(
        id="DUMMY", 
        name="ROOT",
        sectionNumber="0",
        sectionTitle="Top Level",
        text="",
        contentChildIds=[]
      )
      first_level = 1 
      last_level = self.__class__.SECTION_LEVELS + 1
      for index, row in self.sheet.iterrows():
        for level in range(first_level, last_level):
          number = str(self.read_cell_by_name(index, f"sectionNumber{level}"))
          if number != "":
            new_level = level
            break
        title = self.read_cell_by_name(index, 'sectionTitle')
        text = self.read_cell_by_name(index, 'text')
        name = self.read_cell_by_name(index, 'name')
        name = f"SECTION {number}" if name == "" else name
        #print(f"PARAMS: New={new_level}, Current={current_level}, Num={number}, Title={title}, Text={text}, Name={name}")
        try:
          item = Content(
            id=id_manager.build_id(Content), 
            name=name,
            sectionNumber=number,
            sectionTitle=title,
            text=text,
            contentChildIds=[]
          )
          self.items.append(item)
          #print(f"ITEM: {item}")
          if new_level == current_level:
            # Same level
            parent = current_parent[-1]
            #print(f"PARENT1: P={parent.id}, C={item.id}")
            parent.contentChildIds.append(item.id)
          elif new_level > current_level:
            # Down
            current_parent.append(previous_item)
            current_level = new_level
            parent = current_parent[-1]
            #print(f"PARENT2: P={parent.id}, C={item.id} ")
            parent.contentChildIds.append(item.id)
          else:
            # Up
            current_parent.pop()
            current_level = new_level
          previous_item = item
          #print("")
          #print("")
        except Exception as e:
          self._general_error(f"Failed to create Content object, exception {e}")
          #print(f"{traceback.format_exc()}")
          self._traceback(f"{traceback.format_exc()}")
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      #print(f"{traceback.format_exc()}")
      self._traceback(f"{traceback.format_exc()}")

