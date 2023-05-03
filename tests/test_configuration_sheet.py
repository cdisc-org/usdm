import pytest
import pandas as pd

from src.usdm_excel.configuration_sheet import ConfigurationSheet
from src.usdm_excel.option_manager import Options, PrevNextOption, RootOption
#from src.usdm_excel.option_manager import *
#from src.usdm_excel.ct_version_manager import ct_version_manager
from src.usdm_excel import ct_version_manager as ctvm
from src.usdm_excel import om

def test_defaults(mocker):
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = {'col_1': ['Option X', 'Option 2', 'Option 3'], 'col_2': ['maybe', 'True', '']}
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data)
  configuration = ConfigurationSheet("")
  assert om.get(Options.ROOT) == RootOption.API_COMPLIANT.value
  assert om.get(Options.PREVIOUS_NEXT) == PrevNextOption.NONE.value
  assert om.get(Options.DESCRIPTION) == ""

def test_set(mocker):
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = {'col_1': ['Ct Version', 'SDR Prev Next', 'sdr ROOT', 'sdr Description'], 'col_2': ['THIS=that', 'sdr', 'SDR', 'No desc set']}
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data)
  configuration = ConfigurationSheet("")
  assert om.get(Options.ROOT) == RootOption.SDR_COMPATABLE.value
  assert om.get(Options.PREVIOUS_NEXT) == PrevNextOption.NULL_STRING.value
  assert om.get(Options.DESCRIPTION) == "No desc set"
  assert ctvm.get('THIS') == 'that'
