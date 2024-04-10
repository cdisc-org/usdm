import traceback
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.option_manager import Options, EmptyNoneOption
from usdm_excel.globals import Globals

class ConfigurationSheet(BaseSheet):

  SHEET_NAME = 'configuration'
  
  PARAMS_NAME_COL = 0
  PARAMS_VALUE_COL = 1

  def __init__(self, file_path: str, globals: Globals):
    try:
      super().__init__(file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME, header=None)
      self.globals.option_manager.set(Options.EMPTY_NONE, EmptyNoneOption.NONE)
      self.globals.option_manager.set(Options.USDM_VERSION, 3)
      self._process_sheet()
    except Exception as e:
      self._sheet_exception(e)

  def _process_sheet(self):
    for rindex, row in self.sheet.iterrows():
      name = self.read_cell(rindex, self.PARAMS_NAME_COL).strip().upper()
      value = self.read_cell(rindex, self.PARAMS_VALUE_COL)
      if name == 'CT VERSION':
        parts = value.split('=')
        if len(parts) == 2:
          self.globals.ct_version_manager.add(parts[0].strip(), parts[1].strip())
      elif name == 'EMPTY NONE':
        if value.strip().upper() == 'EMPTY':
          self.globals.option_manager.set(Options.EMPTY_NONE, EmptyNoneOption.EMPTY)
      elif name == 'USDM VERSION':
        text = value.strip().upper()
        if text in ['2', '3']:
          self.globals.option_manager.set(Options.USDM_VERSION, int(text))
      elif name == 'SDR PREV NEXT':
        self._general_warning("The SDR PREV NEXT option is now deprecated and will be ignored.")
      elif name == 'SDR ROOT':
        self._general_warning("The SDR ROOT option is now deprecated and will be ignored.")
      elif name == 'SDR DESCRIPTION':
        self._general_warning("The SDR DESCRIPTION option is now deprecated and will be ignored.")
