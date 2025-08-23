import pandas as pd
from usdm_excel.study_design_sites_sheet.study_design_sites_sheet import (
    StudyDesignSitesSheet,
)
from usdm_model.code import Code
from usdm_model.organization import Organization
from tests.test_factory import Factory
from usdm_excel.globals import Globals


def test_create(mocker, globals):
    globals.cross_references.clear()
    _organizations(globals)
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Site_1", "Site_2", "Site_3"]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        ["Site1", "Site One", "Big Site", "GBR", "Sponsor1"],
        ["Site2", "Site Two", "Little Site", "FRA", "Sponsor2"],
        ["Site3", "Site Three", "Middle Site", "GER", "Sponsor3"],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=["name", "siteLabel", "siteDescription", "siteCountry", "organization"],
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
        decode="GER",
    )
    mock_code = mocker.patch("usdm_excel.iso_3166.ISO3166.code")
    mock_code.side_effect = [expected_1, expected_2, expected_3]
    sheet = StudyDesignSitesSheet("", globals)
    assert len(sheet.items) == 3
    assert sheet.items[0].model_dump() == {
        "country": {
            "code": "code",
            "codeSystem": "codesys",
            "codeSystemVersion": "3",
            "decode": "GBR",
            "id": "Code1",
            "instanceType": "Code",
            "extensionAttributes": [],
        },
        "description": "Big Site",
        "id": "Site_1",
        "instanceType": "StudySite",
        "label": "Site One",
        "name": "Site1",
        "extensionAttributes": [],
    }
    assert sheet.items[1].model_dump() == {
        "country": {
            "code": "code",
            "codeSystem": "codesys",
            "codeSystemVersion": "3",
            "decode": "FRA",
            "id": "Code2",
            "instanceType": "Code",
            "extensionAttributes": [],
        },
        "description": "Little Site",
        "id": "Site_2",
        "instanceType": "StudySite",
        "label": "Site Two",
        "name": "Site2",
        "extensionAttributes": [],
    }
    assert sheet.items[2].model_dump() == {
        "country": {
            "code": "code",
            "codeSystem": "codesys",
            "codeSystemVersion": "3",
            "decode": "GER",
            "id": "Code3",
            "instanceType": "Code",
            "extensionAttributes": [],
        },
        "description": "Middle Site",
        "id": "Site_3",
        "instanceType": "StudySite",
        "label": "Site Three",
        "name": "Site3",
        "extensionAttributes": [],
    }


def test_create_empty(mocker, globals):
    globals.cross_references.clear()
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = []
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=["name", "siteLabel", "siteDescription", "siteCountry", "organization"],
    )
    sites = StudyDesignSitesSheet("", globals)
    assert len(sites.items) == 0


def test_read_cell_by_name_error(mocker, globals):
    globals.cross_references.clear()
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [["Site1", "Site One", "Big Site", "Description", ""]]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=["name", "siteName", "siteLabel", "siteDescription", "organization"],
    )
    mock_json = mocker.patch("json.load")
    mock_json.return_value = {}
    sites = StudyDesignSitesSheet("", globals)
    mock_error.assert_called()
    assert mock_error.call_args[0][0] == "studyDesignSites"
    assert mock_error.call_args[0][1] == 1
    assert mock_error.call_args[0][2] == 5
    assert mock_error.call_args[0][3] == "No organization specified for site 'Site One'"


def _organizations(globals: Globals):
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
