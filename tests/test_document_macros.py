import pytest
from usdm_model.eligibility_criterion import EligibilityCriterion
from usdm_model.biomedical_concept import BiomedicalConcept
from usdm_model.activity import Activity
from usdm_excel.document.macros import Macros
from usdm_excel.globals import Globals
from tests.test_factory import Factory

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

def create_bc(factory: Factory, globals: Globals):
  code = factory.cdisc_dummy()
  alias_code = factory.alias_code(code)
  bc = factory.item(BiomedicalConcept, {'name': 'height', 'label': 'bc name', 'reference': 'something', 'code': alias_code, 'synonyms': ['body height', 'Standing height']})
  activity = factory.item(Activity, {'name': 'vitals' ,'biomedicalConceptIds': [bc.id]})
  globals.cross_references.add(bc.id, bc)
  globals.cross_references.add(activity.name, activity)

def get_instance(mocker, globals, factory, minimal):
  globals.id_manager.clear()
  minimal.population.criteria = create_criteria(factory)
  bs = factory.base_sheet(mocker)
  macro = Macros(bs, minimal.study)
  return macro

def test_create(mocker, globals, factory, minimal):
  macro = get_instance(mocker, globals, factory, minimal)
  assert macro is not None

def test_resolve_ok(mocker, globals, factory, minimal):
  macro = get_instance(mocker, globals, factory, minimal)
  result = macro.resolve('<usdm:macro id="section" name="inclusion"/>')
  expected = '<table class="table"><tr><td>01</td><td><usdm:ref attribute="text" '\
    'id="EligibilityCriterion_1" klass="EligibilityCriterion"></usdm:ref></td></tr><tr><td>02'\
    '</td><td><usdm:ref attribute="text" id="EligibilityCriterion_2" klass="EligibilityCriterion">'\
    '</usdm:ref></td></tr></table>'
  assert result == expected

def test_invalid_method(mocker, globals, factory, minimal):
  macro = get_instance(mocker, globals, factory, minimal)
  result = macro.resolve('<usdm:macro id="xxx" name="inclusion"/>')
  expected = 'Missing content: invalid method name'
  assert result == expected

def test_invalid_exception(mocker, globals, factory, minimal):
  macro = get_instance(mocker, globals, factory, minimal)
  result = macro.resolve('<usdm:macro name="inclusion"/>')
  expected = 'Missing content: exception'
  assert result == expected

def test_bc_ok_name(mocker, globals, factory, minimal):
  macro = get_instance(mocker, globals, factory, minimal)
  create_bc(factory, globals)
  result = macro.resolve('<usdm:macro id="bc" name="height" activity="vitals"/>')
  expected = '<usdm:ref attribute="label" id="BiomedicalConcept_1" klass="BiomedicalConcept"></usdm:ref>'
  assert result == expected

def test_bc_ok_synonym_1(mocker, globals, factory, minimal):
  macro = get_instance(mocker, globals, factory, minimal)
  create_bc(factory, globals)
  result = macro.resolve('<usdm:macro id="bc" name="body HEIGHT" activity="vitals"/>')
  expected = '<usdm:ref attribute="label" id="BiomedicalConcept_1" klass="BiomedicalConcept"></usdm:ref>'
  assert result == expected

def test_bc_ok_synonym_2(mocker, globals, factory, minimal):
  macro = get_instance(mocker, globals, factory, minimal)
  create_bc(factory, globals)
  result = macro.resolve('<usdm:macro id="bc" name=" standing height " activity="vitals"/>')
  expected = '<usdm:ref attribute="label" id="BiomedicalConcept_1" klass="BiomedicalConcept"></usdm:ref>'
  assert result == expected

def test_bc_error(mocker, globals, factory, minimal):
  macro = get_instance(mocker, globals, factory, minimal)
  create_bc(factory, globals)
  result = macro.resolve('<usdm:macro id="bc" name="heightX" activity="vitals"/>')
  expected = 'Missing BC: failed to find BC in activity'
  assert result == expected

def test_activity_error(mocker, globals, factory, minimal):
  macro = get_instance(mocker, globals, factory, minimal)
  create_bc(factory, globals)
  result = macro.resolve('<usdm:macro id="bc" name="height" activity="vitalsX"/>')
  expected = 'Missing activity: failed to find activity'
  assert result == expected
