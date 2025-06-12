import pandas as pd
from usdm_excel.globals import Globals


def mock_sheet(mocker, globals: Globals, data):
    # print(f"MOCKER: {type(mocker)}")
    globals.cross_references.clear()
    mo = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mo)
    item = mocker.patch("pandas.read_excel")
    item.return_value = pd.DataFrame.from_dict(data)
    return item


def mock_sheet_present(mocker):
    item = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
    item.side_effect = [True]
    return item


def fake_create_object(cls, params, index):
    params["id"] = f"{cls.__name__}_{index}"
    return cls(**params)


def mock_create_object(mocker, data):
    item = mocker.patch("usdm_excel.base_sheet.BaseSheet.create_object")
    #print(f"ITEM ARGS: {item.call_args}")
    for index, params in enumerate(data):
        params["data"]["id"] = f"{params['cls'].__name__}_{index + 1}"
    item.side_effect = [params["cls"](**params["data"]) for params in data]
    return item


def mock_error(mocker):
    item = mocker.patch("usdm_excel.base_sheet.BaseSheet._error")
    return item


def mock_sheet_exception(mocker):
    item = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_exception")
    return item
