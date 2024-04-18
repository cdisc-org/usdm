from usdm_excel.document.elements import Elements

def test_organization_address(mocker, globals, factory, minimal):
  sheet = factory.base_sheet(mocker)
  elements = Elements(sheet, minimal.study)
  assert elements.organization_address() == '<usdm:ref klass="Address" id="Address_1" attribute="text"/>'

def test_organization_name(mocker, globals, factory, minimal):
  sheet = factory.base_sheet(mocker)
  elements = Elements(sheet, minimal.study)
  assert elements.organization_name() == '<usdm:ref klass="Organization" id="Organization_1" attribute="name"/>'