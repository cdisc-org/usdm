from src.usdm_excel.globals import Globals as GlobalsClass
from tests.test_factory import Factory as FactoryClass
from tests.test_data_factory import MinimalStudy
from usdm_model.eligibility_criterion import EligibilityCriterion
from usdm_excel.document.template_plain import TemplatePlain

def create_criteria(factory: FactoryClass, minimal: MinimalStudy):
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
  #print(f"RESULTS: {results}")
  for criterion in results:
    minimal.population.criterionIds.append(criterion.id)
  minimal.study.versions[0].criteria = results
  return results

def test_create(mocker, globals: GlobalsClass, minimal: MinimalStudy, factory: FactoryClass):
  globals.id_manager.clear()
  criteria = create_criteria(factory, minimal)
  bs = factory.base_sheet(mocker)
  template = TemplatePlain(bs, minimal.study_version, minimal.study_definition_document_version)
  result = template.inclusion({})
  expected = '<table class="table"><tr><td>01</td><td><usdm:ref klass="EligibilityCriterion" '\
    'id="EligibilityCriterion_1" attribute="text"></usdm:ref></td></tr><tr><td>02</td><td>'\
    '<usdm:ref klass="EligibilityCriterion" id="EligibilityCriterion_2" attribute="text"></usdm:ref>'\
    '</td></tr></table>'
  assert result == expected
