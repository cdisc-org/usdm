from usdm_excel.base_sheet import BaseSheet
from usdm_excel.ct_version_manager import ct_version_manager
from usdm_excel.option_manager import * 
import traceback
import pandas as pd

class ConfigurationSheet(BaseSheet):

  PARAMS_NAME_COL = 0
  PARAMS_VALUE_COL = 1

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='configuration', header=None)
      option_manager.set(Options.EMPTY_NONE, EmptyNoneOption.NONE)
      option_manager.set(Options.USDM_VERSION, 3)
      # option_manager.set(Options.PREVIOUS_NEXT, PrevNextOption.NONE)
      # option_manager.set(Options.ROOT, RootOption.API_COMPLIANT)
      # option_manager.set(Options.DESCRIPTION, "")
      self._process_sheet()
    except Exception as e:
      self._general_error(f"Exception '{e}' raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

  def om(self):
    return option_manager
  
  def _process_sheet(self):
    for rindex, row in self.sheet.iterrows():
      name = self.read_cell(rindex, self.PARAMS_NAME_COL).strip().upper()
      value = self.read_cell(rindex, self.PARAMS_VALUE_COL)
      if name == 'CT VERSION':
        parts = value.split('=')
        if len(parts) == 2:
          ct_version_manager.add(parts[0].strip(), parts[1].strip())
      elif name == 'EMPTY NONE':
        if value.strip().upper() == 'EMPTY':
          option_manager.set(Options.EMPTY_NONE, EmptyNoneOption.EMPTY)
      elif name == 'USDM VERSION':
        text = value.strip().upper()
        if text in ['2', '3']:
          option_manager.set(Options.USDM_VERSION, int(text))
      elif name == 'SDR PREV NEXT':
        self._general_warning("The SDR PREV NEXT option is now deprecated and will be ignored.")
      elif name == 'SDR ROOT':
        self._general_warning("The SDR ROOT option is now deprecated and will be ignored.")
      elif name == 'SDR DESCRIPTION':
        self._general_warning("The SDR DESCRIPTION option is now deprecated and will be ignored.")
