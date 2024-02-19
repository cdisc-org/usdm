import pandas as pd
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cdisc_ct import CDISCCT
from usdm_model.study_design import StudyDesign
from usdm_model.eligibility_criterion import EligibilityCriterion
from usdm_model.study_epoch import StudyEpoch
from usdm_model.study_cell import StudyCell
from usdm_model.study_arm import StudyArm
from usdm_model.population_definition import *
from usdm_model.study import Study
from usdm_model.study_version import StudyVersion
from usdm_model.study_title import StudyTitle
from usdm_model.study_protocol_document import StudyProtocolDocument
from usdm_model.study_protocol_document_version import StudyProtocolDocumentVersion
from usdm_excel.document.template_plain import TemplatePlain

from tests.test_factory import Factory

cdisc_ct = CDISCCT()
factory = Factory()

INCLUSION = cdisc_ct.code('C25532', 'Inc')
EXCLUSION = cdisc_ct.code('C25370', 'Exc')
DUMMY = cdisc_ct.code("C12345", "decode")


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

criteria = create_criteria()
dummy_population = factory.item(StudyDesignPopulation, {'name': 'POP1', 'label': '', 'description': '', 'includesHealthySubjects': True, 'criteria': criteria })
dummy_cell = factory.item(StudyCell, {'armId': "X", 'epochId': "Y"})
dummy_arm = factory.item(StudyArm, {'name': "Arm1", 'type': DUMMY, 'dataOriginDescription': 'xxx', 'dataOriginType': DUMMY})
dummy_epoch = factory.item(StudyEpoch, {'name': 'EP1', 'label': 'Epoch A', 'description': '', 'type': DUMMY})

p_doc_version = factory.item(StudyProtocolDocumentVersion, {'protocolVersion': '1', 'protocolStatus': DUMMY})
p_doc = factory.item(StudyProtocolDocument, {'name': 'EP1', 'label': 'Epoch A', 'description': '', 'versions': [p_doc_version]})

study_design = factory.item(StudyDesign, {'name': 'Study Design', 'label': '', 'description': '', 
  'rationale': 'XXX', 'interventionModel': DUMMY, 'arms': [dummy_arm], 'studyCells': [dummy_cell], 
  'epochs': [dummy_epoch], 'population': dummy_population})
study_title = factory.item (StudyTitle, {'text': 'Title', 'type': DUMMY})
study_version = factory.item(StudyVersion, {'versionIdentifier': '1', 'rationale': 'XXX', 'titles': [study_title], 'studyDesigns': [study_design]}) 
study = factory.item(Study, {'id': None, 'name': 'Study', 'label': '', 'description': '', 'versions': [study_version], 'documentedBy': p_doc}) 

def fake_sheet(mocker):
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  data = []
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame(data, columns=[])
  return BaseSheet("", "")

def test_create(mocker):
  bs = fake_sheet(mocker)
  template = TemplatePlain(bs, study)
  result = template.inclusion()
  expected = '<table class="table"><tr><td><p>01</p></td><td><p><usdm:ref klass="EligibilityCriterion" id="EligibilityCriterion_1" attribute="text"></usdm:ref></p></td></tr><tr><td><p>02</p></td><td><p><usdm:ref klass="EligibilityCriterion" id="EligibilityCriterion_2" attribute="text"></usdm:ref></p></td></tr></table>'
  assert result == expected
