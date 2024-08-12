import pytest
from usdm_excel.document.elements import Elements

@pytest.fixture
def elements(mocker, globals, factory, minimal):
  sheet = factory.base_sheet(mocker)
  return Elements(sheet, minimal.study, 'sponsor')

def test_phase(elements):
  assert elements.study_phase() == '<usdm:ref klass="Code" id="Code_9" attribute="decode"/>'

def test_short_title(elements):
  assert elements.study_short_title() == '<usdm:ref klass="StudyTitle" id="StudyTitle_2" attribute="text"/>'

def test_full_title(elements):
  assert elements.study_full_title() == '<usdm:ref klass="StudyTitle" id="StudyTitle_1" attribute="text"/>'

def test_acronym(elements):
  assert elements.study_acronym() == '<usdm:ref klass="StudyTitle" id="StudyTitle_3" attribute="text"/>'

def test_study_rationale(elements):
  assert elements.study_rationale() == '<usdm:ref klass="StudyVersion" id="StudyVersion_1" attribute="rationale"/>'

def test_version_identifier(elements):
  assert elements.study_version_identifier() == '<usdm:ref klass="StudyVersion" id="StudyVersion_1" attribute="versionIdentifier"/>'

def test_identifier(elements):
  assert elements.study_identifier() == '<usdm:ref klass="StudyIdentifier" id="StudyIdentifier_1" attribute="studyIdentifier"/>'

def test_regulatory_identifiers(elements):
  assert elements.study_regulatory_identifiers() == '<usdm:ref klass="StudyIdentifier" id="StudyIdentifier_2" attribute="studyIdentifier"/>, <usdm:ref klass="StudyIdentifier" id="StudyIdentifier_3" attribute="studyIdentifier"/>'

def test_study_date(elements):
  assert elements.study_date() == '<usdm:ref klass="GovernanceDate" id="GovernanceDate_1" attribute="dateValue"/>'

def test_approval_date(elements):
  assert elements.approval_date() == '<usdm:ref klass="GovernanceDate" id="GovernanceDate_1" attribute="dateValue"/>'

def test_organization_name_and_address(elements):
  assert elements.organization_name_and_address() == '<usdm:ref klass="Organization" id="Organization_1" attribute="name"/>, <usdm:ref klass="Address" id="Address_1" attribute="text"/>'

def test_organization_address(elements):
  assert elements.organization_address() == '<usdm:ref klass="Address" id="Address_1" attribute="text"/>'

def test_organization_name(elements):
  assert elements.organization_name() == '<usdm:ref klass="Organization" id="Organization_1" attribute="name"/>'

def test_amendment(elements):
  assert elements.amendment() == '<usdm:ref klass="StudyAmendment" id="StudyAmendment_1" attribute="number"/>'

def test_amendment_scopes(elements):
  assert elements.amendment_scopes() == '<usdm:ref klass="Code" id="Code_3" attribute="decode"/>'
