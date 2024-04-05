
from yattag import Doc
from usdm_model.eligibility_criterion import EligibilityCriterion
from usdm_model.narrative_content import NarrativeContent
#from usdm_excel.document.document import Document

from tests.test_factory import Factory
from tests.test_data_factory import MinimalStudy
from tests.test_utility import clear as tu_clear

factory = Factory()

INCLUSION = factory.cdisc_code('C25532', 'Inc')
EXCLUSION = factory.cdisc_code('C25370', 'Exc')

def create_criteria():
  item_list = [
    {'name': 'IE1', 'label': '', 'description': '', 'text': 'Only perform at baseline', 
     'dictionaryId': None, 'category': INCLUSION, 'identifier': '01', 'nextId': None, 'previousId': None, 'contextId': None
    },
    {'name': 'IE2', 'label': '', 'description': '', 'text': '<p>Only perform on males</p>', 
    'dictionaryId': None, 'category': INCLUSION, 'identifier': '02', 'nextId': None, 'previousId': None, 'contextId': None
    },
  ]
  results = factory.set(EligibilityCriterion, item_list)
  return results


def test_create(mocker):
  tu_clear()
  minimal = MinimalStudy()
  minimal.population.criteria = create_criteria()
  bs = factory.base_sheet(mocker)
  doc = Doc()
  document = Document(bs, "xxx", minimal.study, "")
  content = factory.item(NarrativeContent, {'name': "C1", 'sectionNumber': '1.1.1', 'sectionTitle': 'Section Title', 'text': '<usdm:macro id="section" name="inclusion"/>', 'childIds': []})
  document._content_to_html(content, doc)
  result = doc.getvalue()
  expected = '<div class=""><h3 id="section-1.1.1">1.1.1 Section Title</h3><usdm:macro id="section" name="inclusion"></usdm:macro></div>'
  assert result == expected
