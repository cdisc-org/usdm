from usdm_excel.document.utility import get_soup

def test_normal(mocker, globals, factory):
  globals.errors.clear()
  bs = factory.base_sheet(mocker)
  assert globals.errors.count() == 0
  result = get_soup("<p>Hello</p>", bs)
  expected = '<p>Hello</p>'
  assert str(result) == expected
  assert globals.errors.count() == 0

def test_warning(mocker, globals, factory):
  globals.errors.clear()
  bs = factory.base_sheet(mocker)
  assert globals.errors.count() == 0
  result = get_soup("input/output", bs)
  expected = 'input/output'
  assert str(result) == expected
  expected = "Warning in sheet : Warning raised within Soup package, processing 'input/output'\n"\
    "Message returned 'The input looks more like a filename than markup. You may want to open this "\
    "file and pass the filehandle into Beautiful Soup.'" 
  assert globals.errors.count() == 1
  assert globals.errors.items[0].to_log() == expected

