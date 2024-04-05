import pandas as pd
from usdm_model.eligibility_criterion import EligibilityCriterion
from usdm_excel.document.template_plain import TemplatePlain

from tests.test_factory import Factory
from tests.test_data_factory import MinimalStudy

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
  template = TemplatePlain(bs, minimal.study)
  result = template.inclusion()
  expected = '<table class="table"><tr><td>01</td><td><usdm:ref klass="EligibilityCriterion" '\
    'id="EligibilityCriterion_1" attribute="text"></usdm:ref></td></tr><tr><td>02</td><td>'\
    '<usdm:ref klass="EligibilityCriterion" id="EligibilityCriterion_2" attribute="text"></usdm:ref>'\
    '</td></tr></table>'
  assert result == expected
