def mock_error_add(mocker, data):
    item = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    item.side_effect = data
    return item
