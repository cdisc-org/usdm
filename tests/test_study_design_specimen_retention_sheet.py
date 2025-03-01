import pytest
import pandas as pd
from usdm_excel.study_design_specimen_retention_sheet.study_design_specimen_retention_sheet import (
    StudyDesignSpecimenRetentionSheet,
)
from usdm_excel.globals import Globals
from tests.test_factory import Factory

xfail = pytest.mark.xfail


def test_create(mocker, globals):
    data = {
        "name": ["A1", "A2", "A3"],
        "description": [
            "Annotation Text One",
            "Annotation Text Two",
            "Annotation Text Three",
        ],
        "label": ["LABEL1", "LABEL2", "LABEL3"],
        "retained": [True, False, True],
        "includesDNA": [True, False, True],
    }
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [
        "BiospecimenRetention_1",
        "BiospecimenRetention_2",
        "BiospecimenRetention_3",
    ]
    _setup(mocker, globals, data)
    item = StudyDesignSpecimenRetentionSheet("", globals)
    assert len(item.items) == 3
    assert item.items[0].model_dump() == {
        "id": "BiospecimenRetention_1",
        "extensionAttributes": [],
        "instanceType": "BiospecimenRetention",
        "name": "A1",
        "description": "Annotation Text One",
        "label": "LABEL1",
        "isRetained": True,
        "includesDNA": True,
    }
    assert item.items[1].model_dump() == {
        "id": "BiospecimenRetention_2",
        "extensionAttributes": [],
        "instanceType": "BiospecimenRetention",
        "name": "A2",
        "description": "Annotation Text Two",
        "label": "LABEL2",
        "isRetained": False,
        "includesDNA": False,
    }
    assert item.items[2].model_dump() == {
        "id": "BiospecimenRetention_3",
        "extensionAttributes": [],
        "instanceType": "BiospecimenRetention",
        "name": "A3",
        "description": "Annotation Text Three",
        "label": "LABEL3",
        "isRetained": True,
        "includesDNA": True,
    }


def test_create_empty(mocker, globals):
    data = {}
    _setup(mocker, globals, data)
    item = StudyDesignSpecimenRetentionSheet("", globals)
    assert len(item.items) == 0


def test_read_cell_by_name_error(mocker, globals):
    data = {
        "name": ["A1"],
        "description": ["Annotation Text One"],
        "label": ["LABEL1"],
        "includesDNA": [True],
    }
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Code_1", "BiospecimenRetention_1"]
    _setup(mocker, globals, data)
    item = StudyDesignSpecimenRetentionSheet("", globals)
    assert mock_error.call_count == 1
    mock_error.assert_has_calls(
        [
            mocker.call(
                "studyDesignSpecimen",
                1,
                -1,
                "Error attempting to read cell 'retained'. Exception: Failed to detect column(s) 'retained' in sheet",
                40,
            ),
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
