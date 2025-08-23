import pandas as pd
from usdm_excel.study_identifier_and_organization_sheets.study_references_sheet import (
    StudyReferencesSheet,
)
from usdm_model.code import Code
from usdm_model.organization import Organization
from tests.test_factory import Factory

DEFAULT_COLUMNS = ["identifier", "organization", "referenceType"]
MISSING_COLUMN = ["identifier", "organization"]


def test_create(mocker, globals):
    ids = ["Code_1", "RI_1", "Code_2", "RI_2"]
    data = [
        ["NCT12345678", "Sponsor1", "Pediatric Investigation Plan"],
        ["NCT12345679", "Sponsor2", "Clinical Development Plan"],
    ]
    sheet = _setup(mocker, globals, data, ids)
    assert len(sheet.items) == 2
    assert sheet.items[0].model_dump() == {
        "id": "RI_1",
        "text": "NCT12345678",
        "scopeId": "Organization_1",
        "extensionAttributes": [],
        "instanceType": "ReferenceIdentifier",
        "type": {
            "id": "Code_1",
            "code": "C215674",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Pediatric Investigation Plan",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
    }
    assert sheet.items[1].model_dump() == {
        "id": "RI_2",
        "text": "NCT12345679",
        "scopeId": "Organization_2",
        "extensionAttributes": [],
        "instanceType": "ReferenceIdentifier",
        "type": {
            "id": "Code_2",
            "code": "C142424",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Clinical Development Plan",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
    }


def test_create_empty(mocker, globals):
    ids = []
    data = []
    sheet = _setup(mocker, globals, data, ids)
    assert len(sheet.items) == 0


def test_error(mocker, globals):
    ids = ["Code_1", "RI_1"]
    data = [["NCT12345678", "Sponsor1"]]
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    sheet = _setup(mocker, globals, data, ids, MISSING_COLUMN)
    assert sheet.items == []
    assert mock_error.call_count == 1
    errors = [
        mocker.call(
            "studyReferences",
            None,
            None,
            "Exception. Error [Failed to detect column(s) 'referenceType, type' in sheet] while reading sheet 'studyReferences'. See log for additional details.",
            40,
        ),
    ]
    mock_error.assert_has_calls(errors)


def _setup(mocker, globals, data, ids, columns=DEFAULT_COLUMNS):
    globals.cross_references.clear()
    globals.id_manager.clear()
    organizations(globals)
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ids
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=columns)
    mock_json = mocker.patch("json.load")
    mock_json.return_value = {}
    return StudyReferencesSheet("", globals)


def organizations(globals):
    factory = Factory(globals)
    org1 = factory.item(
        Organization,
        {
            "name": "Sponsor1",
            "type": factory.cdisc_code("C54149", "Pharmaceutical Company"),
            "identifier": "123456781",
            "identifierScheme": "DUNS",
            "legalAddress": None,
        },
    )
    org2 = factory.item(
        Organization,
        {
            "name": "Sponsor2",
            "type": factory.cdisc_code("C54149", "Pharmaceutical Company"),
            "identifier": "123456782",
            "identifierScheme": "DUNS",
            "legalAddress": None,
        },
    )
    org3 = factory.item(
        Organization,
        {
            "name": "Sponsor3",
            "type": factory.cdisc_code("C54149", "Pharmaceutical Company"),
            "identifier": "123456783",
            "identifierScheme": "DUNS",
            "legalAddress": None,
        },
    )
    globals.cross_references.add(org1.name, org1)
    globals.cross_references.add(org2.name, org2)
    globals.cross_references.add(org3.name, org3)
