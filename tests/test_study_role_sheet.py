import pandas as pd
from usdm_excel.study_role_sheet.study_role_sheet import StudyRoleSheet
from usdm_model.comment_annotation import CommentAnnotation
from usdm_model.organization import Organization
from usdm_excel.globals import Globals
from tests.test_factory import Factory


def test_create(factory, mocker, globals):
    data = {
        "name": ["AP1", "AP2", "AP3"],
        "description": ["Desc One", "Desc Two", "Desc Three"],
        "label": ["Lable 1", "L2", "L3"],
        "organizations": ["Sponsor 1", "Sponsor 2", ""],
        "people": ["", "", ""],
        "masking": ["Masking 1", "Masking 2", ""],
        "role": ["Investigator", "Sponsor", "Sponsor"],
    }

    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [
        "C_1",
        "C_2",
        "C_3",
        "O_1",
        "O_2",
        "O_3",
        "M_1",
        "C_4",
        "AP_1",
        "M_2",
        "C_5",
        "AP_2",
        "C_6",
        "AP_3",
    ]
    _setup(mocker, globals, data)
    _create_orgs(factory, globals)
    item = StudyRoleSheet("", globals)
    assert len(item.items) == 3
    assert item.items[0].model_dump() == {
        "id": "AP_1",
        "name": "AP1",
        "label": "Lable 1",
        "description": "Desc One",
        "code": {
            "id": "C_4",
            "code": "C25936",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Investigator",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
        "appliesToIds": [],
        "assignedPersons": [],
        "organizationIds": ["O_1"],
        "masking": {
            "id": "M_1",
            "text": "Masking 1",
            "isMasked": True,
            "extensionAttributes": [],
            "instanceType": "Masking",
        },
        "extensionAttributes": [],
        "notes": [],
        "instanceType": "StudyRole",
    }
    assert item.items[1].model_dump() == {
        "id": "AP_2",
        "name": "AP2",
        "label": "L2",
        "description": "Desc Two",
        "code": {
            "id": "C_5",
            "code": "C70793",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Sponsor",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
        "appliesToIds": [],
        "assignedPersons": [],
        "organizationIds": ["O_2"],
        "masking": {
            "id": "M_2",
            "text": "Masking 2",
            "isMasked": True,
            "extensionAttributes": [],
            "instanceType": "Masking",
        },
        "extensionAttributes": [],
        "notes": [],
        "instanceType": "StudyRole",
    }
    assert item.items[2].model_dump() == {
        "id": "AP_3",
        "name": "AP3",
        "label": "L3",
        "description": "Desc Three",
        "code": {
            "id": "C_6",
            "code": "C70793",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Sponsor",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
        "appliesToIds": [],
        "assignedPersons": [],
        "organizationIds": [],
        "masking": None,
        "extensionAttributes": [],
        "notes": [],
        "instanceType": "StudyRole",
    }


def test_notes(factory, mocker, globals):
    data = {
        "name": ["AP1"],
        "description": ["Desc One"],
        "label": ["Label 1"],
        "organizations": ["Sponsor 1"],
        "people": [""],
        "masking": ["Masking 1"],
        "role": ["Investigator"],
        "notes": ["N1"],
    }

    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [
        "C_1",
        "C_2",
        "C_3",
        "O_1",
        "O_2",
        "O_3",
        "N_1",
        "N_2",
        "N_3",
        "M_1",
        "C_4",
        "AP_1",
    ]
    _setup(mocker, globals, data)
    _create_orgs(factory, globals)
    _create_notes(factory, globals)
    item = StudyRoleSheet("", globals)
    assert len(item.items) == 1
    assert item.items[0].model_dump() == {
        "id": "AP_1",
        "name": "AP1",
        "label": "Label 1",
        "description": "Desc One",
        "code": {
            "id": "C_4",
            "code": "C25936",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Investigator",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
        "appliesToIds": [],
        "assignedPersons": [],
        "organizationIds": ["O_1"],
        "masking": {
            "id": "M_1",
            "text": "Masking 1",
            "isMasked": True,
            "extensionAttributes": [],
            "instanceType": "Masking",
        },
        "extensionAttributes": [],
        "notes": [
            {
                "codes": [],
                "extensionAttributes": [],
                "id": "N_1",
                "instanceType": "CommentAnnotation",
                "text": "Note 1",
            },
        ],
        "instanceType": "StudyRole",
    }


def test_create_empty(mocker, globals):
    data = {}
    _setup(mocker, globals, data)
    item = StudyRoleSheet("", globals)
    assert len(item.items) == 0


def test_read_cell_by_name_error(mocker, globals):
    data = {
        "name": ["AP1"],
        "description": ["Desc One"],
        "label": ["Lable 1"],
        "organizations": [""],
        "people": [""],
        "role": ["Investigator"],
    }
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Code_1", "Abbreviation_1"]
    _setup(mocker, globals, data)
    item = StudyRoleSheet("", globals)
    assert mock_error.call_count == 1
    mock_error.assert_has_calls(
        [
            mocker.call(
                "roles",
                1,
                -1,
                "Error attempting to read cell 'masking'. Exception: Failed to detect column(s) 'masking' in sheet",
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
            "type": factory.cdisc_code("C54149", "Pharmaceutical Company"),
            "identifier": "123456789",
            "identifierScheme": "DUNS",
            "legalAddress": None,
        },
        {
            "name": "Sponsor 2",
            "type": factory.cdisc_code("C54149", "Pharmaceutical Company"),
            "identifier": "222222222",
            "identifierScheme": "DUNS",
            "legalAddress": None,
        },
        {
            "name": "Sponsor 3",
            "type": factory.cdisc_code("C54149", "Pharmaceutical Company"),
            "identifier": "333333333",
            "identifierScheme": "DUNS",
            "legalAddress": None,
        },
    ]
    for item in items:
        org = factory.item(Organization, item)
        globals.cross_references.add(item["name"], org)


def _create_notes(factory: Factory, globals: Globals):
    notes = {
        "N1": {"text": "Note 1", "codes": []},
        "N2": {"text": "Note 2", "codes": []},
        "N3": {"text": "Note 3", "codes": []},
    }
    for name, note in notes.items():
        item = factory.item(CommentAnnotation, note)
        globals.cross_references.add(name, item)
