from tests.mocks.mock_general import *
from tests.mocks.mock_sheet import *
from tests.mocks.mock_ids import *
from tests.mocks.mock_logging import *
from usdm_excel.study_design_estimands_sheet.study_design_estimands_sheet import (
    StudyDesignEstimandsSheet,
)
from usdm_model.api_base_model import ApiBaseModelWithIdAndName


def test_create(mocker, globals):
    sheet_data = {
        "name": ["ESTIMAND1", "ESTIMAND2", "ESTIMAND3"],
        "summaryMeasure": ["Survival 1", "Survival 2", "Survival 3"],
        "populationDescription": ["P Desc 1", "P Desc 2", "P Desc 3"],
        "populationSubset": ["POP1", "POP2", "POP3"],
        "intercurrentEventName": ["IE Name 1", "IE Name 2", "IE Name 3"],
        "intercurrentEventDescription": ["IE Desc 1", "IE Desc 2", "IE Desc 3"],
        "treatmentXref": ["INT1", "INT2", "INT3"],
        "endpointXref": ["END1", "END2", "END3"],
        "intercurrentEventStrategy": ["Strategy 1", "Strategy 2", "Strategy 3"],
        "intercurrentEventText": [
            "Strategy Text 1",
            "Strategy Text 2",
            "Strategy Text 3",
        ],
    }
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [
        ApiBaseModelWithIdAndName(id="X1", name="POP1"),
        ApiBaseModelWithIdAndName(id="X2", name="INT1"),
        ApiBaseModelWithIdAndName(id="X3", name="END1"),
        ApiBaseModelWithIdAndName(id="X4", name="POP2"),
        ApiBaseModelWithIdAndName(id="X5", name="INT2"),
        ApiBaseModelWithIdAndName(id="X6", name="END2"),
        ApiBaseModelWithIdAndName(id="X7", name="POP3"),
        ApiBaseModelWithIdAndName(id="X8", name="INT3"),
        ApiBaseModelWithIdAndName(id="X9", name="END3"),
    ]
    mock_sheet_present(mocker)
    mock_sheet(mocker, globals, sheet_data)
    item = StudyDesignEstimandsSheet("", globals)
    assert len(item.estimands) == 3
    assert len(item.populations) == 3
    assert item.estimands[0].model_dump() == {
        "analysisPopulationId": "AnalysisPopulation_1",
        "description": "",
        "id": "Estimand_1",
        "instanceType": "Estimand",
        "intercurrentEvents": [
            {
                "description": "IE Desc 1",
                "dictionaryId": None,
                "id": "IntercurrentEvent_1",
                "instanceType": "IntercurrentEvent",
                "label": "",
                "name": "IE Name 1",
                "notes": [],
                "strategy": "Strategy 1",
                "text": "Strategy Text 1",
                "extensionAttributes": [],
            },
        ],
        "interventionIds": ["X2"],
        "label": "ESTIMAND1",
        "name": "ESTIMAND1",
        "notes": [],
        "populationSummary": "Survival 1",
        "variableOfInterestId": "X3",
        "extensionAttributes": [],
    }
    assert item.populations[0].model_dump() == {
        "description": None,
        "id": "AnalysisPopulation_1",
        "instanceType": "AnalysisPopulation",
        "label": None,
        "name": "AP_1",
        "notes": [],
        "subsetOfIds": ["X1"],
        "text": "P Desc 1",
        "extensionAttributes": [],
    }
    assert item.estimands[1].model_dump() == {
        "analysisPopulationId": "AnalysisPopulation_2",
        "description": "",
        "id": "Estimand_2",
        "instanceType": "Estimand",
        "intercurrentEvents": [
            {
                "description": "IE Desc 2",
                "dictionaryId": None,
                "id": "IntercurrentEvent_2",
                "instanceType": "IntercurrentEvent",
                "label": "",
                "name": "IE Name 2",
                "notes": [],
                "strategy": "Strategy 2",
                "text": "Strategy Text 2",
                "extensionAttributes": [],
            },
        ],
        "interventionIds": ["X5"],
        "label": "ESTIMAND2",
        "name": "ESTIMAND2",
        "notes": [],
        "populationSummary": "Survival 2",
        "variableOfInterestId": "X6",
        "extensionAttributes": [],
    }
    assert item.populations[1].model_dump() == {
        "description": None,
        "id": "AnalysisPopulation_2",
        "instanceType": "AnalysisPopulation",
        "label": None,
        "name": "AP_2",
        "notes": [],
        "subsetOfIds": ["X4"],
        "text": "P Desc 2",
        "extensionAttributes": [],
    }
    assert item.estimands[2].model_dump() == {
        "analysisPopulationId": "AnalysisPopulation_3",
        "description": "",
        "id": "Estimand_3",
        "instanceType": "Estimand",
        "intercurrentEvents": [
            {
                "description": "IE Desc 3",
                "dictionaryId": None,
                "id": "IntercurrentEvent_3",
                "instanceType": "IntercurrentEvent",
                "label": "",
                "name": "IE Name 3",
                "notes": [],
                "strategy": "Strategy 3",
                "text": "Strategy Text 3",
                "extensionAttributes": [],
            },
        ],
        "interventionIds": ["X8"],
        "label": "ESTIMAND3",
        "name": "ESTIMAND3",
        "notes": [],
        "populationSummary": "Survival 3",
        "variableOfInterestId": "X9",
        "extensionAttributes": [],
    }
    assert item.populations[2].model_dump() == {
        "description": None,
        "id": "AnalysisPopulation_3",
        "instanceType": "AnalysisPopulation",
        "label": None,
        "name": "AP_3",
        "notes": [],
        "subsetOfIds": ["X7"],
        "text": "P Desc 3",
        "extensionAttributes": [],
    }


def test_create_empty(mocker, globals):
    sheet_data = {}
    mock_sheet_present(mocker)
    mock_sheet(mocker, globals, sheet_data)
    item = StudyDesignEstimandsSheet("", globals)
    assert len(item.estimands) == 0
    assert len(item.populations) == 0


def test_read_cell_by_name_error(mocker, globals):
    sheet_data = {
        "name": ["ESTIMAND1"],
        "summaryMeasure": ["Survival 1"],
        "populationDescription": ["P Desc 1"],
        "intercurrentEventName": ["IE Name 1"],
        "intercurrentEventDescription": ["IE Desc 1"],
        "treatmentXref": ["INT1"],
        "endpointXref": ["END1"],
        "intercurrentEventStrategy": ["Strategy 1"],
        "intercurrentEventText": ["Strategy Text 1"],
    }
    mea = mock_error_add(mocker, [None, None, None, None, None, None])
    mock_sheet_present(mocker)
    mock_sheet(mocker, globals, sheet_data)
    item = StudyDesignEstimandsSheet("", globals)
    assert mock_called(mea, 3)
    mock_parameters_correct(
        mea,
        [
            mocker.call(
                "studyDesignEstimands",
                1,
                -1,
                "Error attempting to read cell 'populationSubset'. Exception: Failed to detect column(s) 'populationSubset' in sheet",
                40,
            ),
            mocker.call(
                "studyDesignEstimands",
                None,
                None,
                "Unable to find population or cohort with name ''",
                40,
            ),
            mocker.call(
                "studyDesignEstimands",
                None,
                None,
                "Failed to add IntercurrentEvent, no Estimand set",
                40,
            ),
        ],
    )
