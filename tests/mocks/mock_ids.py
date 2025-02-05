def mock_build_id(mocker, data):
    item = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    item.side_effect = data
    return item
