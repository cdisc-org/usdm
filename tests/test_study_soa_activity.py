import pandas as pd
from tests.test_factory import Factory
from usdm_excel.globals import Globals
from usdm_model.procedure import Procedure
from usdm_model.biomedical_concept import BiomedicalConcept
from usdm_model.schedule_timeline import ScheduleTimeline
from usdm_model.activity import Activity
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_v2_sheet.soa_activity import SoAActivity


def test_read_bc(mocker, globals):
    bcs, procedures, timelines, activities = _data(globals)
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [activities[0], bcs[0], None, None]
    base_sheet = _setup(mocker, globals)
    activity_map = {}
    item = SoAActivity(base_sheet, 0, activity_map)
    assert item._bcs == ["BC1"]
    assert item._prs == []
    assert item._tls == []
    assert item._parent_name == ""
    assert item._child_name == "Activity 1"
    usdm_activity = item.activity
    assert usdm_activity.name == "Activity 1"
    assert usdm_activity.label == "Activity One"
    assert usdm_activity.description == None
    assert usdm_activity.biomedicalConceptIds == []
    assert usdm_activity.bcCategoryIds == []
    assert usdm_activity.bcSurrogateIds == ["BiomedicalConceptSurrogate_1"]
    assert usdm_activity.definedProcedures == []
    assert usdm_activity.timelineId == None


def test_read_procedure(mocker, globals):
    bcs, procedures, timelines, activities = _data(globals)
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [procedures[0], None, None]
    base_sheet = _setup(mocker, globals)
    activity_map = {}
    item = SoAActivity(base_sheet, 1, activity_map)
    assert item._bcs == []
    assert item._prs == ["Procedure"]
    assert item._tls == []
    assert item._parent_name == ""
    assert item._child_name == "Activity 2"
    usdm_activity = item.activity
    assert usdm_activity.name == "Activity 2"
    assert usdm_activity.label == "Activity 2"
    assert usdm_activity.description == "Activity 2"
    assert usdm_activity.biomedicalConceptIds == []
    assert usdm_activity.bcCategoryIds == []
    assert usdm_activity.bcSurrogateIds == []
    assert usdm_activity.definedProcedures == [procedures[0]]
    assert usdm_activity.timelineId == None


def test_read_procedure_error(mocker, globals):
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    bcs, procedures, timelines, activities = _data(globals)
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [None, activities[0], None]
    base_sheet = _setup(mocker, globals)
    activity_map = {}
    item = SoAActivity(base_sheet, 1, activity_map)
    assert item._bcs == []
    assert item._prs == ["Procedure"]
    assert item._tls == []
    assert item._parent_name == ""
    assert item._child_name == "Activity 2"
    usdm_activity = item.activity
    assert usdm_activity.name == "Activity 1"
    assert usdm_activity.label == "Activity One"
    assert usdm_activity.description == None
    assert usdm_activity.biomedicalConceptIds == []
    assert usdm_activity.bcCategoryIds == []
    assert usdm_activity.bcSurrogateIds == []
    assert usdm_activity.definedProcedures == []
    assert usdm_activity.timelineId == None
    mock_error.assert_called()
    assert mock_error.call_args[0][0] == "sheet"
    assert mock_error.call_args[0][1] == 2
    assert mock_error.call_args[0][2] == 3
    assert (
        mock_error.call_args[0][3]
        == "No procedure 'Procedure' found, missing cross reference"
    )


def test_read_timeline(mocker, globals):
    bcs, procedures, timelines, activities = _data(globals)
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [timelines[0], None, None]
    base_sheet = _setup(mocker, globals)
    activity_map = {}
    item = SoAActivity(base_sheet, 2, activity_map)
    assert item._bcs == []
    assert item._prs == []
    assert item._tls == ["Timeline"]
    assert item._parent_name == ""
    assert item._child_name == "Activity 3"
    usdm_activity = item.activity
    assert usdm_activity.name == "Activity 3"
    assert usdm_activity.label == "Activity 3"
    assert usdm_activity.description == "Activity 3"
    assert usdm_activity.biomedicalConceptIds == []
    assert usdm_activity.bcCategoryIds == []
    assert usdm_activity.bcSurrogateIds == []
    assert usdm_activity.definedProcedures == []
    assert usdm_activity.timelineId == "ScheduleTimeline_1"


def test_read_timeline_error(mocker, globals):
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    bcs, procedures, timelines, activities = _data(globals)
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [None, activities[0], None]
    base_sheet = _setup(mocker, globals)
    activity_map = {}
    item = SoAActivity(base_sheet, 2, activity_map)
    assert item._bcs == []
    assert item._prs == []
    assert item._tls == ["Timeline"]
    assert item._parent_name == ""
    assert item._child_name == "Activity 3"
    usdm_activity = item.activity
    assert usdm_activity.name == "Activity 1"
    assert usdm_activity.label == "Activity One"
    assert usdm_activity.description == None
    assert usdm_activity.biomedicalConceptIds == []
    assert usdm_activity.bcCategoryIds == []
    assert usdm_activity.bcSurrogateIds == []
    assert usdm_activity.definedProcedures == []
    assert usdm_activity.timelineId == None
    mock_error.assert_called()
    assert mock_error.call_args[0][0] == "sheet"
    assert mock_error.call_args[0][1] == 3
    assert mock_error.call_args[0][2] == 3
    assert (
        mock_error.call_args[0][3]
        == "No timeline 'Timeline' found, missing cross reference"
    )


def test_read_all(mocker, globals):
    bcs, procedures, timelines, activities = _data(globals)
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [timelines[0], procedures[0], None]
    base_sheet = _setup(mocker, globals)
    activity_map = {}
    item = SoAActivity(base_sheet, 3, activity_map)
    assert item._bcs == ["BC1"]
    assert item._prs == ["Procedure"]
    assert item._tls == ["Timeline"]
    assert item._parent_name == ""
    assert item._child_name == "Activity 4"
    usdm_activity = item.activity
    assert usdm_activity.name == "Activity 4"
    assert usdm_activity.label == "Activity 4"
    assert usdm_activity.description == "Activity 4"
    assert usdm_activity.biomedicalConceptIds == []
    assert usdm_activity.bcCategoryIds == []
    assert usdm_activity.bcSurrogateIds == ["BiomedicalConceptSurrogate_1"]
    assert usdm_activity.definedProcedures == [procedures[0]]
    assert usdm_activity.timelineId == "ScheduleTimeline_1"


def test_read_parent(mocker, globals):
    bcs, procedures, timelines, activities = _data(globals)
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [activities[2], None]
    base_sheet = _setup(mocker, globals)
    activity_map = {}
    item = SoAActivity(base_sheet, 4, activity_map)
    assert item._bcs == ["BC1"]
    assert item._prs == ["Procedure"]
    assert item._tls == ["Timeline"]
    assert item._parent_name == "Parent 1"
    assert item._child_name == ""
    usdm_activity = item.activity
    assert usdm_activity.name == "Parent 1"
    assert usdm_activity.label == "Parent One"
    assert usdm_activity.description == None
    assert usdm_activity.biomedicalConceptIds == []
    assert usdm_activity.bcCategoryIds == []
    assert usdm_activity.bcSurrogateIds == []
    assert usdm_activity.definedProcedures == []
    assert usdm_activity.timelineId == None


def test_read_parent_ignore_child(mocker, globals):
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    bcs, procedures, timelines, activities = _data(globals)
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [None, None]
    base_sheet = _setup(mocker, globals)
    activity_map = {}
    item = SoAActivity(base_sheet, 5, activity_map)
    assert item._bcs == []
    assert item._prs == []
    assert item._tls == []
    assert item._parent_name == "Parent 2"
    assert item._child_name == "Activity 5"
    usdm_activity = item.activity
    assert usdm_activity.name == "Parent 2"
    assert usdm_activity.label == "Parent 2"
    assert usdm_activity.description == "Parent 2"
    assert usdm_activity.biomedicalConceptIds == []
    assert usdm_activity.bcCategoryIds == []
    assert usdm_activity.bcSurrogateIds == []
    assert usdm_activity.definedProcedures == []
    assert usdm_activity.timelineId == None
    assert mock_error.call_count == 2
    mock_error.assert_has_calls(
        [
            mocker.call(
                "sheet",
                6,
                2,
                "Both parent 'Parent 2' and child activity 'Activity 5' found, child has been ignored",
                30,
            ),
            mocker.call(
                "sheet",
                6,
                3,
                "No activity 'Parent 2' found, so one has been created",
                30,
            ),
        ]
    )


def test_read_parent_repeated(mocker, globals):
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    bcs, procedures, timelines, activities = _data(globals)
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [None, None]
    base_sheet = _setup(mocker, globals)
    activity_map = {"Parent 1"}
    item = SoAActivity(base_sheet, 4, activity_map)
    assert item._bcs == ["BC1"]
    assert item._prs == ["Procedure"]
    assert item._tls == ["Timeline"]
    assert item._parent_name == "Parent 1"
    assert item._child_name == ""
    assert item.activity is None
    assert mock_error.call_count == 1
    mock_error.assert_has_calls(
        [
            mocker.call(
                "sheet",
                5,
                1,
                "Parent activity 'Parent 1' has already been referenced in the SoA, parent has been ignored",
                40,
            )
        ]
    )


def test_read_child_repeated(mocker, globals):
    mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
    bcs, procedures, timelines, activities = _data(globals)
    mock_cross_ref = mocker.patch("usdm_excel.cross_ref.CrossRef.get")
    mock_cross_ref.side_effect = [None, None]
    base_sheet = _setup(mocker, globals)
    activity_map = {"Activity 1"}
    item = SoAActivity(base_sheet, 0, activity_map)
    assert item._bcs == ["BC1"]
    assert item._prs == []
    assert item._tls == []
    assert item._parent_name == ""
    assert item._child_name == "Activity 1"
    assert item.activity is None
    assert mock_error.call_count == 1
    mock_error.assert_has_calls(
        [
            mocker.call(
                "sheet",
                1,
                2,
                "Child activity 'Activity 1' has already been referenced in the SoA, child has been ignored",
                40,
            )
        ]
    )


def _setup(mocker, globals: Globals):
    mocked_open = mocker.mock_open(read_data="File")
    mocker.patch("builtins.open", mocked_open)
    data = {
        "col_1": ["", "", "", "", "Parent 1", "Parent 2"],
        "col_2": [
            "Activity 1",
            "Activity 2",
            "Activity 3",
            "Activity 4",
            "",
            "Activity 5",
        ],
        "col_3": [
            "BC: BC1",
            "PR: Procedure",
            "TL: Timeline",
            "BC: BC1, PR: Procedure, TL: Timeline",
            "BC: BC1, PR: Procedure, TL: Timeline",
            "",
        ],
    }
    mock_read = mocker.patch("pandas.read_excel")
    mock_read.return_value = pd.DataFrame.from_dict(data)
    return BaseSheet("", globals, "sheet")


def _data(globals: Globals):
    globals.id_manager.clear()
    factory = Factory(globals)
    item_list = [
        {
            "name": "PR1",
            "label": "Procedure 1",
            "description": "Procedure One",
            "procedureType": "PR1",
            "code": factory.cdisc_dummy(),
        },
        {
            "name": "PR2",
            "label": "Procedure 2",
            "description": "Procedure Two",
            "procedureType": "PR2",
            "code": factory.cdisc_dummy(),
        },
    ]
    procedures = factory.set(Procedure, item_list)

    item_list = [
        {
            "name": "TL1",
            "label": "Timeline 1",
            "description": "Timeline One",
            "mainTimeline": False,
            "entryCondition": "",
            "entryId": "",
            "procedureType": "PR1",
            "code": factory.cdisc_dummy(),
        },
        {
            "name": "TL2",
            "label": "Timeline 2",
            "description": "Timeline Two",
            "mainTimeline": False,
            "entryCondition": "",
            "entryId": "",
            "procedureType": "PR2",
            "code": factory.cdisc_dummy(),
        },
    ]
    timelines = factory.set(ScheduleTimeline, item_list)

    item_list = [
        {
            "name": "BC1",
            "label": "Biomedicall Concept 1",
            "reference": "BC REF 1",
            "code": factory.alias_code(factory.cdisc_dummy()),
        },
        {
            "name": "BC2",
            "label": "Biomedicall Concept 2",
            "reference": "BC REF 2",
            "code": factory.alias_code(factory.cdisc_dummy()),
        },
    ]
    bcs = factory.set(BiomedicalConcept, item_list)

    item_list = [
        {"name": "Activity 1", "label": "Activity One"},
        {"name": "Activity 2", "label": "Activity Two"},
        {"name": "Parent 1", "label": "Parent One"},
    ]
    activities = factory.set(Activity, item_list)

    return bcs, procedures, timelines, activities
