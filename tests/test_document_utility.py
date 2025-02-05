from usdm_excel.document.utility import get_soup


def test_normal(mocker, globals, factory):
    globals.errors_and_logging.errors().clear()
    bs = factory.base_sheet(mocker)
    assert globals.errors_and_logging.errors().count() == 0
    result = get_soup("<p>Hello</p>", bs)
    expected = "<p>Hello</p>"
    assert str(result) == expected
    assert globals.errors_and_logging.errors().count() == 0


def test_warning(mocker, globals, factory):
    mock_error = mocker.patch(
        "usdm_excel.errors_and_logging.errors_and_logging.ErrorsAndLogging.debug"
    )
    globals.errors_and_logging.errors().clear()
    bs = factory.base_sheet(mocker)
    assert globals.errors_and_logging.errors().count() == 0
    result = get_soup("input/output", bs)
    expected = "input/output"
    assert str(result) == expected
    mock_error.assert_called()
    assert (
        mock_error.call_args[0][0]
        == "Warning raised within Soup package, processing 'input/output'\nMessage returned 'The input looks more like a filename than markup. You may want to open this file and pass the filehandle into Beautiful Soup.'"
    )
    assert mock_error.call_args[0][1] == ""
