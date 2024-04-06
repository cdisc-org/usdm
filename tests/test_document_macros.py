from usdm_model.eligibility_criterion import EligibilityCriterion
from usdm_excel.document.macros import Macros
from tests.test_data_factory import MinimalStudy

def create_criteria(factory):
  INCLUSION = factory.cdisc_code('C25532', 'Inc')
  EXCLUSION = factory.cdisc_code('C25370', 'Exc')
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

def test_create(mocker, globals, factory, minimal):
  minimal.population.criteria = create_criteria(factory)
  bs = factory.base_sheet(mocker)
  macro = Macros(bs, minimal.study)
  result = macro.resolve('<usdm:macro id="section" name="inclusion"/>')
  expected = '<table class="table"><tr><td>01</td><td><usdm:ref attribute="text" '\
    'id="EligibilityCriterion_1" klass="EligibilityCriterion"></usdm:ref></td></tr><tr><td>02'\
    '</td><td><usdm:ref attribute="text" id="EligibilityCriterion_2" klass="EligibilityCriterion">'\
    '</usdm:ref></td></tr></table>'
  assert result == expected
