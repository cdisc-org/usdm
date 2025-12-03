import pytest

xfail = pytest.mark.xfail



@xfail
def test_create(mocker, globals):
    assert 0
    # mocked_open = mocker.mock_open(read_data="File")
    # mocker.patch("builtins.open", mocked_open)
    # mock_read = mocker.patch("pandas.read_excel")
    # data = {
    #   'col_1':
    #     [ 'studyTitle', 'studyVersion', 'studyType', 'studyPhase', 'studyAcronym', 'studyRationale',
    #       'businessTherapueticAreas', '', 'briefTitle', 'Something brief' ],
    #   'col_2':
    #     [ 'title', '1', 'Interventional Study', 'C15602', 'BEAST', 'Damn good',
    #       '', '', 'officalTitle', 'Very offical' ],
    #   'col_3': [ '', '', '', '', '', '', '', '', 'publicTitle', 'Open' ],
    #   'col_4': [ '', '', '', '', '', '', '', '', 'scientificTitle', 'Blah blah blah' ],
    #   'col_5': [ '', '', '', '', '', '', '', '', 'protocolVersion', '1' ],
    #   'col_6': [ '', '', '', '', '', '', '', '', 'protocolAmendment', 'A' ],
    #   'col_7': [ '', '', '', '', '', '', '', '', 'protocolEffectiveDate', '2010-01-01 00:00:00' ],
    #   'col_8': [ '', '', '', '', '', '', '', '', 'protocolStatus', 'draft' ],
    #   }
    # mock_read.return_value = pd.DataFrame.from_dict(data)
    # study = StudySheet("")
    # assert(study.study.studyTitle) == 'title'
    # assert(study.study.studyVersion) == '1'
