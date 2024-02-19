from usdm_excel.document.utility import get_soup
from usdm_excel.errors.errors import error_manager

from tests.test_factory import Factory

factory = Factory()

def test_normal(mocker):
  bs = factory.base_sheet(mocker)
  assert error_manager.count() == 0
  result = get_soup("<p>Hello</p>", bs)
  expected = '<p>Hello</p>'
  assert str(result) == expected
  assert error_manager.count() == 0

def test_warning(mocker):
  bs = factory.base_sheet(mocker)
  assert error_manager.count() == 0
  result = get_soup("input/output", bs)
  expected = 'input/output'
  assert str(result) == expected
  expected = "Warning in sheet : Warning raised within Soup package, processing 'input/output'\n"\
    "Message returned 'The input looks more like a filename than markup. You may want to open this "\
    "file and pass the filehandle into Beautiful Soup.'" 
  assert error_manager.count() == 1
  assert error_manager.items[0].to_log() == expected

