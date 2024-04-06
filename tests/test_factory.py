import pandas as pd
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.globals import Globals
from usdm_model.code import Code

class Factory():

  def __init__(self):
    pass
    #self.globals = Globals()
    #self.globals.create()
  
  def clear(self):
    pass
    #self.globals.id_manager.clear()
    #self.globals.cross_references.clear()
    #self.globals.errors.clear()

  def globals(self):
    return self.globals
  
  def item(self, cls, params):
    params['id'] = params['id'] if 'id' in params else self.globals.id_manager.build_id(cls)
    params['instanceType'] = cls.__name__
    return cls(**params)

  def set(self, cls, item_list):
    results = []
    for item in item_list:
      results.append(self.item(cls, item))
    return results

  def base_sheet(self, mocker):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = []
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=[])
    return BaseSheet("", self.globals, "")

  def cdisc_code(self, code, decode):
    return self._build_code(code=code, system="xxx", version="1", decode=decode)
  
  def cdisc_dummy(self):
    return self.cdisc_code("C12345", "decode")

  def _build_code(self, code, system, version, decode):
    id = self.globals.id_manager.build_id(Code)
    instance = Code(id=id, code=code, codeSystem=system, codeSystemVersion=version, decode=decode)
    return instance