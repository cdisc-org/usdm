import pandas as pd
from usdm_excel.study_product_sheet.study_product_organization_role_sheet import (
    StudyProductOrganizationRoleSheet,
)
from usdm_model.organization import Organization
from usdm_model.administrable_product import AdministrableProduct
from usdm_model.medical_device import MedicalDevice
from usdm_excel.globals import Globals
from tests.test_factory import Factory


def test_create(factory, mocker, globals):
    data = {
        "name": ["AP1", "AP2", "AP3"],
        "description": ["Desc One", "Desc Two", "Desc Three"],
        "label": ["Lable 1", "L2", "L3"],
        "organization": ["Sponsor 1", "Sponsor 2", "Sponsor 3"],
        "role": ["Manufacturer", "Supplier", "Supplier"],
        "appliesTo": ["Product 1", "Device 1", "Product 1, Device 1"],
    }
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [
        "C_1",
        "C_2",
        "C_3",
        "O_1",
        "O_2",
        "O_3",
        "C_4",
        "C_5",
        "C_6",
        "C_7",
        "C_8",
        "C_9",
        "C_10",
        "C_11",
        "C_12",
        "C_13",
        "AP_1",
        "AP_2",
        "AP_3",
        "C_15",
        "C_16",
        "C_17",
        "MD_1",
        "MD_2",
        "MD_3",
        "C_18",
        "POR_1",
        "C_19",
        "POR_2",
        "C_20",
        "POR_3",
        "X_5",
        "X_6",
        "X_7",
        "X_8",
        "X_9",
        "X_10",
        "X_11",
        "X_12",
    ]
    _setup(mocker, globals, data)
    _create_orgs(factory, globals)
    _create_products(factory, globals)
    _create_devices(factory, globals)
    item = StudyProductOrganizationRoleSheet("", globals)
    assert len(item.items) == 3
    assert item.items[0].model_dump() == {
        "id": "POR_1",
        "name": "AP1",
        "label": "Lable 1",
        "description": "Desc One",
        "code": {
            "id": "C_18",
            "code": "C25392",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Manufacturer",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
        "appliesToIds": ["AP_1"],
        "organizationId": "O_1",
        "extensionAttributes": [],
        "instanceType": "ProductOrganizationRole",
    }
    assert item.items[1].model_dump() == {
        "id": "POR_2",
        "name": "AP2",
        "label": "L2",
        "description": "Desc Two",
        "code": {
            "id": "C_19",
            "code": "C43530",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Supplier",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
        "appliesToIds": ["MD_1"],
        "organizationId": "O_2",
        "extensionAttributes": [],
        "instanceType": "ProductOrganizationRole",
    }
    assert item.items[2].model_dump() == {
        "id": "POR_3",
        "name": "AP3",
        "label": "L3",
        "description": "Desc Three",
        "code": {
            "id": "C_20",
            "code": "C43530",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Supplier",
            "extensionAttributes": [],
            "instanceType": "Code",
        },
        "appliesToIds": ["AP_1", "MD_1"],
        "organizationId": "O_3",
        "extensionAttributes": [],
        "instanceType": "ProductOrganizationRole",
    }


def test_create_empty(mocker, globals):
    data = {}
    _setup(mocker, globals, data)
    item = StudyProductOrganizationRoleSheet("", globals)
    assert len(item.items) == 0


def test_read_cell_by_name_error(mocker, globals):
    data = {
        "name": ["AP1"],
        "description": ["Desc One"],
        "label": ["Lable 1"],
        "role": ["Investigator"],
    }
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Code_1", "Abbreviation_1"]
    _setup(mocker, globals, data)
    item = StudyProductOrganizationRoleSheet("", globals)
    assert mock_error.call_count == 2
    mock_error.assert_has_calls(
        [
            mocker.call(
                "studyProductOrganizationRoles",
                1,
                -1,
                "Error attempting to read cell 'organization'. Exception: Failed to detect column(s) 'organization' in sheet",
                40,
            ),
            mocker.call(
                "studyProductOrganizationRoles",
                None,
                None,
                "Exception. Error ['NoneType' object has no attribute 'id'] while reading sheet 'studyProductOrganizationRoles'. See log for additional details.",
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
        instance = factory.item(Organization, item)
        globals.cross_references.add(item["name"], instance)


def _create_products(factory: Factory, globals: Globals):
    std_code = factory.cdisc_code("C12345x1", "XX1")
    items = [
        {
            "name": "Product 1",
            "productDesignation": factory.cdisc_code("C12345x1", "YYY"),
            "sourcing": factory.cdisc_code("C12345x1", "XXX"),
            "administrableDoseForm": factory.alias_code(std_code, []),
        },
        {
            "name": "Product 2",
            "productDesignation": factory.cdisc_code("C12345x1", "YYY"),
            "sourcing": factory.cdisc_code("C12345x1", "XXX"),
            "administrableDoseForm": factory.alias_code(std_code, []),
        },
        {
            "name": "Product 3",
            "productDesignation": factory.cdisc_code("C12345x1", "YYY"),
            "sourcing": factory.cdisc_code("C12345x1", "XXX"),
            "administrableDoseForm": factory.alias_code(std_code, []),
        },
    ]
    for item in items:
        instance = factory.item(AdministrableProduct, item)
        globals.cross_references.add(item["name"], instance)


def _create_devices(factory: Factory, globals: Globals):
    items = [
        {"name": "Device 1", "sourcing": factory.cdisc_code("C12345x1", "XXX")},
        {"name": "Device 2", "sourcing": factory.cdisc_code("C12345x1", "XXX")},
        {"name": "Device 3", "sourcing": factory.cdisc_code("C12345x1", "XXX")},
    ]
    for item in items:
        instance = factory.item(MedicalDevice, item)
        globals.cross_references.add(item["name"], instance)
