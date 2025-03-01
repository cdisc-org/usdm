import pytest
import pandas as pd
from usdm_excel.study_design_eligibility_criteria_sheet.study_design_eligibility_criteria_sheet import (
    StudyDesignEligibilityCriteriaSheet,
)
from usdm_model.code import Code


xfail = pytest.mark.xfail


def test_create(mocker, globals):
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [
        "Code_1",
        "EligibilityItemId_1",
        "EligibilityId_1",
        "Code_2",
        "EligibilityItemId_2",
        "EligibilityId_2",
        "Code_3",
        "EligibilityItemId_3",
        "EligibilityId_3",
    ]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        [
            "Inclusion",
            "01",
            "INC01",
            "The study age criterion",
            "Age critierion",
            "Subjects should be between 18 and 45 years old",
            "dictionary",
        ],
        [
            "Inclusion",
            "02",
            "INC01",
            "The study abc criterion",
            "ABC critierion",
            "Subjects should have ABC",
            "dictionary",
        ],
        [
            "Exclusion",
            "01",
            "EXC01",
            "Exclude those with all fingers",
            "Fingers critierion",
            "Subjects should not have all fingers",
            "dictionary",
        ],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=[
            "category",
            "identifier",
            "name",
            "description",
            "label",
            "text",
            "dictionary",
        ],
    )
    items = StudyDesignEligibilityCriteriaSheet("", globals)
    assert len(items.items) == 3
    assert items.items[0].model_dump() == {
        "id": "EligibilityId_1",
        "name": "INC01",
        "description": "The study age criterion",
        "label": "Age critierion",
        "criterionItemId": "EligibilityItemId_1",
        "category": {
            "code": "C25532",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Inclusion Criteria",
            "id": "Code_1",
            "instanceType": "Code",
            "extensionAttributes": [],
        },
        "identifier": "01",
        "nextId": None,
        "previousId": None,
        "notes": [],
        "instanceType": "EligibilityCriterion",
        "extensionAttributes": [],
    }
    assert items.criterion_items[0].model_dump() == {
        "id": "EligibilityItemId_1",
        "text": "Subjects should be between 18 and 45 years old",
        "dictionaryId": None,
        "instanceType": "EligibilityCriterionItem",
        "name": "INC01",
        "label": None,
        "description": None,
        "notes": [],
        "extensionAttributes": [],
    }
    assert items.items[1].model_dump() == {
        "id": "EligibilityId_2",
        "name": "INC01",
        "description": "The study abc criterion",
        "label": "ABC critierion",
        "criterionItemId": "EligibilityItemId_2",
        "category": {
            "code": "C25532",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Inclusion Criteria",
            "id": "Code_2",
            "instanceType": "Code",
            "extensionAttributes": [],
        },
        "identifier": "02",
        "nextId": None,
        "previousId": None,
        "notes": [],
        "instanceType": "EligibilityCriterion",
        "extensionAttributes": [],
    }
    assert items.criterion_items[1].model_dump() == {
        "id": "EligibilityItemId_2",
        "text": "Subjects should have ABC",
        "dictionaryId": None,
        "instanceType": "EligibilityCriterionItem",
        "name": "INC01",
        "label": None,
        "description": None,
        "notes": [],
        "extensionAttributes": [],
    }
    assert items.items[2].model_dump() == {
        "id": "EligibilityId_3",
        "name": "EXC01",
        "description": "Exclude those with all fingers",
        "label": "Fingers critierion",
        "criterionItemId": "EligibilityItemId_3",
        "category": {
            "code": "C25370",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Exclusion Criteria",
            "id": "Code_3",
            "instanceType": "Code",
            "extensionAttributes": [],
        },
        "identifier": "01",
        "nextId": None,
        "previousId": None,
        "notes": [],
        "instanceType": "EligibilityCriterion",
        "extensionAttributes": [],
    }
    assert items.criterion_items[2].model_dump() == {
        "id": "EligibilityItemId_3",
        "text": "Subjects should not have all fingers",
        "dictionaryId": None,
        "instanceType": "EligibilityCriterionItem",
        "name": "EXC01",
        "label": None,
        "description": None,
        "notes": [],
        "extensionAttributes": [],
    }


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
            "category",
            "identifier",
            "name",
            "description",
            "label",
            "text",
            "dictionary",
        ],
    )
    items = StudyDesignEligibilityCriteriaSheet("", globals)
    assert len(items.items) == 0


def test_read_cell_by_name_error(mocker, globals):
    globals.cross_references.clear()
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
            "Inclusion",
            "01",
            "The study age criterion",
            "Age critierion",
            "Subjects should be between 18 and 45 years old",
            "dictionary",
        ]
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data, columns=["category", "identifier", "name", "label", "text", "dictionary"]
    )
    items = StudyDesignEligibilityCriteriaSheet("", globals)
    mock_error.assert_called()
    assert call_parameters == [
        (
            "studyDesignEligibilityCriteria",
            1,
            -1,
            "Error attempting to read cell 'description'. Exception: Failed to detect column(s) 'description' in sheet",
            40,
        ),
        (
            "studyDesignEligibilityCriteria",
            1,
            5,
            "Dictionary 'dictionary' not found",
            30,
        ),
        (
            "studyDesignEligibilityCriteria",
            None,
            None,
            "Unable to find dictionary with name 'dictionary'",
            40,
        ),
    ]
