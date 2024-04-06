import pytest
from src.usdm_excel.globals import Globals as GlobalsClass

global_instance = GlobalsClass()
global_instance.create()
  
@pytest.fixture
def globals():
  return global_instance