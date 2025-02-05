import pytest
import pandas as pd
from usdm_excel.study_design_population_sheet.study_design_population_sheet import (
    StudyDesignPopulationSheet,
)
from usdm_model.characteristic import Characteristic

xfail = pytest.mark.xfail


def test_create(mocker, globals):
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [
        Characteristic(
            id="CH_1", name="CHAR_1", text="Something", instanceType="Characteristic"
        ),
        Characteristic(
            id="CH_2", name="CHAR_2", text="Something", instanceType="Characteristic"
        ),
        Characteristic(
            id="CH_3", name="CHAR_3", text="Something", instanceType="Characteristic"
        ),
    ]
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [
        "R_1",
        "R_2",
        "X_3",
        "R_4",
        "Code_5",
        "PopulationId_1",
        "X_7",
        "X_8",
        "X_9",
        "X_10",
        "X_11",
        "CohortId_1",
        "X_13",
        "X_14",
        "X_15",
        "X_16",
        "X_17",
        "CohortId_2",
        "X_18",
        "X_19",
        "X_20",
    ]
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        [
            "MAIN",
            "POP01",
            "Main pop",
            "Main Pop",
            "BOTH",
            "10..20",
            "100..110",
            "100..110 years",
            "Y",
            "",
        ],
        [
            "COHORT",
            "POP02",
            "Cohort 1",
            "Cohort 1",
            "MALE",
            "5..10",
            "50..50",
            "50..50 years",
            "Y",
            "CHAR_1, CHAR_2",
        ],
        [
            "COHORT",
            "POP03",
            "Cohort 2",
            "Cohort 2",
            "FEMALE",
            "5..10",
            "50..60",
            "50..60 years",
            "Y",
            "CHAR_3",
        ],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=[
            "level",
            "name",
            "description",
            "label",
            "plannedSexOfParticipants",
            "plannedCompletionNumber",
            "plannedEnrollmentNumber",
            "plannedAge",
            "includesHealthySubjects",
            "characteristics",
        ],
    )
    item = StudyDesignPopulationSheet("", globals)
    assert item.population.model_dump() == {
        "cohorts": [
            {
                "characteristics": [
                    {
                        "description": None,
                        "dictionaryId": None,
                        "id": "CH_1",
                        "instanceType": "Characteristic",
                        "label": None,
                        "name": "CHAR_1",
                        "notes": [],
                        "text": "Something",
                    },
                    {
                        "description": None,
                        "dictionaryId": None,
                        "id": "CH_2",
                        "instanceType": "Characteristic",
                        "label": None,
                        "name": "CHAR_2",
                        "notes": [],
                        "text": "Something",
                    },
                ],
                "criterionIds": [],
                "description": "Cohort 1",
                "id": "X_14",
                "includesHealthySubjects": True,
                "instanceType": "StudyCohort",
                "label": "Cohort 1",
                "name": "POP02",
                "notes": [],
                "plannedAge": {
                    "id": "CohortId_1",
                    "instanceType": "Range",
                    "isApproximate": False,
                    "maxValue": 50.0,
                    "minValue": 50.0,
                    "unit": {
                        "id": "X_11",
                        "instanceType": "AliasCode",
                        "standardCode": {
                            "code": "C29848",
                            "codeSystem": "http://www.cdisc.org",
                            "codeSystemVersion": "2024-09-27",
                            "decode": "Year",
                            "id": "X_10",
                            "instanceType": "Code",
                        },
                        "standardCodeAliases": [],
                    },
                },
                "plannedCompletionNumber": {
                    "id": "X_8",
                    "instanceType": "Range",
                    "isApproximate": False,
                    "maxValue": 10.0,
                    "minValue": 5.0,
                    "unit": None,
                },
                "plannedEnrollmentNumber": {
                    "id": "X_9",
                    "instanceType": "Range",
                    "isApproximate": False,
                    "maxValue": 50.0,
                    "minValue": 50.0,
                    "unit": None,
                },
                "plannedSex": [
                    {
                        "code": "C20197",
                        "codeSystem": "http://www.cdisc.org",
                        "codeSystemVersion": "2024-09-27",
                        "decode": "Male",
                        "id": "X_13",
                        "instanceType": "Code",
                    },
                ],
            },
            {
                "characteristics": [
                    {
                        "description": None,
                        "dictionaryId": None,
                        "id": "CH_3",
                        "instanceType": "Characteristic",
                        "label": None,
                        "name": "CHAR_3",
                        "notes": [],
                        "text": "Something",
                    },
                ],
                "criterionIds": [],
                "description": "Cohort 2",
                "id": "X_20",
                "includesHealthySubjects": True,
                "instanceType": "StudyCohort",
                "label": "Cohort 2",
                "name": "POP03",
                "notes": [],
                "plannedAge": {
                    "id": "X_18",
                    "instanceType": "Range",
                    "isApproximate": False,
                    "maxValue": 60.0,
                    "minValue": 50.0,
                    "unit": {
                        "id": "CohortId_2",
                        "instanceType": "AliasCode",
                        "standardCode": {
                            "code": "C29848",
                            "codeSystem": "http://www.cdisc.org",
                            "codeSystemVersion": "2024-09-27",
                            "decode": "Year",
                            "id": "X_17",
                            "instanceType": "Code",
                        },
                        "standardCodeAliases": [],
                    },
                },
                "plannedCompletionNumber": {
                    "id": "X_15",
                    "instanceType": "Range",
                    "isApproximate": False,
                    "maxValue": 10.0,
                    "minValue": 5.0,
                    "unit": None,
                },
                "plannedEnrollmentNumber": {
                    "id": "X_16",
                    "instanceType": "Range",
                    "isApproximate": False,
                    "maxValue": 60.0,
                    "minValue": 50.0,
                    "unit": None,
                },
                "plannedSex": [
                    {
                        "code": "C16576",
                        "codeSystem": "http://www.cdisc.org",
                        "codeSystemVersion": "2024-09-27",
                        "decode": "Female",
                        "id": "X_19",
                        "instanceType": "Code",
                    },
                ],
            },
        ],
        "criterionIds": [],
        "description": "Main pop",
        "id": "X_7",
        "includesHealthySubjects": True,
        "instanceType": "StudyDesignPopulation",
        "label": "Main Pop",
        "name": "POP01",
        "notes": [],
        "plannedAge": {
            "id": "Code_5",
            "instanceType": "Range",
            "isApproximate": False,
            "maxValue": 110.0,
            "minValue": 100.0,
            "unit": {
                "id": "R_4",
                "instanceType": "AliasCode",
                "standardCode": {
                    "code": "C29848",
                    "codeSystem": "http://www.cdisc.org",
                    "codeSystemVersion": "2024-09-27",
                    "decode": "Year",
                    "id": "X_3",
                    "instanceType": "Code",
                },
                "standardCodeAliases": [],
            },
        },
        "plannedCompletionNumber": {
            "id": "R_1",
            "instanceType": "Range",
            "isApproximate": False,
            "maxValue": 20.0,
            "minValue": 10.0,
            "unit": None,
        },
        "plannedEnrollmentNumber": {
            "id": "R_2",
            "instanceType": "Range",
            "isApproximate": False,
            "maxValue": 110.0,
            "minValue": 100.0,
            "unit": None,
        },
        "plannedSex": [
            {
                "code": "C49636",
                "codeSystem": "http://www.cdisc.org",
                "codeSystemVersion": "2024-09-27",
                "decode": "Both",
                "id": "PopulationId_1",
                "instanceType": "Code",
            },
        ],
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
    items = StudyDesignPopulationSheet("", globals)
    assert items.population == None


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
            "MAIN",
            "POP01",
            "Main pop",
            "Main Pop",
            "10..20",
            "100..110",
            "100..110 years",
            "Y",
            "",
        ]
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(
        data,
        columns=[
            "level",
            "name",
            "description",
            "label",
            "plannedCompletionNumber",
            "plannedEnrollmentNumber",
            "plannedAge",
            "includesHealthySubjects",
            "characteristics",
        ],
    )
    items = StudyDesignPopulationSheet("", globals)
    mock_error.assert_called()
    assert call_parameters == [
        (
            "studyDesignPopulations",
            None,
            None,
            "Exception. Error [Failed to detect column(s) 'plannedSexOfParticipants' in sheet] while reading sheet 'studyDesignPopulations'. See log for additional details.",
            40,
        )
    ]
