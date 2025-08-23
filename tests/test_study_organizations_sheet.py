import pandas as pd
from usdm_excel.study_identifier_and_organization_sheets.study_organizations_sheet import (
    StudyOrganizationsSheet,
)
from usdm_model.code import Code


def test_create(mocker, globals):
    globals.cross_references.clear()
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [
        "Code_1",
        "Addr_1",
        "Org_1",
        "Code_2",
        "Addr_2",
        "Org_2",
        "Code_3",
        "Addr_3",
        "Org_3",
    ]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        [
            "USGOV",
            "CT-GOV",
            "ClinicalTrials.gov",
            "label 1",
            "Clinical Study Registry",
            "line|district|city|state|postal_code|GBR",
        ],
        [
            "USGOV2",
            "CT-GOV2",
            "ClinicalTrials2.gov",
            "label 2",
            "Clinical Study Registry",
            "line2,district2,city2,state2,postal_code2,FRA",
        ],
        [
            "USGOV3",
            "CT-GOV3",
            "ClinicalTrials3.gov",
            "label 3",
            "Clinical Study Registry",
            "line3,district3,city3,state3,postal_code3,FR",
        ],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=["identifierScheme", "identifier", "name", "label", "type", "address"],
    )
    mock_json = mocker.patch("json.load")
    mock_json.return_value = {}
    expected_1 = Code(
        id="Code1",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="GBR",
    )
    expected_2 = Code(
        id="Code2",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="FRA",
    )
    expected_3 = Code(
        id="Code3",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="FRA",
    )
    mock_code = mocker.patch("usdm_excel.iso_3166.ISO3166.code")
    mock_code.side_effect = [expected_1, expected_2, expected_3]
    item = StudyOrganizationsSheet("", globals)
    assert len(item.items) == 3
    assert item.items[0].model_dump() == {
        "id": "Org_1",
        "identifier": "CT-GOV",
        "identifierScheme": "USGOV",
        "extensionAttributes": [],
        "instanceType": "Organization",
        "label": "label 1",
        "legalAddress": {
            "city": "city",
            "country": {
                "code": "code",
                "codeSystem": "codesys",
                "codeSystemVersion": "3",
                "decode": "GBR",
                "id": "Code1",
                "extensionAttributes": [],
                "instanceType": "Code",
            },
            "district": "district",
            "id": "Addr_1",
            "extensionAttributes": [],
            "instanceType": "Address",
            "lines": [
                "line",
            ],
            "postalCode": "postal_code",
            "state": "state",
            "text": "line, city, district, state, postal_code, GBR",
        },
        "managedSites": [],
        "name": "ClinicalTrials.gov",
        "type": {
            "code": "C93453",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Clinical Study Registry",
            "id": "Code_1",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
    }
    assert item.items[1].model_dump() == {
        "id": "Org_2",
        "identifier": "CT-GOV2",
        "identifierScheme": "USGOV2",
        "extensionAttributes": [],
        "instanceType": "Organization",
        "label": "label 2",
        "legalAddress": {
            "city": "city2",
            "country": {
                "code": "code",
                "codeSystem": "codesys",
                "codeSystemVersion": "3",
                "decode": "FRA",
                "id": "Code2",
                "extensionAttributes": [],
                "instanceType": "Code",
            },
            "district": "district2",
            "id": "Addr_2",
            "extensionAttributes": [],
            "instanceType": "Address",
            "lines": [
                "line2",
            ],
            "postalCode": "postal_code2",
            "state": "state2",
            "text": "line2, city2, district2, state2, postal_code2, FRA",
        },
        "managedSites": [],
        "name": "ClinicalTrials2.gov",
        "type": {
            "code": "C93453",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Clinical Study Registry",
            "id": "Code_2",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
    }
    assert item.items[2].model_dump() == {
        "id": "Org_3",
        "identifier": "CT-GOV3",
        "identifierScheme": "USGOV3",
        "extensionAttributes": [],
        "instanceType": "Organization",
        "label": "label 3",
        "legalAddress": {
            "city": "city3",
            "country": {
                "code": "code",
                "codeSystem": "codesys",
                "codeSystemVersion": "3",
                "decode": "FRA",
                "id": "Code3",
                "extensionAttributes": [],
                "instanceType": "Code",
            },
            "district": "district3",
            "id": "Addr_3",
            "extensionAttributes": [],
            "instanceType": "Address",
            "lines": [
                "line3",
            ],
            "postalCode": "postal_code3",
            "state": "state3",
            "text": "line3, city3, district3, state3, postal_code3, FRA",
        },
        "managedSites": [],
        "name": "ClinicalTrials3.gov",
        "type": {
            "code": "C93453",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Clinical Study Registry",
            "id": "Code_3",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
    }


def test_create_with_z(mocker, globals):
    globals.cross_references.clear()
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [
        "Code_1",
        "Addr_1",
        "Org_1",
        "Code_2",
        "Addr_2",
        "Org_2",
        "Code_3",
        "Addr_3",
        "Org_3",
    ]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        [
            "USGOV",
            "CT-GOV",
            "ClinicalTrials.gov",
            "NCT12345678",
            "Clinical Study Registry",
            "line|district|city|state|postal_code|GBR",
        ],
        [
            "USGOV2",
            "CT-GOV2",
            "ClinicalTrials2.gov",
            "NCT12345679",
            "Clinical Study Registry",
            "line2,district2,city2,state2,postal_code2,FRA",
        ],
        [
            "USGOV3",
            "CT-GOV3",
            "ClinicalTrials3.gov",
            "NCT123456710",
            "Clinical Study Registry",
            "line3,district3,city3,state3,postal_code3,FR",
        ],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=[
            "organizationIdentifierScheme",
            "organizationIdentifier",
            "organizationName",
            "label",
            "organizationType",
            "organizationAddress",
        ],
    )
    mock_json = mocker.patch("json.load")
    mock_json.return_value = {}
    expected_1 = Code(
        id="Code1",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="GBR",
    )
    expected_2 = Code(
        id="Code2",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="FRA",
    )
    expected_3 = Code(
        id="Code3",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="FRA",
    )
    mock_code = mocker.patch("usdm_excel.iso_3166.ISO3166.code")
    mock_code.side_effect = [expected_1, expected_2, expected_3]
    item = StudyOrganizationsSheet("", globals)
    assert len(item.items) == 3
    assert item.items[0].model_dump() == {
        "id": "Org_1",
        "identifier": "CT-GOV",
        "identifierScheme": "USGOV",
        "extensionAttributes": [],
        "instanceType": "Organization",
        "label": "NCT12345678",
        "legalAddress": {
            "city": "city",
            "country": {
                "code": "code",
                "codeSystem": "codesys",
                "codeSystemVersion": "3",
                "decode": "GBR",
                "id": "Code1",
                "extensionAttributes": [],
                "instanceType": "Code",
            },
            "district": "district",
            "id": "Addr_1",
            "extensionAttributes": [],
            "instanceType": "Address",
            "lines": [
                "line",
            ],
            "postalCode": "postal_code",
            "state": "state",
            "text": "line, city, district, state, postal_code, GBR",
        },
        "managedSites": [],
        "name": "ClinicalTrials.gov",
        "type": {
            "code": "C93453",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Clinical Study Registry",
            "id": "Code_1",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
    }
    assert item.items[1].model_dump() == {
        "id": "Org_2",
        "identifier": "CT-GOV2",
        "identifierScheme": "USGOV2",
        "extensionAttributes": [],
        "instanceType": "Organization",
        "label": "NCT12345679",
        "legalAddress": {
            "city": "city2",
            "country": {
                "code": "code",
                "codeSystem": "codesys",
                "codeSystemVersion": "3",
                "decode": "FRA",
                "id": "Code2",
                "extensionAttributes": [],
                "instanceType": "Code",
            },
            "district": "district2",
            "id": "Addr_2",
            "extensionAttributes": [],
            "instanceType": "Address",
            "lines": [
                "line2",
            ],
            "postalCode": "postal_code2",
            "state": "state2",
            "text": "line2, city2, district2, state2, postal_code2, FRA",
        },
        "managedSites": [],
        "name": "ClinicalTrials2.gov",
        "type": {
            "code": "C93453",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Clinical Study Registry",
            "id": "Code_2",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
    }
    assert item.items[2].model_dump() == {
        "id": "Org_3",
        "identifier": "CT-GOV3",
        "identifierScheme": "USGOV3",
        "extensionAttributes": [],
        "instanceType": "Organization",
        "label": "NCT123456710",
        "legalAddress": {
            "city": "city3",
            "country": {
                "code": "code",
                "codeSystem": "codesys",
                "codeSystemVersion": "3",
                "decode": "FRA",
                "id": "Code3",
                "extensionAttributes": [],
                "instanceType": "Code",
            },
            "district": "district3",
            "id": "Addr_3",
            "extensionAttributes": [],
            "instanceType": "Address",
            "lines": [
                "line3",
            ],
            "postalCode": "postal_code3",
            "state": "state3",
            "text": "line3, city3, district3, state3, postal_code3, FRA",
        },
        "managedSites": [],
        "name": "ClinicalTrials3.gov",
        "type": {
            "code": "C93453",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Clinical Study Registry",
            "id": "Code_3",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
    }


def test_create_empty(mocker, globals):
    globals.cross_references.clear()
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = []
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=[
            "studyIdentifierName",
            "studyIdentifierDescription",
            "studyIdentifierType",
        ],
    )
    item = StudyOrganizationsSheet("", globals)
    assert len(item.items) == 0


def test_read_cell_by_name_error(mocker, globals):
    globals.cross_references.clear()
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [["Id 1", "Id One"]]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data, columns=["studyIdentifierName", "studyIdentifierDescription"]
    )
    ids = StudyOrganizationsSheet("", globals)
    mock_error.assert_called()
    assert mock_error.call_args[0][0] == "studyOrganizations"
    assert mock_error.call_args[0][1] == None
    assert mock_error.call_args[0][2] == None
    assert (
        mock_error.call_args[0][3]
        == "Exception. Error [Failed to detect column(s) 'organisationType, organizationType, type' in sheet] while reading sheet 'studyOrganizations'. See log for additional details."
    )


def test_address_error(mocker, globals):
    globals.cross_references.clear()
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Code_1", "Org_1", "Addr_1", "Id_1"]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        [
            "USGOV",
            "CT-GOV",
            "ClinicalTrials.gov",
            "Clinical Study Registry",
            "line|city|district|state|GBR",
        ],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=[
            "organisationIdentifierScheme",
            "organisationIdentifier",
            "organisationName",
            "organisationType",
            "organisationAddress",
        ],
    )
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
    ids = StudyOrganizationsSheet("", globals)
    mock_error.assert_called()
    assert mock_error.call_args[0][0] == "studyOrganizations"
    assert mock_error.call_args[0][1] == 1
    assert mock_error.call_args[0][2] == 5
    assert (
        mock_error.call_args[0][3]
        == "Address 'line|city|district|state|GBR' does not contain the required fields (lines, district, city, state, postal code and country code) using '|' separator characters, only 5 found"
    )
