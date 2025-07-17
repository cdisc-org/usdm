import pandas as pd
from usdm_excel.study_product_sheet.study_product_sheet import StudyProductSheet
from usdm_excel.base_sheet import BaseSheet
from usdm_model.code import Code


def test_create_1(mocker, globals):
    ids = [
        "Id_1",
        "Id_2",
        "Id_3",
        "Id_4",
        "Id_5",
        "Id_6",
        "Id_7",
        "Id_8",
        "Id_9",
        "Id_10",
        "Id_11",
        "Id_12",
        "Id_13",
        "Id_14",
        "Id_15",
        "Id_16",
    ]
    data = {
        "name": ["60 mg Study Drug"],
        "description": ["description 1"],
        "label": ["label 1"],
        "pharmacologicClass": ["FDA: A=B"],
        "administrableDoseForm": ["TABLET"],
        "productDesignation": ["IMP"],
        "productSourcing": ["Centrally Sourced"],
        "ingredientRole": ["HL7:   100000072072=Active"],
        "substanceName": ["Ingredient C"],
        "substanceDescription": ["description 2"],
        "substanceLabel": ["label 2"],
        "substanceCode": [""],
        "strengthName": ["60 mg"],
        "strengthDescription": [""],
        "strengthLabel": [""],
        "strengthNumerator": ["60 mg"],
        "strengthDenominator": ["1 TABLET"],
        "referenceSubstanceName": [""],
        "referenceSubstanceDescription": [""],
        "referenceSubstanceLabel": [""],
        "referenceSubstanceCode": [""],
        "referenceSubstanceStrengthName": [""],
        "referenceSubstanceStrengthDescription": [""],
        "referenceSubstanceStrengthLabel": [""],
        "referenceSubstanceStrengthNumerator": [""],
        "referenceSubstanceStrengthDenominator": [""],
    }
    sheet = _setup_sheet(mocker, globals, data, ids)
    assert sheet.items[0].model_dump() == {
        "administrableDoseForm": {
            "id": "Id_2",
            "extensionAttributes": [],
            "instanceType": "AliasCode",
            "standardCode": {
                "code": "C42998",
                "codeSystem": "http://www.cdisc.org",
                "codeSystemVersion": "2024-09-27",
                "decode": "Tablet Dosage Form",
                "id": "Id_1",
                "extensionAttributes": [],
                "instanceType": "Code",
            },
            "standardCodeAliases": [],
        },
        "description": "description 1",
        "id": "Id_6",
        "identifiers": [],
        "ingredients": [
            {
                "id": "Id_9",
                "extensionAttributes": [],
                "instanceType": "Ingredient",
                "role": {
                    "code": "100000072072",
                    "codeSystem": "HL7",
                    "codeSystemVersion": "",
                    "decode": "Active",
                    "id": "Id_8",
                    "extensionAttributes": [],
                    "instanceType": "Code",
                },
                "substance": {
                    "codes": [],
                    "description": "description 2",
                    "id": "Id_7",
                    "extensionAttributes": [],
                    "instanceType": "Substance",
                    "label": "label 2",
                    "name": "Ingredient C",
                    "referenceSubstance": None,
                    "strengths": [
                        {
                            "denominator": {
                                "id": "Id_15",
                                "extensionAttributes": [],
                                "instanceType": "Quantity",
                                "unit": {
                                    "id": "Id_14",
                                    "extensionAttributes": [],
                                    "instanceType": "AliasCode",
                                    "standardCode": {
                                        "code": "C48542",
                                        "codeSystem": "http://www.cdisc.org",
                                        "codeSystemVersion": "2024-09-27",
                                        "decode": "Tablet Dosing Unit",
                                        "id": "Id_13",
                                        "extensionAttributes": [],
                                        "instanceType": "Code",
                                    },
                                    "standardCodeAliases": [],
                                },
                                "value": 1.0,
                            },
                            "description": "",
                            "id": "Id_16",
                            "extensionAttributes": [],
                            "instanceType": "Strength",
                            "label": "",
                            "name": "60 mg",
                            "numerator": {
                                "id": "Id_12",
                                "extensionAttributes": [],
                                "instanceType": "Quantity",
                                "unit": {
                                    "id": "Id_11",
                                    "extensionAttributes": [],
                                    "instanceType": "AliasCode",
                                    "standardCode": {
                                        "code": "C28253",
                                        "codeSystem": "http://www.cdisc.org",
                                        "codeSystemVersion": "2024-09-27",
                                        "decode": "Milligram",
                                        "id": "Id_10",
                                        "extensionAttributes": [],
                                        "instanceType": "Code",
                                    },
                                    "standardCodeAliases": [],
                                },
                                "value": 60.0,
                            },
                        },
                    ],
                },
            },
        ],
        "extensionAttributes": [],
        "instanceType": "AdministrableProduct",
        "label": "label 1",
        "name": "60 mg Study Drug",
        "notes": [],
        "pharmacologicClass": {
            "code": "A",
            "codeSystem": "FDA",
            "codeSystemVersion": "",
            "decode": "B",
            "id": "Id_3",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
        "productDesignation": {
            "code": "C202579",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Investigational Medicinal Product",
            "id": "Id_4",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
        "properties": [],
        "sourcing": {
            "code": "C215659",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Centrally Sourced",
            "id": "Id_5",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
    }


def test_create_2(mocker, globals):
    ids = [
        "Id_1",
        "Id_2",
        "Id_3",
        "Id_4",
        "Id_5",
        "Id_6",
        "Id_7",
        "Id_8",
        "Id_9",
        "Id_10",
        "Id_11",
        "Id_12",
        "Id_13",
        "Id_14",
        "Id_15",
        "Id_16",
        "Id_17",
        "Id_18",
        "Id_19",
        "Id_20",
        "Id_21",
        "Id_22",
        "Id_23",
        "Id_24",
        "Id_25",
        "Id_26",
        "Id_27",
        "Id_28",
        "Id_29",
        "Id_30",
    ]
    data = {
        "name": ["60 mg Study Drug", ""],
        "description": ["description 1", ""],
        "label": ["label 1", ""],
        "pharmacologicClass": ["FDA: A=B", ""],
        "administrableDoseForm": ["TABLET", ""],
        "productDesignation": ["IMP", "NIMP (AxMP)"],
        "productSourcing": ["Centrally Sourced", "Locally Sourced"],
        "ingredientRole": ["HL7:   100000072072=Active", "HL7:   100000072072=Active"],
        "substanceName": ["Ingredient C", "Ingredient D"],
        "substanceDescription": ["description 2", "description 3"],
        "substanceLabel": ["label 2", "label 3"],
        "substanceCode": ["", ""],
        "strengthName": ["60 mg", "120 mg"],
        "strengthDescription": ["", ""],
        "strengthLabel": ["", ""],
        "strengthNumerator": ["60 mg", "120 mg"],
        "strengthDenominator": ["1 TABLET", "1 TABLET"],
        "referenceSubstanceName": ["", ""],
        "referenceSubstanceDescription": ["", ""],
        "referenceSubstanceLabel": ["", ""],
        "referenceSubstanceCode": ["", ""],
        "referenceSubstanceStrengthName": ["", ""],
        "referenceSubstanceStrengthDescription": ["", ""],
        "referenceSubstanceStrengthLabel": ["", ""],
        "referenceSubstanceStrengthNumerator": ["", ""],
        "referenceSubstanceStrengthDenominator": ["", ""],
    }
    sheet = _setup_sheet(mocker, globals, data, ids)
    assert sheet.items[0].ingredients[0].substance.name == "Ingredient C"
    assert sheet.items[0].ingredients[1].substance.name == "Ingredient D"


def test_create_3(mocker, globals):
    ids = [
        "Id_1",
        "Id_2",
        "Id_3",
        "Id_4",
        "Id_5",
        "Id_6",
        "Id_7",
        "Id_8",
        "Id_9",
        "Id_10",
        "Id_11",
        "Id_12",
        "Id_13",
        "Id_14",
        "Id_15",
        "Id_16",
        "Id_17",
        "Id_18",
        "Id_19",
        "Id_20",
        "Id_21",
        "Id_22",
        "Id_23",
        "Id_24",
        "Id_25",
        "Id_26",
        "Id_27",
        "Id_28",
        "Id_29",
        "Id_30",
        "Id_31",
        "Id_32",
        "Id_33",
        "Id_34",
        "Id_35",
        "Id_36",
        "Id_37",
        "Id_38",
        "Id_39",
        "Id_40",
    ]
    data = {
        "name": ["60 mg Study Drug", ""],
        "description": ["description 1", ""],
        "label": ["label 1", ""],
        "pharmacologicClass": ["FDA: A=B", ""],
        "administrableDoseForm": ["TABLET", ""],
        "productDesignation": ["IMP", "NIMP (AxMP)"],
        "productSourcing": ["Centrally Sourced", "Locally Sourced"],
        "ingredientRole": ["HL7:   100000072072=Active", "HL7:   100000072072=Active"],
        "substanceName": ["Ingredient C", "Ingredient D"],
        "substanceDescription": ["description 2", "description 3"],
        "substanceLabel": ["label 2", "label 3"],
        "substanceCode": ["", ""],
        "strengthName": ["60 mg", "120 mg"],
        "strengthDescription": ["", ""],
        "strengthLabel": ["", ""],
        "strengthNumerator": ["60 mg", "120 mg"],
        "strengthDenominator": ["1 TABLET", "1 TABLET"],
        "referenceSubstanceName": ["", "albuterol base"],
        "referenceSubstanceDescription": ["", "Reference description"],
        "referenceSubstanceLabel": ["", "Reference label"],
        "referenceSubstanceCode": ["", ""],
        "referenceSubstanceStrengthName": ["", "90 μg"],
        "referenceSubstanceStrengthDescription": ["", "Ref strength description"],
        "referenceSubstanceStrengthLabel": ["", "Ref strength label"],
        "referenceSubstanceStrengthNumerator": ["", "90	ug"],
        "referenceSubstanceStrengthDenominator": ["", "1	INHALATION"],
    }
    sheet = _setup_sheet(mocker, globals, data, ids)
    assert sheet.items[0].ingredients[0].substance.referenceSubstance == None
    assert (
        sheet.items[0].ingredients[1].substance.referenceSubstance.name
        == "albuterol base"
    )
    assert (
        sheet.items[0].ingredients[1].substance.referenceSubstance.strengths[0].name
        == "90 μg"
    )


def test_missign_column_error(mocker, globals):
    ids = [
        "Id_1",
        "Id_2",
        "Id_3",
        "Id_4",
        "Id_5",
        "Id_6",
        "Id_7",
        "Id_8",
        "Id_9",
        "Id_10",
        "Id_11",
        "Id_12",
        "Id_13",
        "Id_14",
    ]
    data = {
        "name": ["60 mg Study Drug"],
        "description": ["description 1"],
        "label": ["label 1"],
        "administrableDoseForm": ["TABLET"],
        "productDesignation": ["IMP"],
        "productSourcing": ["Centrally Sourced"],
        "ingredientRole": ["HL7:   100000072072=Active"],
        "substanceName": ["Ingredient C"],
        "substanceDescription": ["description 2"],
        "substanceLabel": ["label 2"],
        "substanceCode": [""],
        "strengthName": ["60 mg"],
        "strengthDescription": [""],
        "strengthLabel": [""],
        "strengthNumerator": ["60 mg"],
        "strengthDenominator": ["1 TABLET"],
        "referenceSubstanceName": [""],
        "referenceSubstanceDescription": [""],
        "referenceSubstanceLabel": [""],
        "referenceSubstanceCode": [""],
        "referenceSubstanceStrengthName": [""],
        "referenceSubstanceStrengthDescription": [""],
        "referenceSubstanceStrengthLabel": [""],
        "referenceSubstanceStrengthNumerator": [""],
        "referenceSubstanceStrengthDenominator": [""],
    }
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    sheet = _setup_sheet(mocker, globals, data, ids)
    assert mock_error.call_count == 1
    mock_error.assert_has_calls(
        [
            mocker.call(
                "studyProducts",
                None,
                None,
                "Exception. Error [Failed to detect column(s) 'pharmacologicClass' in sheet] while reading sheet 'studyProducts'. See log for additional details.",
                40,
            )
        ]
    )


def _setup_sheet(mocker, globals, data, ids):
    globals.cross_references.clear()
    mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    mock_present.side_effect = [True]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ids
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)
    return StudyProductSheet("", globals)
