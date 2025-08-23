import pytest
import json
import pandas as pd
from usdm_excel.study_design_intervention_sheet.study_design_intervention_sheet import (
    StudyDesignInterventionSheet,
)
from usdm_model.code import Code
from usdm_model.administrable_product import AdministrableProduct
from usdm_excel.globals import Globals
from tests.test_factory import Factory

xfail = pytest.mark.xfail

SAVE = False
COLUMNS = [
    "name",
    "description",
    "label",
    "codes",
    "role",
    "type",
    "product",
    "minimumResponseDuration",
    "administrationName",
    "administrationDescription",
    "administrationLabel",
    "administrationRoute",
    "administrationDose",
    "administrationFrequency",
    "administrationDurationDescription",
    "administrationDurationWillVary",
    "administrationDurationWillVaryReason",
    "administrationDurationQuantity",
]


def read_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def dump_json(data):
    print(f"\n{json.dumps(data, indent=2)}")


def test_create(mocker, globals: Globals, factory: Factory):
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [f"pid_{x}" for x in range(10)]
    _create_products(factory, globals)
    mock_id.side_effect = [f"Id_{x}" for x in range(100)]

    mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
    mock_code.side_effect = [
        Code(
            id=f"Code_{x}",
            code=f"C{x}",
            codeSystem="CDISC",
            codeSystemVersion="1",
            decode=f"INDEX{x}",
        )
        for x in range(100)
    ]

    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    # productDesignation now removed but leave in data, wont do any harm as it is ignored. Also see COLUMNS above.
    data = [
        # name     description    label          codes                          role                         type      product                 minimumResponseDuration,  administrationName [10] administrationDescription administrationLabel administrationRoute administrationDose administrationFrequency administrationDurationDescription administrationDurationWillVary administrationDurationWillVaryReason administrationDurationQuantity
        [
            "Int 1",
            "Int Desc 1",
            "Int Label 1",
            "SPONSOR: A=B",
            "Experimental Intervention",
            "C12345",
            "Product 1",
            "1 Day",
            "Admin 1",
            "Admin Desc 1",
            "Admin Label 1",
            "C345671",
            "12 mg",
            "C65432",
            "Dur desc 1",
            "False",
            "",
            "14 %",
        ],
        [
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "Admin 2",
            "Admin Desc 2",
            "Admin Label 1",
            "C345672",
            "1 mg",
            "C65432",
            "Dur desc 1",
            "False",
            "",
            "10 m",
        ],
        [
            "Int 2",
            "Int Desc 2",
            "Int Label 2",
            "SPONSOR: C=D",
            "Placebo",
            "C12346",
            "",
            "3 Weeks",
            "Admin 3",
            "Admin Desc 3",
            "Admin Label 1",
            "C345673",
            "100 mg",
            "C65432",
            "Dur desc 1",
            "False",
            "",
            "12 C",
        ],
        [
            "Int 3",
            "Int Desc 3",
            "Int Label 3",
            "SPONSOR: E=F, SPONSOR: G=H",
            "Rescue Medicine",
            "C12347",
            "",
            "4 Years",
            "Admin 4",
            "Admin Desc 4",
            "Admin Label 1",
            "C345674",
            "500 mg",
            "C65432",
            "Dur desc 1",
            "False",
            "",
            "12 F",
        ],
        [
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "Admin 5",
            "Admin Desc 5",
            "Admin Label 1",
            "C345675",
            "1 mg",
            "C65432",
            "Dur desc 1",
            "False",
            "",
            "15 in",
        ],
    ]

    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=COLUMNS)
    item = StudyDesignInterventionSheet("", globals)
    # dump_json({'items': [json.loads(x.to_json()) for x in interventions.items]})
    assert len(item.items) == 3
    assert item.items[0].model_dump() == {
        "id": "Id_14",
        "name": "Int 1",
        "label": "Int Label 1",
        "description": "Int Desc 1",
        "role": {
            "id": "Code_2",
            "code": "C2",
            "codeSystem": "CDISC",
            "codeSystemVersion": "1",
            "decode": "INDEX2",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
        "type": {
            "id": "Code_3",
            "code": "C3",
            "codeSystem": "CDISC",
            "codeSystemVersion": "1",
            "decode": "INDEX3",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
        "minimumResponseDuration": {
            "id": "Id_13",
            "value": 1.0,
            "unit": {
                "id": "Id_12",
                "standardCode": {
                    "id": "Id_11",
                    "code": "C25301",
                    "codeSystem": "http://www.cdisc.org",
                    "codeSystemVersion": "2024-09-27",
                    "decode": "Day",
                    "extensionAttributes": [],
                    "instanceType": "Code",
                },
                "standardCodeAliases": [],
                "extensionAttributes": [],
                "instanceType": "AliasCode",
            },
            "extensionAttributes": [],
            "instanceType": "Quantity",
        },
        "codes": [
            {
                "id": "Id_10",
                "code": "A",
                "codeSystem": "SPONSOR",
                "codeSystemVersion": "",
                "decode": "B",
                "extensionAttributes": [],
                "instanceType": "Code",
            }
        ],
        "administrations": [
            {
                "id": "Id_9",
                "name": "Admin 1",
                "label": "Admin Label 1",
                "medicalDeviceId": None,
                "administrableProductId": "pid_4",
                "description": "Admin Desc 1",
                "duration": {
                    "id": "Id_3",
                    "quantity": {
                        "id": "Id_2",
                        "value": 14.0,
                        "unit": {
                            "id": "Id_1",
                            "standardCode": {
                                "id": "Id_0",
                                "code": "C25613",
                                "codeSystem": "http://www.cdisc.org",
                                "codeSystemVersion": "2024-09-27",
                                "decode": "Percentage",
                                "extensionAttributes": [],
                                "instanceType": "Code",
                            },
                            "standardCodeAliases": [],
                            "extensionAttributes": [],
                            "instanceType": "AliasCode",
                        },
                        "extensionAttributes": [],
                        "instanceType": "Quantity",
                    },
                    "text": "Dur desc 1",
                    "durationWillVary": False,
                    "reasonDurationWillVary": "",
                    "extensionAttributes": [],
                    "instanceType": "Duration",
                },
                "dose": {
                    "id": "Id_6",
                    "value": 12.0,
                    "unit": {
                        "id": "Id_5",
                        "standardCode": {
                            "id": "Id_4",
                            "code": "C28253",
                            "codeSystem": "http://www.cdisc.org",
                            "codeSystemVersion": "2024-09-27",
                            "decode": "Milligram",
                            "extensionAttributes": [],
                            "instanceType": "Code",
                        },
                        "standardCodeAliases": [],
                        "extensionAttributes": [],
                        "instanceType": "AliasCode",
                    },
                    "extensionAttributes": [],
                    "instanceType": "Quantity",
                },
                "route": {
                    "id": "Id_7",
                    "standardCode": {
                        "id": "Code_0",
                        "code": "C0",
                        "codeSystem": "CDISC",
                        "codeSystemVersion": "1",
                        "decode": "INDEX0",
                        "extensionAttributes": [],
                        "instanceType": "Code",
                    },
                    "standardCodeAliases": [],
                    "extensionAttributes": [],
                    "instanceType": "AliasCode",
                },
                "frequency": {
                    "id": "Id_8",
                    "standardCode": {
                        "id": "Code_1",
                        "code": "C1",
                        "codeSystem": "CDISC",
                        "codeSystemVersion": "1",
                        "decode": "INDEX1",
                        "extensionAttributes": [],
                        "instanceType": "Code",
                    },
                    "standardCodeAliases": [],
                    "extensionAttributes": [],
                    "instanceType": "AliasCode",
                },
                "notes": [],
                "extensionAttributes": [],
                "instanceType": "Administration",
            },
            {
                "id": "Id_24",
                "name": "Admin 2",
                "label": "Admin Label 1",
                "medicalDeviceId": None,
                "administrableProductId": None,
                "description": "Admin Desc 2",
                "duration": {
                    "id": "Id_18",
                    "quantity": {
                        "id": "Id_17",
                        "value": 10.0,
                        "unit": {
                            "id": "Id_16",
                            "standardCode": {
                                "id": "Id_15",
                                "code": "C41139",
                                "codeSystem": "http://www.cdisc.org",
                                "codeSystemVersion": "2024-09-27",
                                "decode": "Meter",
                                "extensionAttributes": [],
                                "instanceType": "Code",
                            },
                            "standardCodeAliases": [],
                            "extensionAttributes": [],
                            "instanceType": "AliasCode",
                        },
                        "extensionAttributes": [],
                        "instanceType": "Quantity",
                    },
                    "text": "Dur desc 1",
                    "durationWillVary": False,
                    "reasonDurationWillVary": "",
                    "extensionAttributes": [],
                    "instanceType": "Duration",
                },
                "dose": {
                    "id": "Id_21",
                    "value": 1.0,
                    "unit": {
                        "id": "Id_20",
                        "standardCode": {
                            "id": "Id_19",
                            "code": "C28253",
                            "codeSystem": "http://www.cdisc.org",
                            "codeSystemVersion": "2024-09-27",
                            "decode": "Milligram",
                            "extensionAttributes": [],
                            "instanceType": "Code",
                        },
                        "standardCodeAliases": [],
                        "extensionAttributes": [],
                        "instanceType": "AliasCode",
                    },
                    "extensionAttributes": [],
                    "instanceType": "Quantity",
                },
                "route": {
                    "id": "Id_22",
                    "standardCode": {
                        "id": "Code_4",
                        "code": "C4",
                        "codeSystem": "CDISC",
                        "codeSystemVersion": "1",
                        "decode": "INDEX4",
                        "extensionAttributes": [],
                        "instanceType": "Code",
                    },
                    "standardCodeAliases": [],
                    "extensionAttributes": [],
                    "instanceType": "AliasCode",
                },
                "frequency": {
                    "id": "Id_23",
                    "standardCode": {
                        "id": "Code_5",
                        "code": "C5",
                        "codeSystem": "CDISC",
                        "codeSystemVersion": "1",
                        "decode": "INDEX5",
                        "extensionAttributes": [],
                        "instanceType": "Code",
                    },
                    "standardCodeAliases": [],
                    "extensionAttributes": [],
                    "instanceType": "AliasCode",
                },
                "notes": [],
                "extensionAttributes": [],
                "instanceType": "Administration",
            },
        ],
        "notes": [],
        "extensionAttributes": [],
        "instanceType": "StudyIntervention",
    }
    assert item.items[1].model_dump() == {
        "id": "Id_39",
        "name": "Int 2",
        "label": "Int Label 2",
        "description": "Int Desc 2",
        "role": {
            "id": "Code_8",
            "code": "C8",
            "codeSystem": "CDISC",
            "codeSystemVersion": "1",
            "decode": "INDEX8",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
        "type": {
            "id": "Code_9",
            "code": "C9",
            "codeSystem": "CDISC",
            "codeSystemVersion": "1",
            "decode": "INDEX9",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
        "minimumResponseDuration": {
            "id": "Id_38",
            "value": 3.0,
            "unit": {
                "id": "Id_37",
                "standardCode": {
                    "id": "Id_36",
                    "code": "C29844",
                    "codeSystem": "http://www.cdisc.org",
                    "codeSystemVersion": "2024-09-27",
                    "decode": "Week",
                    "extensionAttributes": [],
                    "instanceType": "Code",
                },
                "standardCodeAliases": [],
                "extensionAttributes": [],
                "instanceType": "AliasCode",
            },
            "extensionAttributes": [],
            "instanceType": "Quantity",
        },
        "codes": [
            {
                "id": "Id_35",
                "code": "C",
                "codeSystem": "SPONSOR",
                "codeSystemVersion": "",
                "decode": "D",
                "extensionAttributes": [],
                "instanceType": "Code",
            }
        ],
        "administrations": [
            {
                "id": "Id_34",
                "name": "Admin 3",
                "label": "Admin Label 1",
                "medicalDeviceId": None,
                "administrableProductId": None,
                "description": "Admin Desc 3",
                "duration": {
                    "id": "Id_28",
                    "quantity": {
                        "id": "Id_27",
                        "value": 12.0,
                        "unit": {
                            "id": "Id_26",
                            "standardCode": {
                                "id": "Id_25",
                                "code": "C42559",
                                "codeSystem": "http://www.cdisc.org",
                                "codeSystemVersion": "2024-09-27",
                                "decode": "Degree Celsius",
                                "extensionAttributes": [],
                                "instanceType": "Code",
                            },
                            "standardCodeAliases": [],
                            "extensionAttributes": [],
                            "instanceType": "AliasCode",
                        },
                        "extensionAttributes": [],
                        "instanceType": "Quantity",
                    },
                    "text": "Dur desc 1",
                    "durationWillVary": False,
                    "reasonDurationWillVary": "",
                    "extensionAttributes": [],
                    "instanceType": "Duration",
                },
                "dose": {
                    "id": "Id_31",
                    "value": 100.0,
                    "unit": {
                        "id": "Id_30",
                        "standardCode": {
                            "id": "Id_29",
                            "code": "C28253",
                            "codeSystem": "http://www.cdisc.org",
                            "codeSystemVersion": "2024-09-27",
                            "decode": "Milligram",
                            "extensionAttributes": [],
                            "instanceType": "Code",
                        },
                        "standardCodeAliases": [],
                        "extensionAttributes": [],
                        "instanceType": "AliasCode",
                    },
                    "extensionAttributes": [],
                    "instanceType": "Quantity",
                },
                "route": {
                    "id": "Id_32",
                    "standardCode": {
                        "id": "Code_6",
                        "code": "C6",
                        "codeSystem": "CDISC",
                        "codeSystemVersion": "1",
                        "decode": "INDEX6",
                        "extensionAttributes": [],
                        "instanceType": "Code",
                    },
                    "standardCodeAliases": [],
                    "extensionAttributes": [],
                    "instanceType": "AliasCode",
                },
                "frequency": {
                    "id": "Id_33",
                    "standardCode": {
                        "id": "Code_7",
                        "code": "C7",
                        "codeSystem": "CDISC",
                        "codeSystemVersion": "1",
                        "decode": "INDEX7",
                        "extensionAttributes": [],
                        "instanceType": "Code",
                    },
                    "standardCodeAliases": [],
                    "extensionAttributes": [],
                    "instanceType": "AliasCode",
                },
                "notes": [],
                "extensionAttributes": [],
                "instanceType": "Administration",
            }
        ],
        "notes": [],
        "extensionAttributes": [],
        "instanceType": "StudyIntervention",
    }
    assert item.items[2].model_dump() == {
        "id": "Id_55",
        "name": "Int 3",
        "label": "Int Label 3",
        "description": "Int Desc 3",
        "role": {
            "id": "Code_12",
            "code": "C12",
            "codeSystem": "CDISC",
            "codeSystemVersion": "1",
            "decode": "INDEX12",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
        "type": {
            "id": "Code_13",
            "code": "C13",
            "codeSystem": "CDISC",
            "codeSystemVersion": "1",
            "decode": "INDEX13",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
        "minimumResponseDuration": {
            "id": "Id_54",
            "value": 4.0,
            "unit": {
                "id": "Id_53",
                "standardCode": {
                    "id": "Id_52",
                    "code": "C29848",
                    "codeSystem": "http://www.cdisc.org",
                    "codeSystemVersion": "2024-09-27",
                    "decode": "Year",
                    "extensionAttributes": [],
                    "instanceType": "Code",
                },
                "standardCodeAliases": [],
                "extensionAttributes": [],
                "instanceType": "AliasCode",
            },
            "extensionAttributes": [],
            "instanceType": "Quantity",
        },
        "codes": [
            {
                "id": "Id_50",
                "code": "E",
                "codeSystem": "SPONSOR",
                "codeSystemVersion": "",
                "decode": "F",
                "extensionAttributes": [],
                "instanceType": "Code",
            },
            {
                "id": "Id_51",
                "code": "G",
                "codeSystem": "SPONSOR",
                "codeSystemVersion": "",
                "decode": "H",
                "extensionAttributes": [],
                "instanceType": "Code",
            },
        ],
        "administrations": [
            {
                "id": "Id_49",
                "name": "Admin 4",
                "label": "Admin Label 1",
                "medicalDeviceId": None,
                "administrableProductId": None,
                "description": "Admin Desc 4",
                "duration": {
                    "id": "Id_43",
                    "quantity": {
                        "id": "Id_42",
                        "value": 12.0,
                        "unit": {
                            "id": "Id_41",
                            "standardCode": {
                                "id": "Id_40",
                                "code": "C44277",
                                "codeSystem": "http://www.cdisc.org",
                                "codeSystemVersion": "2024-09-27",
                                "decode": "Degree Fahrenheit",
                                "extensionAttributes": [],
                                "instanceType": "Code",
                            },
                            "standardCodeAliases": [],
                            "extensionAttributes": [],
                            "instanceType": "AliasCode",
                        },
                        "extensionAttributes": [],
                        "instanceType": "Quantity",
                    },
                    "text": "Dur desc 1",
                    "durationWillVary": False,
                    "reasonDurationWillVary": "",
                    "extensionAttributes": [],
                    "instanceType": "Duration",
                },
                "dose": {
                    "id": "Id_46",
                    "value": 500.0,
                    "unit": {
                        "id": "Id_45",
                        "standardCode": {
                            "id": "Id_44",
                            "code": "C28253",
                            "codeSystem": "http://www.cdisc.org",
                            "codeSystemVersion": "2024-09-27",
                            "decode": "Milligram",
                            "extensionAttributes": [],
                            "instanceType": "Code",
                        },
                        "standardCodeAliases": [],
                        "extensionAttributes": [],
                        "instanceType": "AliasCode",
                    },
                    "extensionAttributes": [],
                    "instanceType": "Quantity",
                },
                "route": {
                    "id": "Id_47",
                    "standardCode": {
                        "id": "Code_10",
                        "code": "C10",
                        "codeSystem": "CDISC",
                        "codeSystemVersion": "1",
                        "decode": "INDEX10",
                        "extensionAttributes": [],
                        "instanceType": "Code",
                    },
                    "standardCodeAliases": [],
                    "extensionAttributes": [],
                    "instanceType": "AliasCode",
                },
                "frequency": {
                    "id": "Id_48",
                    "standardCode": {
                        "id": "Code_11",
                        "code": "C11",
                        "codeSystem": "CDISC",
                        "codeSystemVersion": "1",
                        "decode": "INDEX11",
                        "extensionAttributes": [],
                        "instanceType": "Code",
                    },
                    "standardCodeAliases": [],
                    "extensionAttributes": [],
                    "instanceType": "AliasCode",
                },
                "notes": [],
                "extensionAttributes": [],
                "instanceType": "Administration",
            },
            {
                "id": "Id_65",
                "name": "Admin 5",
                "label": "Admin Label 1",
                "medicalDeviceId": None,
                "administrableProductId": None,
                "description": "Admin Desc 5",
                "duration": {
                    "id": "Id_59",
                    "quantity": {
                        "id": "Id_58",
                        "value": 15.0,
                        "unit": {
                            "id": "Id_57",
                            "standardCode": {
                                "id": "Id_56",
                                "code": "C48500",
                                "codeSystem": "http://www.cdisc.org",
                                "codeSystemVersion": "2024-09-27",
                                "decode": "Inch",
                                "extensionAttributes": [],
                                "instanceType": "Code",
                            },
                            "standardCodeAliases": [],
                            "extensionAttributes": [],
                            "instanceType": "AliasCode",
                        },
                        "extensionAttributes": [],
                        "instanceType": "Quantity",
                    },
                    "text": "Dur desc 1",
                    "durationWillVary": False,
                    "reasonDurationWillVary": "",
                    "extensionAttributes": [],
                    "instanceType": "Duration",
                },
                "dose": {
                    "id": "Id_62",
                    "value": 1.0,
                    "unit": {
                        "id": "Id_61",
                        "standardCode": {
                            "id": "Id_60",
                            "code": "C28253",
                            "codeSystem": "http://www.cdisc.org",
                            "codeSystemVersion": "2024-09-27",
                            "decode": "Milligram",
                            "extensionAttributes": [],
                            "instanceType": "Code",
                        },
                        "standardCodeAliases": [],
                        "extensionAttributes": [],
                        "instanceType": "AliasCode",
                    },
                    "extensionAttributes": [],
                    "instanceType": "Quantity",
                },
                "route": {
                    "id": "Id_63",
                    "standardCode": {
                        "id": "Code_14",
                        "code": "C14",
                        "codeSystem": "CDISC",
                        "codeSystemVersion": "1",
                        "decode": "INDEX14",
                        "extensionAttributes": [],
                        "instanceType": "Code",
                    },
                    "standardCodeAliases": [],
                    "extensionAttributes": [],
                    "instanceType": "AliasCode",
                },
                "frequency": {
                    "id": "Id_64",
                    "standardCode": {
                        "id": "Code_15",
                        "code": "C15",
                        "codeSystem": "CDISC",
                        "codeSystemVersion": "1",
                        "decode": "INDEX15",
                        "extensionAttributes": [],
                        "instanceType": "Code",
                    },
                    "standardCodeAliases": [],
                    "extensionAttributes": [],
                    "instanceType": "AliasCode",
                },
                "notes": [],
                "extensionAttributes": [],
                "instanceType": "Administration",
            },
        ],
        "notes": [],
        "extensionAttributes": [],
        "instanceType": "StudyIntervention",
    }


def test_create_empty(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = []
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=COLUMNS)
    interventions = StudyDesignInterventionSheet("", globals)
    assert len(interventions.items) == 0


def test_read_cell_by_name_error(mocker, globals):
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]]
    mock_read = mocker.patch("pandas.read_excel")
    columns = COLUMNS
    columns = columns[0:-1]
    mock_read.return_value = pd.DataFrame(data, columns=columns)
    interventions = StudyDesignInterventionSheet("", globals)
    mock_error.assert_called()
    assert mock_error.call_args[0][0] == "studyDesignInterventions"
    assert mock_error.call_args[0][1] == None
    assert mock_error.call_args[0][2] == None
    assert (
        mock_error.call_args[0][3]
        == "Exception. Error [Failed to detect column(s) 'administrationDurationQuantity' in sheet] while reading sheet 'studyDesignInterventions'. See log for additional details."
    )


def _create_products(factory: Factory, globals: Globals):
    std_code = factory.cdisc_code("C12345x1", "XX1")
    items = [
        {
            "name": "Product 1",
            "productDesignation": factory.cdisc_code("C12345x1", "YYY"),
            "sourcing": factory.cdisc_code("C12345x1", "XXX"),
            "administrableDoseForm": factory.alias_code(std_code, []),
        },
    ]
    for item in items:
        instance = factory.item(AdministrableProduct, item)
        globals.cross_references.add(item["name"], instance)
