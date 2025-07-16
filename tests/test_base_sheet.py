import pytest
import pandas as pd
from usdm_excel.base_sheet import BaseSheet
from usdm_model.code import Code

xfail = pytest.mark.xfail


def test_cell_empty(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = {"col_1": [3, 2, 1, 0], "col_2": [None, "b", "c", None]}
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)
    base = BaseSheet("", globals, "sheet")
    test_data = [(0, 0, False), (3, 0, False), (0, 1, True), (3, 1, True)]
    for test in test_data:
        assert (base.cell_empty(test[0], test[1])) == test[2]


def test_cell_empty_legacy(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = {"col_1": [3, 2, 1, 0], "col_2": [None, "b", "-", None]}
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)
    base = BaseSheet("", globals, "sheet")
    test_data = [
        (0, 0, "3", False),
        (3, 0, "0", False),
        (0, 1, "", True),
        (2, 1, "", True),
        (3, 1, "", True),
    ]
    for test in test_data:
        value, is_null = base.read_cell_empty_legacy(test[0], test[1])
        assert (value) == test[2]
        assert (is_null) == test[3]


def test_read_cell_empty(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = {"col_1": [3, 2, 1, 0], "col_2": [None, "b", "-", None]}
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)
    base = BaseSheet("", globals, "sheet")
    test_data = [
        (0, 0, "3", "3"),
        (3, 0, "0", "0"),
        (0, 1, "", ""),
        (2, 1, "", "-"),
        (3, 1, "", ""),
    ]
    for test in test_data:
        assert (base.read_cell_empty(test[0], test[1], "-")) == test[2]
        assert (base.read_cell_empty(test[0], test[1], "=")) == test[3]


def test_read_cell(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", ""]}
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)
    base = BaseSheet("", globals, "sheet")
    test_data = [(0, 0, "3"), (3, 0, "0"), (0, 1, "a"), (3, 1, "")]
    for test in test_data:
        assert (base.read_cell(test[0], test[1])) == test[2]


def test_read_cell_default(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", None]}
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)
    base = BaseSheet("", globals, "sheet")
    test_data = [(3, 1, "100s", "100s")]
    for test in test_data:
        assert (base.read_cell(test[0], test[1], default=test[2])) == test[3]


def test_read_cell_error(mocker, globals):
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", ""]}
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)
    base = BaseSheet("", globals, "sheet")
    assert (base.read_cell(6, 8)) == ""
    mock_error.assert_called()
    assert mock_error.call_args[0][0] == "sheet"
    assert mock_error.call_args[0][1] == 7
    assert mock_error.call_args[0][2] == 9
    assert (
        mock_error.call_args[0][3]
        == "Exception. Error reading cell. See log for additional details."
    )


def test_read_cell_by_name(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [["tom", 10], ["nick", 15], ["juli", 14], ["fred", ""]]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=["Name", "Age"])
    base = BaseSheet("", globals, "sheet")
    test_data = [
        (0, "Name", "tom"),
        (2, "Name", "juli"),
        (0, "Age", "10"),
        (2, "Age", "14"),
        (3, "Age", ""),
    ]
    for test in test_data:
        assert (base.read_cell_by_name(test[0], test[1])) == test[2]


def test_read_cell_by_name_default(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [["tom", 10], ["nick", 15], ["juli", 14], ["fred", ""]]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=["Name", "Age"])
    base = BaseSheet("", globals, "sheet")
    assert (base.read_cell_by_name(0, "NameX", "Default")) == "Default"
    assert (base.read_cell_by_name(0, "Name", "Default")) == "tom"
    assert (base.read_cell_by_name(0, ["NameX", "XXX"], "Default")) == "Default"
    assert (base.read_cell_by_name(0, ["NameX", "XXX", "Age"], "Default")) == "10"
    assert (base.read_cell_by_name(3, "Age", default="100")) == ""


def test_read_cell_by_name_error(mocker, globals):
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [["tom", 10], ["nick", 15], ["juli", 14]]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=["Name", "Age"])
    base = BaseSheet("", globals, "sheet")
    assert (base.read_cell_by_name(1, "Not There")) == ""
    mock_error.assert_called()
    assert mock_error.call_args[0][0] == "sheet"
    assert mock_error.call_args[0][1] == 2
    assert mock_error.call_args[0][2] == -1
    assert (
        mock_error.call_args[0][3]
        == "Error attempting to read cell 'Not There'. Exception: Failed to detect column(s) 'Not There' in sheet"
    )


def test_read_cell_by_name_present(mocker, globals):
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [["tom", 10], ["nick", 15], ["juli", 14]]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=["Name", "Age"])
    base = BaseSheet("", globals, "sheet")
    assert (base.read_cell_by_name(1, "Not There", must_be_present=False)) == ""
    mock_error.assert_not_called()


def test_read_cell_multiple(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        ["tom", ""],
        ["nick", "Sam"],
        ["juli", " Fred, Dick,   Harry  "],
        ["andy", "John  , Jane"],
        ["andy", '"John, & Fred", Jane'],
        ["andy", '"John, \\" & Fred", Jane'],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=["Name", "Children"])
    base = BaseSheet("", globals, "sheet")
    test_data = [
        (0, 1, []),
        (2, 1, ["Fred", "Dick", "Harry"]),
        (3, 1, ["John", "Jane"]),
        (4, 1, ["John, & Fred", "Jane"]),
        (5, 1, ['John, " & Fred', "Jane"]),
    ]
    for test in test_data:
        assert (base.read_cell_multiple(test[0], test[1])) == test[2]


def test_read_cell_multiple_by_name(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        ["tom", ""],
        ["nick", "Sam"],
        ["juli", " Fred, Dick,   Harry  "],
        ["andy", "John  , Jane"],
        ["andy", '"John, & Fred", Jane'],
        ["andy", '"John, \\" & Fred", Jane'],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=["Name", "Children"])
    base = BaseSheet("", globals, "sheet")
    test_data = [
        (0, [], True, ""),
        (2, ["Fred", "Dick", "Harry"], True, ""),
        (3, ["John", "Jane"], True, ""),
        (4, ["John, & Fred", "Jane"], True, ""),
        (5, ['John, " & Fred', "Jane"], True, ""),
        (6, [], False, ""),
    ]
    for test in test_data:
        errors = globals.errors_and_logging._errors
        errors.clear()
        assert (base.read_cell_multiple_by_name(test[0], "Children")) == test[1]


def test_read_boolean_cell(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        [0, "a"],
        [1, "y"],
        [2, "Y"],
        [3, "true"],
        [4, "True"],
        [5, "yes"],
        [
            6,
            1,
        ],
        [7, "1"],
        [8, ""],
        [9, "T"],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=["Name", "Children"])
    base = BaseSheet("", globals, "sheet")
    test_data = [
        (0, 1, False),
        (1, 1, True),
        (2, 1, True),
        (3, 1, True),
        (4, 1, True),
        (5, 1, True),
        (6, 1, True),
        (7, 1, True),
        (8, 1, False),
        (9, 1, True),
    ]
    for test in test_data:
        assert (base.read_boolean_cell(test[0], test[1])) == test[2]


def test_read_boolean_cell_by_name(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        [0, "a", ""],
        [1, "y", ""],
        [2, "Y", ""],
        [3, "true", ""],
        [4, "True", ""],
        [5, "yes", ""],
        [6, 1, ""],
        [7, "1", ""],
        [8, "", ""],
        [9, "T", ""],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=["Name", "Children", "Other"])
    base = BaseSheet("", globals, "sheet")
    test_data = [
        (0, "Children", False),
        (1, "Children", True),
        (2, "Children", True),
        (3, "Children", True),
        (4, "Children", True),
        (5, "Children", True),
        (6, "Children", True),
        (7, "Children", True),
        (8, "Children", False),
        (9, "Children", True),
        (0, "Other", False),
        (1, "OtherX", False),
    ]
    for test in test_data:
        assert (base.read_boolean_cell_by_name(test[0], test[1])) == test[2]


def test_read_quantity_cell_by_name(mocker, globals):
    globals.cross_references.clear()
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [[""], ["1 days"], [" 1 weeks"], ["14 Hours"], ["14"], [""]]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=["Quantity"])
    base = BaseSheet("", globals, "sheet")
    test_data = [
        #  Name,       Allow Missing Units, Allow Empty, Errors, Empty,  Value,  Unit,     Error
        (
            0,
            "Quantity",
            False,
            False,
            True,
            False,
            0.0,
            "",
            "Error in sheet sheet at [1,1]: Could not decode the quantity value, appears to be empty ''",
        ),
        (1, "Quantity", False, False, False, False, 1.0, "C25301", ""),
        (2, "Quantity", False, False, False, False, 1.0, "C29844", ""),
        (3, "Quantity", False, False, False, False, 14.0, "C25529", ""),
        (4, "Quantity", True, False, False, False, 14.0, "", ""),
        (5, "Quantity", False, True, False, True, 0.0, "", ""),
    ]
    for test in test_data:
        errors = globals.errors_and_logging._errors
        errors.clear()
        item = base.read_quantity_cell_by_name(test[0], test[1], test[2], test[3])
        if not test[4] and not test[5]:
            assert (item.value) == test[6]
            if not test[2]:
                assert (item.unit.standardCode.code) == test[7]
            assert (len(errors.items)) == 0
        elif test[5]:
            assert (item) == None
        else:
            assert (item) == None
            assert (errors.items[0].to_log()) == test[8]


def test_read_range_cell_by_name(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [
        [""],
        ["1..2 days"],
        [" 1 .. 3 weeks"],
        [" .. 3 weeks"],
        ["1 ..  weeks"],
        ["1 . 4 weeks"],
        ["14 Hours"],
        ["14"],
        [""],
    ]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=["Range"])
    base = BaseSheet("", globals, "sheet")
    test_data = [
        #  Name,    Req Units, Allow Empty, Errors, Empty, Min,  Max,   Unit,     Error
        (
            0,
            "Range",
            True,
            False,
            True,
            False,
            0.0,
            0.0,
            "",
            "Error in sheet sheet at [1,1]: Could not decode the range value, appears to be empty ''",
        ),
        (1, "Range", True, False, False, False, 1.0, 2.0, "C25301", ""),
        (2, "Range", True, False, False, False, 1.0, 3.0, "C29844", ""),
        (
            3,
            "Range",
            True,
            False,
            True,
            False,
            0.0,
            0.0,
            "",
            "Error in sheet sheet at [4,1]: Could not decode the range value '.. 3 weeks'",
        ),
        (
            4,
            "Range",
            True,
            False,
            True,
            False,
            0.0,
            0.0,
            "",
            "Error in sheet sheet at [5,1]: Unable to set the units code for the range '1 ..  weeks'",
        ),
        (
            5,
            "Range",
            True,
            False,
            True,
            False,
            0.0,
            0.0,
            "",
            "Error in sheet sheet at [6,1]: Unable to set the units code for the range '1 . 4 weeks'",
        ),
        (6, "Range", True, False, False, False, 14.0, 14.0, "C25529", ""),
        (7, "Range", False, False, False, False, 14.0, 14.0, "", ""),
        (8, "Range", True, True, False, True, 0.0, 0.0, "", ""),
    ]
    for test in test_data:
        globals.errors_and_logging.errors().clear()
        # print(f"INDEX: {test[0]}")
        range = base.read_range_cell_by_name(test[0], test[1], test[2], test[3])
        if not test[4] and not test[5]:
            assert (range.minValue.value) == test[6]
            assert (range.maxValue.value) == test[7]
            if test[2]:
                assert (range.minValue.unit.standardCode.code) == test[8]
            assert (range.isApproximate) == False
            assert (len(globals.errors_and_logging.errors().items)) == 0
        elif test[5]:
            assert (range) == None
        else:
            assert (range) == None
            assert (globals.errors_and_logging.errors().items[0].to_log()) == test[9]


# def test_read_description_by_name(mocker, globals):
#   mock_option = mocker.patch("usdm_excel.om.get")
#   mock_option.side_effect=['xxx', 'xxx', 'xxx']
#   mocked_open = mocker.mock_open(read_data="File")
#   mocker.patch("builtins.open", mocked_open)
#   data = [[0, ''], [1, 'something'], [2, '  ']]
#   mock_read = mocker.patch("pandas.read_excel")
#   mock_read.return_value = pd.DataFrame(data, columns=['Name', 'Children'])
#   base = BaseSheet("", globals, "sheet")
#   test_data = [
#     (0,'Children','xxx'),
#     (1,'Children','something'),
#     (2,'Children','xxx'),
#   ]
#   for test in test_data:
#     assert(base.read_description_by_name(test[0],test[1])) == test[2]


@xfail
def test_read_cell_with_previous():
    assert 0


@xfail
def test_read_other_code_cell_by_name():
    assert 0


@xfail
def test_read_other_code_cell():
    assert 0


@xfail
def test_read_other_code_cell_multiple_by_name():
    assert 0


@xfail
def test_read_other_code_cell_mutiple():
    assert 0


def test_column_present(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = []
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=["Name", "Children"])
    base = BaseSheet("", globals, "sheet")
    assert (base.column_present("Name")) == 0
    assert (base.column_present(["Name"])) == 0
    assert (base.column_present(["Children"])) == 1
    assert (base.column_present(["ChildrenX", "Children"])) == 1
    with pytest.raises(BaseSheet.FormatError):
        assert base.column_present(["Fred"])


def test_read_cdisc_klass_attribute_cell_by_name(mocker, globals):
    expected = Code(
        id="CodeX",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label",
    )
    mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
    mock_code.side_effect = [expected, None]
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [[0, "a"], [1, ""], [2, "c"]]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=["Name", "Children"])
    base = BaseSheet("", globals, "sheet")
    test_data = [
        (0, "Children", expected, ""),
        (
            1,
            "Children",
            None,
            "sheet",
            2,
            2,
            "Empty cell detected where CDISC CT value expected.",
        ),
        (2, "Children", None, "sheet", 3, 2, "CDISC CT not found for value 'c'."),
    ]
    for test in test_data:
        assert (
            base.read_cdisc_klass_attribute_cell_by_name("X", "y", test[0], test[1])
        ) == test[2]
        if not test[3] == "":
            mock_error.assert_called()
            assert mock_error.call_args[0][0] == test[3]
            assert mock_error.call_args[0][1] == test[4]
            assert mock_error.call_args[0][2] == test[5]
            assert mock_error.call_args[0][3] == test[6]


def test_read_cdisc_klass_attribute_cell(mocker, globals):
    expected = Code(
        id="CodeX",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label",
    )
    mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
    mock_code.side_effect = [expected, None]
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "", "c", ""]}
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)
    base = BaseSheet("", globals, "sheet")
    test_data = [
        (0, 1, expected, ""),
        (
            1,
            1,
            None,
            "sheet",
            2,
            2,
            "Empty cell detected where CDISC CT value expected.",
        ),
        (2, 1, None, "sheet", 3, 2, "CDISC CT not found for value 'c'."),
    ]
    for test in test_data:
        assert (
            base.read_cdisc_klass_attribute_cell("X", "y", test[0], test[1])
        ) == test[2]
        if not test[3] == "":
            mock_error.assert_called()
            assert mock_error.call_args[0][0] == test[3]
            assert mock_error.call_args[0][1] == test[4]
            assert mock_error.call_args[0][2] == test[5]
            assert mock_error.call_args[0][3] == test[6]


@xfail
def test_read_cdisc_klass_attribute_cell_multiple_by_name(mocker, globals):
    assert 0


def test_read_cdisc_klass_attribute_cell_multiple(mocker, globals):
    expected_1 = Code(
        id="CodeX1",
        code="code1",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label1",
    )
    expected_2 = Code(
        id="CodeX2",
        code="code2",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label2",
    )
    mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
    mock_code.side_effect = [expected_1, expected_2, None]
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = {"col_1": [3, 2, 1, 0], "col_2": ["a,b", "", "c", ""]}
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)
    base = BaseSheet("", globals, "sheet")
    test_data = [
        (0, 1, [expected_1, expected_2], ""),
        (
            1,
            1,
            [],
            "sheet",
            2,
            2,
            "Empty cell detected where multiple CDISC CT values expected.",
        ),
        (2, 1, [], "sheet", 3, 2, "CDISC CT not found for value 'c'."),
    ]
    for test in test_data:
        assert (
            base.read_cdisc_klass_attribute_cell_multiple("X", "y", test[0], test[1])
        ) == test[2]
        if not test[3] == "":
            mock_error.assert_called()
            assert mock_error.call_args[0][0] == test[3]
            assert mock_error.call_args[0][1] == test[4]
            assert mock_error.call_args[0][2] == test[5]
            assert mock_error.call_args[0][3] == test[6]


def test_read_cdisc_klass_attribute_cell_multiple_by_name(mocker, globals):
    expected_1 = Code(
        id="CodeX1",
        code="code1",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label1",
    )
    expected_2 = Code(
        id="CodeX2",
        code="code2",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label2",
    )
    mock_code = mocker.patch("usdm_excel.cdisc_ct.CDISCCT.code_for_attribute")
    mock_code.side_effect = [expected_1, expected_2, None]
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = [[0, "a,b"], [1, ""], [2, "c"]]
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data, columns=["Name", "Children"])
    base = BaseSheet("", globals, "sheet")
    test_data = [
        (0, "Children", [expected_1, expected_2], ""),
        (
            1,
            "Children",
            [],
            "sheet",
            2,
            2,
            "Empty cell detected where multiple CDISC CT values expected.",
        ),
        (2, "Children", [], "sheet", 3, 2, "CDISC CT not found for value 'c'."),
    ]
    for test in test_data:
        assert (
            base.read_cdisc_klass_attribute_cell_multiple_by_name(
                "X", "y", test[0], test[1]
            )
        ) == test[2]
        if not test[3] == "":
            mock_error.assert_called()
            assert mock_error.call_args[0][0] == test[3]
            assert mock_error.call_args[0][1] == test[4]
            assert mock_error.call_args[0][2] == test[5]
            assert mock_error.call_args[0][3] == test[6]


def test__decode_other_cell(mocker, globals):
    expected = Code(
        id="Code_1", code="c", codeSystem="a", codeSystemVersion="3", decode="d"
    )
    mock_version = mocker.patch("usdm_excel.ct_version_manager.CTVersionManager.get")
    mock_version.side_effect = ["3"]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Code_1"]
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = []
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data)
    base = BaseSheet("", globals, "sheet")
    test_data = [
        ("", 0, 0, None, ""),
        (
            "xxx",
            1,
            1,
            None,
            "sheet",
            2,
            2,
            "Failed to decode code data 'xxx', no ':' detected",
        ),
        (
            "a:",
            1,
            1,
            None,
            "sheet",
            2,
            2,
            "Failed to decode code data 'a:', no '=' detected",
        ),
        (
            "a:c",
            1,
            1,
            None,
            "sheet",
            2,
            2,
            "Failed to decode code data 'a:c', no '=' detected",
        ),
        ("a:c=d", 1, 1, expected, ""),
    ]
    for test in test_data:
        assert (base._decode_other_code(test[0], test[1], test[2])) == test[3]
        if not test[4] == "":
            mock_error.assert_called()
            assert mock_error.call_args[0][0] == test[4]
            assert mock_error.call_args[0][1] == test[5]
            assert mock_error.call_args[0][2] == test[6]
            assert mock_error.call_args[0][3] == test[7]


def test__state_split(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = []
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data)
    base = BaseSheet("", globals, "sheet")
    test_data = [
        ("111", ["111"]),
        ("111,    ", ["111"]),
        ('"111", 222, 333', ["111", "222", "333"]),
        ('"111", 222, 333, "4"', ["111", "222", "333", "4"]),
        ('"111 \\" quote", 222, 333', ['111 " quote', "222", "333"]),
        ('"111 \\" quote",,, 222, 333', ['111 " quote', "", "", "222", "333"]),
    ]
    for test in test_data:
        assert (base._state_split(test[0])) == test[1]

    with pytest.raises(BaseSheet.FormatError):
        base._state_split('123, "456')


def test__to_int(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = []
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame(data)
    base = BaseSheet("", globals, "sheet")
    assert (base._to_int("4")) == 4
    assert (base._to_int("dd")) == None


def test_read_address_cell_by_name(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = {
        "address": [
            "line1, district, city, state, postal code, USA",
            "line1, line2, district, city, state, postal code, USA",
            "line1| line2| district| city| state| postal code| USA",
        ]
    }
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)
    mock_json = mocker.patch("json.load")
    mock_json.side_effect = [{}, {}, {}]
    expected_1 = Code(
        id="Code1",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="USA",
    )
    mock_code = mocker.patch("usdm_excel.iso_3166.ISO3166.code")
    mock_code.side_effect = [expected_1, expected_1, expected_1]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Addr_1", "Addr_2", "Addr_3"]
    base = BaseSheet("", globals, "sheet")
    mock_ta = mocker.patch("usdm_excel.base_sheet.BaseSheet._to_address")
    mock_ta.side_effect = ["success", "success", "success"]
    assert base.read_address_cell_by_name(0, "address") == "success"
    assert base.read_address_cell_by_name(1, "address") == "success"
    assert base.read_address_cell_by_name(2, "address") == "success"
    assert mock_ta.call_count == 3
    expected = [
        mocker.call(
            "Addr_1",
            lines=["line1"],
            district="district",
            city="city",
            state="state",
            postal_code="postal code",
            country=expected_1,
        ),
        mocker.call(
            "Addr_2",
            lines=["line1", "line2"],
            district="district",
            city="city",
            state="state",
            postal_code="postal code",
            country=expected_1,
        ),
        mocker.call(
            "Addr_3",
            lines=["line1", "line2"],
            district="district",
            city="city",
            state="state",
            postal_code="postal code",
            country=expected_1,
        ),
    ]
    mock_ta.assert_has_calls(expected)


def test_read_address_cell_by_name_errors(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = {
        "address": [
            "district, city, state, postal code, USA",
            "",
        ]
    }
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)
    mock_json = mocker.patch("json.load")
    mock_json.side_effect = [{}, {}, {}]
    expected_1 = Code(
        id="Code1",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="USA",
    )
    mock_code = mocker.patch("usdm_excel.iso_3166.ISO3166.code")
    mock_code.side_effect = [expected_1, expected_1, expected_1]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Addr_1", "Addr_2", "Addr_3"]
    base = BaseSheet("", globals, "sheet")
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    assert base.read_address_cell_by_name(0, "address") == None
    assert base.read_address_cell_by_name(1, "address") == None
    assert base.read_address_cell_by_name(1, "address", True) == None
    assert mock_error.call_count == 2
    expected = [
        mocker.call(
            "sheet",
            1,
            1,
            "Address 'district, city, state, postal code, USA' does not contain the required fields (lines, district, city, state, postal code and country code) using ',' separator characters, only 5 found",
            40,
        ),
        mocker.call(
            "sheet",
            2,
            1,
            "Address '' does not contain the required fields (lines, district, city, state, postal code and country code) using ',' separator characters, only 0 found",
            40,
        ),
    ]
    mock_error.assert_has_calls(expected)


def test_read_person_name_cell_by_name(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = {
        "name": [
            "prefix, first, family, suffix",
            "prefix1 prefix2, first1, first2, family, suffix1 suffix2",
        ]
    }
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)
    mock_json = mocker.patch("json.load")
    mock_json.side_effect = [{}, {}, {}]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = ["Name_1", "Name_2"]
    base = BaseSheet("", globals, "sheet")
    result = base.read_person_name_cell_by_name(0, "name")
    assert result.model_dump() == {
        "extensionAttributes": [],
        "familyName": "family",
        "givenNames": ["first"],
        "id": "Name_1",
        "instanceType": "PersonName",
        "prefixes": [
            "prefix",
        ],
        "suffixes": [
            "suffix",
        ],
        "text": "prefix, first, family, suffix",
    }
    result = base.read_person_name_cell_by_name(1, "name")
    assert result.model_dump() == {
        "extensionAttributes": [],
        "familyName": "family",
        "givenNames": ["first1", "first2"],
        "id": "Name_2",
        "instanceType": "PersonName",
        "prefixes": ["prefix1", "prefix2"],
        "suffixes": ["suffix1", "suffix2"],
        "text": "prefix1 prefix2, first1, first2, family, suffix1 suffix2",
    }


def test__to_address(mocker, globals):
    code = Code(
        id="Code1",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="USA",
    )
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = {}
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)
    base = BaseSheet("", globals, "sheet")
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    result = base._to_address(
        "Addr_1", ["line 1"], "city", "district", "state", "postal code", code
    )
    expected = {
        "city": "city",
        "country": {
            "code": "code",
            "codeSystem": "codesys",
            "codeSystemVersion": "3",
            "decode": "USA",
            "id": "Code1",
            "instanceType": "Code",
            "extensionAttributes": [],
        },
        "district": "district",
        "id": "Addr_1",
        "instanceType": "Address",
        "lines": ["line 1"],
        "postalCode": "postal code",
        "state": "state",
        "text": "line 1, city, district, state, postal code, USA",
        "extensionAttributes": [],
    }
    assert result.model_dump() == expected
    result = base._to_address(
        "", ["line 1"], "city", "district", "state", "postal code", code
    )
    assert result == None
    assert mock_error.call_count == 1
    expected = [
        mocker.call(
            "sheet",
            None,
            None,
            "Exception. Failed to create Address object. See log for additional details.",
            40,
        ),
    ]
    mock_error.assert_has_calls(expected)


def test__read_geographic_scopes_cell(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = {"scope": ["Global", "Region: Europe", "Country: FRA", "", "Country=GBR"]}
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)
    mock_json = mocker.patch("json.load")
    mock_json.side_effect = [{}, {}, {}]
    expected_1 = Code(
        id="Code1",
        code="code1",
        codeSystem="country",
        codeSystemVersion="2",
        decode="USA",
    )
    mock_code = mocker.patch("usdm_excel.iso_3166.ISO3166.code")
    mock_code.side_effect = [expected_1]
    expected_2 = Code(
        id="Code4",
        code="code4",
        codeSystem="region",
        codeSystemVersion="3",
        decode="Europe",
    )
    mock_region_code = mocker.patch("usdm_excel.iso_3166.ISO3166.region_code")
    mock_region_code.side_effect = [expected_2]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [
        "Scope_1",
        "Scope_2",
        "Scope_3",
        "Scope_4",
        "Scope_5",
        "Scope_6",
        "Scope_7",
        "Scope_8",
        "Scope_9",
        "Scope_10",
        "Scope_11",
        "Scope_12",
    ]
    base = BaseSheet("", globals, "sheet")
    assert base.read_geographic_scopes_cell(0, 0)[0].model_dump() == {
        "code": None,
        "id": "Scope_2",
        "instanceType": "GeographicScope",
        "type": {
            "code": "C68846",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Global",
            "id": "Scope_1",
            "instanceType": "Code",
            "extensionAttributes": [],
        },
        "extensionAttributes": [],
    }
    assert base.read_geographic_scopes_cell(1, 0)[0].model_dump() == {
        "code": {
            "id": "Scope_4",
            "instanceType": "AliasCode",
            "standardCode": {
                "code": "code4",
                "codeSystem": "region",
                "codeSystemVersion": "3",
                "decode": "Europe",
                "id": "Code4",
                "instanceType": "Code",
                "extensionAttributes": [],
            },
            "standardCodeAliases": [],
            "extensionAttributes": [],
        },
        "id": "Scope_5",
        "instanceType": "GeographicScope",
        "type": {
            "code": "C41129",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Region",
            "id": "Scope_3",
            "instanceType": "Code",
            "extensionAttributes": [],
        },
        "extensionAttributes": [],
    }
    assert base.read_geographic_scopes_cell(2, 0)[0].model_dump() == {
        "code": {
            "id": "Scope_7",
            "instanceType": "AliasCode",
            "standardCode": {
                "code": "code1",
                "codeSystem": "country",
                "codeSystemVersion": "2",
                "decode": "USA",
                "id": "Code1",
                "instanceType": "Code",
                "extensionAttributes": [],
            },
            "standardCodeAliases": [],
            "extensionAttributes": [],
        },
        "id": "Scope_8",
        "instanceType": "GeographicScope",
        "type": {
            "code": "C25464",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Country",
            "id": "Scope_6",
            "instanceType": "Code",
            "extensionAttributes": [],
        },
        "extensionAttributes": [],
    }
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    assert base.read_geographic_scopes_cell(3, 0)[0].model_dump() == {
        "code": None,
        "id": "Scope_10",
        "instanceType": "GeographicScope",
        "type": {
            "code": "C68846",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Global",
            "id": "Scope_9",
            "instanceType": "Code",
            "extensionAttributes": [],
        },
        "extensionAttributes": [],
    }
    assert base.read_geographic_scopes_cell(4, 0)[0].model_dump() == {
        "code": None,
        "id": "Scope_12",
        "instanceType": "GeographicScope",
        "type": {
            "code": "C68846",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Global",
            "id": "Scope_11",
            "instanceType": "Code",
            "extensionAttributes": [],
        },
        "extensionAttributes": [],
    }
    assert mock_error.call_count == 2
    expected = [
        mocker.call(
            "sheet",
            4,
            1,
            "Empty cell detected where geographic scope values expected, assuming global scope.",
            30,
        ),
        mocker.call(
            "sheet",
            5,
            1,
            "Failed to decode geographic scope 'Country=GBR'. Formats are 'Global', 'Region: <value>' or 'Country: <value>'. Assuming global scope.",
            30,
        ),
    ]
    mock_error.assert_has_calls(expected)


def test__read_geographic_scopes_cell_by_name(mocker, globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = {
        "region": [
            "Region: Europe",
        ]
    }
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)
    mock_json = mocker.patch("json.load")
    mock_json.side_effect = [{}]
    expected_1 = Code(
        id="Code1",
        code="code1",
        codeSystem="country",
        codeSystemVersion="2",
        decode="USA",
    )
    mock_code = mocker.patch("usdm_excel.iso_3166.ISO3166.code")
    mock_code.side_effect = [expected_1]
    expected_2 = Code(
        id="Code4",
        code="code4",
        codeSystem="region",
        codeSystemVersion="3",
        decode="Europe",
    )
    mock_region_code = mocker.patch("usdm_excel.iso_3166.ISO3166.region_code")
    mock_region_code.side_effect = [expected_2]
    mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
    mock_id.side_effect = [
        "Scope_1",
        "Scope_2",
        "Scope_3",
        "Scope_4",
        "Scope_5",
        "Scope_6",
        "Scope_7",
        "Scope_8",
        "Scope_9",
    ]
    base = BaseSheet("", globals, "sheet")
    assert base.read_geographic_scopes_cell_by_name(0, "region")[0].model_dump() == {
        "code": {
            "id": "Scope_2",
            "instanceType": "AliasCode",
            "standardCode": {
                "code": "code4",
                "codeSystem": "region",
                "codeSystemVersion": "3",
                "decode": "Europe",
                "id": "Code4",
                "instanceType": "Code",
                "extensionAttributes": [],
            },
            "standardCodeAliases": [],
            "extensionAttributes": [],
        },
        "id": "Scope_3",
        "instanceType": "GeographicScope",
        "type": {
            "code": "C41129",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Region",
            "id": "Scope_1",
            "instanceType": "Code",
            "extensionAttributes": [],
        },
        "extensionAttributes": [],
    }
    assert base.read_geographic_scopes_cell_by_name(1, "regionxxx")[0].model_dump() == {
        "code": None,
        "id": "Scope_5",
        "instanceType": "GeographicScope",
        "type": {
            "code": "C68846",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
            "decode": "Global",
            "id": "Scope_4",
            "instanceType": "Code",
            "extensionAttributes": [],
        },
        "extensionAttributes": [],
    }
