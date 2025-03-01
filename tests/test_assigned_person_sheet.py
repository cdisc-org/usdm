import pytest
import pandas as pd
from usdm_excel.assigned_person_sheet.assigned_person_sheet import AssignedPersonSheet
from usdm_model.organization import Organization
from usdm_excel.globals import Globals
from tests.test_factory import Factory

xfail = pytest.mark.xfail


def test_create(factory, mocker, globals):
    data = {
        "name": ["AP1", "AP2", "AP3"],
        "description": ["Desc One", "Desc Two", "Desc Three"],
        "label": ["Lable 1", "L2", "L3"],
        "jobTitle": ["Title 1", "Title 2", "Title 3"],
        "organization": ["Sponsor 1", "Sponsor 2", ""],
    }
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [
        "C_1",
        "C_2",
        "C_3",
        "O_1",
        "O_2",
        "O_3",
        "AP_1",
        "AP_2",
        "AP_3",
        "X_4",
        "X_5",
    ]
    _setup(mocker, globals, data)
    _create_orgs(factory, globals)
    item = AssignedPersonSheet("", globals)
    assert len(item.items) == 3
    assert item.items[0].model_dump() == {
        "id": "AP_1",
        "extensionAttributes": [],
        "name": "AP1",
        "label": "Lable 1",
        "description": "Desc One",
        "jobTitle": "Title 1",
        "organizationId": "O_1",
        "instanceType": "AssignedPerson",
    }
    assert item.items[1].model_dump() == {
        "id": "AP_2",
        "extensionAttributes": [],
        "name": "AP2",
        "label": "L2",
        "description": "Desc Two",
        "jobTitle": "Title 2",
        "organizationId": "O_2",
        "instanceType": "AssignedPerson",
    }
    assert item.items[2].model_dump() == {
        "id": "AP_3",
        "extensionAttributes": [],
        "name": "AP3",
        "label": "L3",
        "description": "Desc Three",
        "jobTitle": "Title 3",
        "organizationId": None,
        "instanceType": "AssignedPerson",
    }


def test_create_empty(mocker, globals):
    data = {}
    _setup(mocker, globals, data)
    item = AssignedPersonSheet("", globals)
    assert len(item.items) == 0


def test_read_cell_by_name_error(mocker, globals):
    data = {
        "name": ["AP1"],
        "description": ["Desc One"],
        "label": ["Lable 1"],
        "organization": [""],
    }
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Code_1", "Abbreviation_1"]
    _setup(mocker, globals, data)
    item = AssignedPersonSheet("", globals)
    assert mock_error.call_count == 1
    mock_error.assert_has_calls(
        [
            mocker.call(
                "people",
                1,
                -1,
                "Error attempting to read cell 'jobTitle'. Exception: Failed to detect column(s) 'jobTitle' in sheet",
                40,
            )
        ]
    )


def _setup(mocker, globals, data):
    globals.cross_references.clear()
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)


def _create_orgs(factory: Factory, globals: Globals):
    items = [
        {
            "name": "Sponsor 1",
            "type": factory.cdisc_code("C70793", "sponsor"),
            "identifier": "123456789",
            "identifierScheme": "DUNS",
            "legalAddress": None,
        },
        {
            "name": "Sponsor 2",
            "type": factory.cdisc_code("C70793", "sponsor"),
            "identifier": "222222222",
            "identifierScheme": "DUNS",
            "legalAddress": None,
        },
        {
            "name": "Sponsor 3",
            "type": factory.cdisc_code("C70793", "sponsor"),
            "identifier": "333333333",
            "identifierScheme": "DUNS",
            "legalAddress": None,
        },
    ]
    for item in items:
        org = factory.item(Organization, item)
        globals.cross_references.add(item["name"], org)
