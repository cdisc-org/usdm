from usdm_model.study_design import StudyDesign
from usdm_model.study_epoch import StudyEpoch
from usdm_model.study_cell import StudyCell
from usdm_model.study_arm import StudyArm
from usdm_model.population_definition import *
from usdm_model.study import Study
from usdm_model.study_version import StudyVersion
from usdm_model.study_title import StudyTitle
from usdm_model.study_definition_document import StudyProtocolDocument
from usdm_model.study_definition_document_version import StudyProtocolDocumentVersion
from usdm_model.study_identifier import StudyIdentifier
from usdm_model.organization import Organization
from usdm_model.address import Address
from usdm_excel.globals import Globals
from tests.test_factory import Factory

class MinimalStudy():

  def __init__(self, globals: Globals):
    globals.id_manager.clear()
    factory = Factory(globals)
    self.population = factory.item(StudyDesignPopulation, {'name': 'POP1', 'label': '', 'description': '', 'includesHealthySubjects': True, 'criteria': []})
    cell = factory.item(StudyCell, {'armId': "X", 'epochId': "Y"})
    arm = factory.item(StudyArm, {'name': "Arm1", 'type': factory.cdisc_dummy(), 'dataOriginDescription': 'xxx', 'dataOriginType': factory.cdisc_dummy()})
    epoch = factory.item(StudyEpoch, {'name': 'EP1', 'label': 'Epoch A', 'description': '', 'type': factory.cdisc_dummy()})
    study_title = factory.item (StudyTitle, {'text': 'Title', 'type': factory.cdisc_dummy()})
    self.protocl_document_version = factory.item(StudyProtocolDocumentVersion, {'protocolVersion': '1', 'protocolStatus': factory.cdisc_dummy()})
    self.protocl_document = factory.item(StudyProtocolDocument, {'name': 'EP1', 'label': 'Epoch A', 'description': '', 'versions': [self.protocl_document_version]})
    self.study_design = factory.item(StudyDesign, {'name': 'Study Design', 'label': '', 'description': '', 
      'rationale': 'XXX', 'interventionModel': factory.cdisc_dummy(), 'arms': [arm], 'studyCells': [cell], 
      'epochs': [epoch], 'population': self.population})
    address = factory.item(Address, {'line': 'line 1', 'city': 'City', 'district': 'District', 'state': 'State', 'postalCode': '12345', 'country': factory.code("UKK", "UKK_decode")})
    organization = factory.item(Organization, {'name': 'Sponsor', 'organizationType': factory.cdisc_code("C70793", "sponsor"), 'identifier': "123456789", 'identifierScheme': "DUNS", 'legalAddress': address}) 
    identifier = factory.item(StudyIdentifier, {'studyIdentifier': 'SPONSOR-1234', 'studyIdentifierScope': organization})
    self.study_version = factory.item(StudyVersion, {'versionIdentifier': '1', 'rationale': 'XXX', 'titles': [study_title], 'studyDesigns': [self.study_design], 
                                                     'documentVersionId': self.protocl_document_version.id, 'studyIdentifiers': [identifier]}) 
    self.study = factory.item(Study, {'id': None, 'name': 'Study', 'label': '', 'description': '', 'versions': [self.study_version], 'documentedBy': self.protocl_document}) 

