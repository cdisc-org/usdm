import pytest
import pandas as pd
from usdm_excel.study_design_objective_endpoint_sheet.study_design_objective_endpoint_sheet import (
    StudyDesignObjectiveEndpointSheet,
)
from usdm_model.api_base_model import ApiBaseModelWithId


xfail = pytest.mark.xfail


def test_create(mocker, globals):
    # mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    # mock_cross_ref.side_effect=[ApiBaseModelWithId(id="1"), ApiBaseModelWithId(id="2"), ApiBaseModelWithId(id="3"), ApiBaseModelWithId(id="4"), ApiBaseModelWithId(id="5")]
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [
        "Code_1",
        "Code_2",
        "ObjId_1",
        "EndId_1",
        "Code_3",
        "EndId_2",
        "Code_4",
        "Code_5",
        "ObjId_2",
        "EndId_3",
        "Code_6",
        "Code_7",
        "ObjId_3",
        "EndId_4",
        "Code_8",
        "EndId_5",
    ]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        [
            "Obj 1",
            "Obj Desc 1",
            "Obj Label 1",
            "Obj Text 1",
            "Trial Primary Objective",
            "End 1",
            "End Desc 1",
            "End Label 1",
            "End Text 1",
            "",
            "Primary Endpoint",
        ],
        [
            "",
            "",
            "",
            "",
            "",
            "End 2",
            "End Desc 2",
            "End Label 2",
            "End Text 2",
            "",
            "Primary Endpoint",
        ],
        [
            "Obj 2",
            "Obj Desc 2",
            "Obj Label 2",
            "Obj Text 2",
            "Trial Secondary Objective",
            "End 3",
            "End Desc 3",
            "End Label 3",
            "End Text 3",
            "",
            "Secondary Endpoint",
        ],
        [
            "Obj 3",
            "Obj Desc 3",
            "Obj Label 3",
            "Obj Text 3",
            "Trial Secondary Objective",
            "End 4",
            "End Desc 4",
            "End Label 4",
            "End Text 4",
            "",
            "Secondary Endpoint",
        ],
        [
            "",
            "",
            "",
            "",
            "",
            "End 5",
            "End Desc 5",
            "End Label 5",
            "End Text 5",
            "",
            "Secondary Endpoint",
        ],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=[
            "objectiveName",
            "objectiveDescription",
            "objectiveLabel",
            "objectiveText",
            "objectiveLevel",
            "endpointName",
            "endpointDescription",
            "endpointLabel",
            "endpointText",
            "endpointPurpose",
            "endpointLevel",
        ],
    )
    items = StudyDesignObjectiveEndpointSheet("", globals)
    assert len(items.objectives) == 3
    assert items.objectives[0].id == "ObjId_1"
    assert items.objectives[0].name == "Obj 1"
    assert items.objectives[0].description == "Obj Desc 1"
    assert items.objectives[0].label == "Obj Label 1"
    assert items.objectives[0].endpoints[0].name == "End 1"
    assert items.objectives[0].endpoints[1].name == "End 2"
    assert items.objectives[1].id == "ObjId_2"
    assert items.objectives[1].name == "Obj 2"
    assert items.objectives[1].endpoints[0].name == "End 3"
    assert items.objectives[2].id == "ObjId_3"
    assert items.objectives[2].name == "Obj 3"
    assert items.objectives[2].endpoints[0].name == "End 4"
    assert items.objectives[2].endpoints[1].name == "End 5"


def test_create_empty(mocker, globals):
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = []
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=[
            "objectiveName",
            "objectiveDescription",
            "objectiveLabel",
            "objectiveText",
            "objectiveLevel",
            "endpointName",
            "endpointDescription",
            "endpointLabel",
            "endpointText",
            "endpointPurpose",
            "endpointLevel",
        ],
    )
    items = StudyDesignObjectiveEndpointSheet("", globals)
    assert len(items.objectives) == 0


def test_read_cell_by_name_error(mocker, globals):
    call_parameters = []

    def my_add(sheet, row, column, message, level=10):
        call_parameters.append((sheet, row, column, message, level))
        return None

    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_error = mocker.patch(
        "usdm_excel.errors_and_logging.errors.Errors.add", side_effect=my_add
    )
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        [
            "Obj 1",
            "Obj Desc 1",
            "Obj Label 1",
            "Obj Text 1",
            "Primary Objective",
            "End 1",
            "End Desc 1",
            "End Label 1",
            "End Text Purpose 1",
            "Primary Endpoint",
        ]
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=[
            "objectiveName",
            "objectiveDescription",
            "objectiveLabel",
            "objectiveText",
            "objectiveLevel",
            "endpointName",
            "endpointDescription",
            "endpointLabel",
            "endpointPurpose",
            "endpointLevel",
        ],
    )
    items = StudyDesignObjectiveEndpointSheet("", globals)
    mock_error.assert_called()
    assert call_parameters[0] == (
        "studyDesignOE",
        1,
        -1,
        "Error attempting to read cell 'endpointText'. Exception: Failed to detect column(s) 'endpointText' in sheet",
        40,
    )
