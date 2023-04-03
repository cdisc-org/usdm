from usdm_excel.base_sheet import BaseSheet
from usdm_excel.ct_version_manager import ct_version_manager
import traceback
import pandas as pd

class ConfigurationSheet(BaseSheet):

  PARAMS_NAME_COL = 0
  PARAMS_VALUE_COL = 1

  def __init__(self, file_path):
    try:
      #super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='configuration', header=None))
      super().__init__(file_path=file_path, sheet_name='configuration', header=None)
      self._process_sheet()
    except Exception as e:
      print("Oops!", e, "occurred.")
      traceback.print_exc()

  def _process_sheet(self):
    for rindex, row in self.sheet.iterrows():
      name = self.read_cell(rindex, self.PARAMS_NAME_COL)
      value = self.read_cell(rindex, self.PARAMS_VALUE_COL)
      if name.strip().upper() == 'CT VERSION':
        parts = value.split('=')
        if len(parts) == 2:
          ct_version_manager.add(parts[0].strip(), parts[1].strip())
  