import pandas as pd
from usdm_excel.study_identifier_and_organization_sheets.study_identifiers_sheet import (
    StudyIdentifiersSheet,
)
from usdm_model.code import Code
from usdm_model.organization import Organization
from usdm_model.address import Address
from tests.test_factory import Factory


def test_create(mocker, globals):
    globals.cross_references.clear()
    globals.id_manager.clear()
    organizations(globals)
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Id_1", "Id_2", "Id_3"]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        ["NCT12345678", "Sponsor1"],
        ["NCT12345679", "Sponsor2"],
        ["NCT123456710", "Sponsor3"],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=["identifier", "organization"])
    item = StudyIdentifiersSheet("", globals)
    assert len(item.items) == 3
    assert item.items[0].model_dump() == {
        "id": "Id_1",
        "extensionAttributes": [],
        "instanceType": "StudyIdentifier",
        "scopeId": "Organization_1",
        "text": "NCT12345678",
    }
    assert item.items[1].model_dump() == {
        "id": "Id_2",
        "extensionAttributes": [],
        "instanceType": "StudyIdentifier",
        "scopeId": "Organization_2",
        "text": "NCT12345679",
    }
    assert item.items[2].model_dump() == {
        "id": "Id_3",
        "extensionAttributes": [],
        "instanceType": "StudyIdentifier",
        "scopeId": "Organization_3",
        "text": "NCT123456710",
    }


def test_create_empty(mocker, globals):
    globals.cross_references.clear()
    globals.id_manager.clear()
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = []
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=["identifier", "organization"])
    ids = StudyIdentifiersSheet("", globals)
    assert len(ids.items) == 0


def test_error(mocker, globals):
    globals.cross_references.clear()
    globals.id_manager.clear()
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Code_1", "Org_1", "Addr_1", "Id_1"]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        ["NCT12345678"],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=["identifier"])
    mock_json = mocker.patch("json.load")
    mock_json.return_value = {}
    expected_1 = Code(
        id="Code1",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="GBR",
    )
    mock_code = mocker.patch("usdm_excel.iso_3166.ISO3166.code")
    mock_code.side_effect = [expected_1]
    ids = StudyIdentifiersSheet("", globals)
    mock_error.assert_called()
    assert mock_error.call_args[0][0] == "studyIdentifiers"
    assert mock_error.call_args[0][1] == None
    assert mock_error.call_args[0][2] == None
    assert (
        mock_error.call_args[0][3]
        == "Exception. Failed to find organization with name ''. See log for additional details."
    )


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
