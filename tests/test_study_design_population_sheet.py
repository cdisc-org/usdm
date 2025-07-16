import pytest
import pandas as pd
from usdm_excel.study_design_population_sheet.study_design_population_sheet import (
    StudyDesignPopulationSheet,
)
from usdm_model.characteristic import Characteristic
from usdm_model.indication import Indication

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
        Indication(
            id="I_1", name="IND_1", isRareDisease=False, instanceType="Indication"
        ),
        Indication(
            id="I_2", name="IND_2", isRareDisease=False, instanceType="Indication"
        ),
        Characteristic(
            id="CH_3", name="CHAR_3", text="Something", instanceType="Characteristic"
        ),
        Indication(
            id="I_1", name="IND_1", isRareDisease=False, instanceType="Indication"
        ),
    ]
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [
        "X_1",
        "X_2",
        "X_3",
        "X_4",
        "X_5",
        "X_6",
        "X_7",
        "X_8",
        "X_9",
        "X_10",
        "X_11",
        "X_12",
        "X_13",
        "X_14",
        "X_15",
        "X_16",
        "X_17",
        "X_18",
        "X_19",
        "X_20",
        "X_21",
        "X_22",
        "X_23",
        "X_24",
        "X_25",
        "X_26",
        "X_27",
        "X_28",
        "X_29",
        "X_30",
        "X_31",
        "X_32",
        "X_33",
        "X_34",
        "X_35",
        "X_36",
        "X_37",
        "X_38",
        "X_39",
        "X_40",
        "X_41",
        "X_42",
        "X_43",
        "X_44",
        "X_45",
        "X_46",
        "X_47",
        "X_48",
        "X_49",
        "X_50",
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
            "IND_1, IND_2",
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
            "IND_1",
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
            "indications",
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
                        "extensionAttributes": [],
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
                        "extensionAttributes": [],
                        "instanceType": "Characteristic",
                        "label": None,
                        "name": "CHAR_2",
                        "notes": [],
                        "text": "Something",
                    },
                ],
                "indicationIds": ["I_1", "I_2"],
                "criterionIds": [],
                "description": "Cohort 1",
                "id": "X_30",
                "includesHealthySubjects": True,
                "extensionAttributes": [],
                "instanceType": "StudyCohort",
                "label": "Cohort 1",
                "name": "POP02",
                "notes": [],
                "plannedAge": {
                    "id": "X_28",
                    "extensionAttributes": [],
                    "instanceType": "Range",
                    "isApproximate": False,
                    "maxValue": {
                        "id": "X_27",
                        "value": 50.0,
                        "unit": {
                            "id": "X_25",
                            "extensionAttributes": [],
                            "instanceType": "AliasCode",
                            "standardCode": {
                                "code": "C29848",
                                "codeSystem": "http://www.cdisc.org",
                                "codeSystemVersion": "2024-09-27",
                                "decode": "Year",
                                "id": "X_23",
                                "extensionAttributes": [],
                                "instanceType": "Code",
                            },
                            "standardCodeAliases": [],
                        },
                        "extensionAttributes": [],
                        "instanceType": "Quantity",
                    },
                    "minValue": {
                        "id": "X_26",
                        "value": 50.0,
                        "unit": {
                            "id": "X_24",
                            "extensionAttributes": [],
                            "instanceType": "AliasCode",
                            "standardCode": {
                                "code": "C29848",
                                "codeSystem": "http://www.cdisc.org",
                                "codeSystemVersion": "2024-09-27",
                                "decode": "Year",
                                "id": "X_22",
                                "extensionAttributes": [],
                                "instanceType": "Code",
                            },
                            "standardCodeAliases": [],
                        },
                        "extensionAttributes": [],
                        "instanceType": "Quantity",
                    },
                },
                "plannedCompletionNumber": {
                    "id": "X_18",
                    "extensionAttributes": [],
                    "instanceType": "Range",
                    "isApproximate": False,
                    "maxValue": {
                        "id": "X_17",
                        "value": 10.0,
                        "unit": None,
                        "extensionAttributes": [],
                        "instanceType": "Quantity",
                    },
                    "minValue": {
                        "id": "X_16",
                        "value": 5.0,
                        "unit": None,
                        "extensionAttributes": [],
                        "instanceType": "Quantity",
                    },
                },
                "plannedEnrollmentNumber": {
                    "id": "X_21",
                    "extensionAttributes": [],
                    "instanceType": "Range",
                    "isApproximate": False,
                    "maxValue": {
                        "id": "X_20",
                        "value": 50.0,
                        "unit": None,
                        "extensionAttributes": [],
                        "instanceType": "Quantity",
                    },
                    "minValue": {
                        "id": "X_19",
                        "value": 50.0,
                        "unit": None,
                        "extensionAttributes": [],
                        "instanceType": "Quantity",
                    },
                },
                "plannedSex": [
                    {
                        "code": "C20197",
                        "codeSystem": "http://www.cdisc.org",
                        "codeSystemVersion": "2024-09-27",
                        "decode": "Male",
                        "id": "X_29",
                        "extensionAttributes": [],
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
                        "extensionAttributes": [],
                        "instanceType": "Characteristic",
                        "label": None,
                        "name": "CHAR_3",
                        "notes": [],
                        "text": "Something",
                    },
                ],
                "indicationIds": ["I_1"],
                "criterionIds": [],
                "description": "Cohort 2",
                "id": "X_45",
                "includesHealthySubjects": True,
                "extensionAttributes": [],
                "instanceType": "StudyCohort",
                "label": "Cohort 2",
                "name": "POP03",
                "notes": [],
                "plannedAge": {
                    "id": "X_43",
                    "extensionAttributes": [],
                    "instanceType": "Range",
                    "isApproximate": False,
                    "maxValue": {
                        "id": "X_42",
                        "value": 60.0,
                        "unit": {
                            "id": "X_40",
                            "extensionAttributes": [],
                            "instanceType": "AliasCode",
                            "standardCode": {
                                "code": "C29848",
                                "codeSystem": "http://www.cdisc.org",
                                "codeSystemVersion": "2024-09-27",
                                "decode": "Year",
                                "id": "X_38",
                                "extensionAttributes": [],
                                "instanceType": "Code",
                            },
                            "standardCodeAliases": [],
                        },
                        "extensionAttributes": [],
                        "instanceType": "Quantity",
                    },
                    "minValue": {
                        "id": "X_41",
                        "value": 50.0,
                        "unit": {
                            "id": "X_39",
                            "extensionAttributes": [],
                            "instanceType": "AliasCode",
                            "standardCode": {
                                "code": "C29848",
                                "codeSystem": "http://www.cdisc.org",
                                "codeSystemVersion": "2024-09-27",
                                "decode": "Year",
                                "id": "X_37",
                                "extensionAttributes": [],
                                "instanceType": "Code",
                            },
                            "standardCodeAliases": [],
                        },
                        "extensionAttributes": [],
                        "instanceType": "Quantity",
                    },
                },
                "plannedCompletionNumber": {
                    "id": "X_33",
                    "extensionAttributes": [],
                    "instanceType": "Range",
                    "isApproximate": False,
                    "maxValue": {
                        "id": "X_32",
                        "value": 10.0,
                        "unit": None,
                        "extensionAttributes": [],
                        "instanceType": "Quantity",
                    },
                    "minValue": {
                        "id": "X_31",
                        "value": 5.0,
                        "unit": None,
                        "extensionAttributes": [],
                        "instanceType": "Quantity",
                    },
                },
                "plannedEnrollmentNumber": {
                    "id": "X_36",
                    "extensionAttributes": [],
                    "instanceType": "Range",
                    "isApproximate": False,
                    "maxValue": {
                        "id": "X_35",
                        "value": 60.0,
                        "unit": None,
                        "extensionAttributes": [],
                        "instanceType": "Quantity",
                    },
                    "minValue": {
                        "id": "X_34",
                        "value": 50.0,
                        "unit": None,
                        "extensionAttributes": [],
                        "instanceType": "Quantity",
                    },
                },
                "plannedSex": [
                    {
                        "code": "C16576",
                        "codeSystem": "http://www.cdisc.org",
                        "codeSystemVersion": "2024-09-27",
                        "decode": "Female",
                        "id": "X_44",
                        "extensionAttributes": [],
                        "instanceType": "Code",
                    },
                ],
            },
        ],
        "criterionIds": [],
        "description": "Main pop",
        "id": "X_15",
        "includesHealthySubjects": True,
        "extensionAttributes": [],
        "instanceType": "StudyDesignPopulation",
        "label": "Main Pop",
        "name": "POP01",
        "notes": [],
        "plannedAge": {
            "id": "X_13",
            "extensionAttributes": [],
            "instanceType": "Range",
            "isApproximate": False,
            "maxValue": {
                "id": "X_12",
                "value": 110.0,
                "unit": {
                    "id": "X_10",
                    "extensionAttributes": [],
                    "instanceType": "AliasCode",
                    "standardCode": {
                        "code": "C29848",
                        "codeSystem": "http://www.cdisc.org",
                        "codeSystemVersion": "2024-09-27",
                        "decode": "Year",
                        "id": "X_8",
                        "extensionAttributes": [],
                        "instanceType": "Code",
                    },
                    "standardCodeAliases": [],
                },
                "extensionAttributes": [],
                "instanceType": "Quantity",
            },
            "minValue": {
                "id": "X_11",
                "value": 100.0,
                "unit": {
                    "id": "X_9",
                    "extensionAttributes": [],
                    "instanceType": "AliasCode",
                    "standardCode": {
                        "code": "C29848",
                        "codeSystem": "http://www.cdisc.org",
                        "codeSystemVersion": "2024-09-27",
                        "decode": "Year",
                        "id": "X_7",
                        "extensionAttributes": [],
                        "instanceType": "Code",
                    },
                    "standardCodeAliases": [],
                },
                "extensionAttributes": [],
                "instanceType": "Quantity",
            },
        },
        "plannedCompletionNumber": {
            "id": "X_3",
            "extensionAttributes": [],
            "instanceType": "Range",
            "isApproximate": False,
            "maxValue": {
                "id": "X_2",
                "value": 20.0,
                "unit": None,
                "extensionAttributes": [],
                "instanceType": "Quantity",
            },
            "minValue": {
                "id": "X_1",
                "value": 10.0,
                "unit": None,
                "extensionAttributes": [],
                "instanceType": "Quantity",
            },
        },
        "plannedEnrollmentNumber": {
            "id": "X_6",
            "extensionAttributes": [],
            "instanceType": "Range",
            "isApproximate": False,
            "maxValue": {
                "id": "X_5",
                "value": 110.0,
                "unit": None,
                "extensionAttributes": [],
                "instanceType": "Quantity",
            },
            "minValue": {
                "id": "X_4",
                "value": 100.0,
                "unit": None,
                "extensionAttributes": [],
                "instanceType": "Quantity",
            },
        },
        "plannedSex": [
            {
                "code": "C49636",
                "codeSystem": "http://www.cdisc.org",
                "codeSystemVersion": "2024-09-27",
                "decode": "Both",
                "id": "X_14",
                "extensionAttributes": [],
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
