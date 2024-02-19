import pandas as pd
from usdm_excel.id_manager import id_manager
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cdisc_ct import CDISCCT

class Factory():

  def __init__(self):
    self.cdisc_ct = CDISCCT()
  
  def item(self, cls, params):
    params['id'] = params['id'] if 'id' in params else id_manager.build_id(cls)
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
    return BaseSheet("", "")

  def cdisc_code(self, code, decode):
    return self.cdisc_ct.code(code, decode)
  
  def cdisc_dummy(self):
    return self.cdisc_ct.code("C12345", "decode")
