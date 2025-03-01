from bs4 import BeautifulSoup
from usdm_excel.document.soa import SoA
from usdm_model.activity import Activity
from usdm_model.study_epoch import StudyEpoch
from usdm_model.study_cell import StudyCell
from usdm_model.study_arm import StudyArm
from usdm_model.encounter import Encounter
from usdm_model.study_design import InterventionalStudyDesign
from usdm_model.study_version import StudyVersion
from usdm_model.schedule_timeline import ScheduleTimeline
from usdm_model.scheduled_instance import ScheduledActivityInstance
from usdm_model.schedule_timeline_exit import ScheduleTimelineExit
from usdm_model.population_definition import StudyDesignPopulation
from usdm_model.study_title import StudyTitle
from usdm_model.organization import Organization
from usdm_model.identifier import StudyIdentifier
from usdm_model.timing import Timing
from usdm_model.condition import Condition


def translate_reference(text, globals):
    soup = BeautifulSoup(str(text), "html.parser")
    for ref in soup(["usdm:ref"]):
        attributes = ref.attrs
        instance = globals.cross_references.get_by_id(
            attributes["klass"], attributes["id"]
        )
        value = str(getattr(instance, attributes["attribute"]))
        ref.replace_with(value)
    return str(soup)


def double_link(items, prev, next):
    for idx, item in enumerate(items):
        if idx == 0:
            setattr(item, prev, None)
        else:
            the_id = getattr(items[idx - 1], "id")
            setattr(item, prev, the_id)
        if idx == len(items) - 1:
            setattr(item, next, None)
        else:
            the_id = getattr(items[idx + 1], "id")
            setattr(item, next, the_id)


def add_cross_ref(collection, globals):
    for item in collection:
        globals.cross_references.add(item.id, item)


def create_populations(factory, globals):
    item_list = [
        {
            "name": "POP1",
            "includesHealthySubjects": True,
            "plannedEnrollmentNumber": None,
            "plannedCompletionNumber": None,
            "plannedSex": [],
            "criterionIds": [],
            "plannedAge": None,
        },
    ]
    results = factory.set(StudyDesignPopulation, item_list)
    add_cross_ref(results, globals)
    return results


def create_conditions(factory, globals):
    item_list = [
        {
            "name": "COND1",
            "label": "",
            "description": "",
            "text": "Only perform at baseline",
            "appliesToIds": [],
            "contextIds": [],
        },
        {
            "name": "COND2",
            "label": "",
            "description": "",
            "text": "Only perform on males",
            "appliesToIds": [],
            "contextIds": [],
        },
    ]
    results = factory.set(Condition, item_list)
    add_cross_ref(results, globals)
    return results


def create_timings(factory, globals):
    FIXED = factory.cdisc_code("C201358", "Fixed Reference")
    BEFORE = factory.cdisc_code("C201356", "After")
    AFTER = factory.cdisc_code("C201357", "Before")

    E2E = factory.cdisc_code("C201352", "End to End")
    E2S = factory.cdisc_code("C201353", "End to Start")
    S2E = factory.cdisc_code("C201354", "Start to End")
    S2S = factory.cdisc_code("C201355", "Start to Start")

    item_list = [
        {
            "name": "T1",
            "label": "-2 Days",
            "description": "",
            "type": BEFORE,
            "value": "",
            "valueLabel": "",
            "relativeToFrom": S2S,
            "relativeFromScheduledInstanceId": "",
            "relativeToScheduledInstanceId": "",
            "windowLower": "",
            "windowUpper": "",
            "windowLabel": "",
        },
        {
            "name": "T2",
            "label": "Dose",
            "description": "",
            "type": FIXED,
            "value": "",
            "valueLabel": "",
            "relativeToFrom": S2S,
            "relativeFromScheduledInstanceId": "",
            "relativeToScheduledInstanceId": "",
            "windowLower": "",
            "windowUpper": "",
            "windowLabel": "",
        },
        {
            "name": "T3",
            "label": "7 Days",
            "description": "",
            "type": AFTER,
            "value": "",
            "valueLabel": "",
            "relativeToFrom": S2S,
            "relativeFromScheduledInstanceId": "",
            "relativeToScheduledInstanceId": "",
            "windowLower": "",
            "windowUpper": "",
            "windowLabel": "1..1 Days",
        },
    ]
    results = factory.set(Timing, item_list)
    add_cross_ref(results, globals)
    return results


def create_activities(factory, globals):
    item_list = [
        {
            "name": "A1",
            "label": "Activity 1",
            "description": "",
            "definedProcedures": [],
            "biomedicalConceptIds": [],
            "bcCategoryIds": [],
            "bcSurrogateIds": [],
            "timelineId": None,
        },
        {
            "name": "A2",
            "label": "Activity 2",
            "description": "",
            "definedProcedures": [],
            "biomedicalConceptIds": [],
            "bcCategoryIds": [],
            "bcSurrogateIds": [],
            "timelineId": None,
        },
        {
            "name": "A3",
            "label": "Activity 3",
            "description": "",
            "definedProcedures": [],
            "biomedicalConceptIds": [],
            "bcCategoryIds": [],
            "bcSurrogateIds": [],
            "timelineId": None,
        },
        {
            "name": "A4",
            "label": "Activity 4",
            "description": "",
            "definedProcedures": [],
            "biomedicalConceptIds": [],
            "bcCategoryIds": [],
            "bcSurrogateIds": [],
            "timelineId": None,
        },
        {
            "name": "A5",
            "label": "Activity 5",
            "description": "",
            "definedProcedures": [],
            "biomedicalConceptIds": [],
            "bcCategoryIds": [],
            "bcSurrogateIds": [],
            "timelineId": None,
        },
    ]
    results = factory.set(Activity, item_list)
    double_link(results, "previousId", "nextId")
    add_cross_ref(results, globals)
    return results


def create_epochs(factory, globals):
    item_list = [
        {
            "name": "EP1",
            "label": "Epoch A",
            "description": "",
            "type": factory.cdisc_dummy(),
        },
        {
            "name": "EP2",
            "label": "Epoch B",
            "description": "",
            "type": factory.cdisc_dummy(),
        },
        {
            "name": "EP3",
            "label": "Epoch C",
            "description": "",
            "type": factory.cdisc_dummy(),
        },
    ]
    results = factory.set(StudyEpoch, item_list)
    double_link(results, "previousId", "nextId")
    add_cross_ref(results, globals)
    return results


def create_encounters(factory, globals):
    item_list = [
        {
            "name": "E1",
            "label": "Screening",
            "description": "",
            "type": factory.cdisc_dummy(),
            "environmentalSetting": [],
            "contactModes": [],
            "transitionStartRule": None,
            "transitionEndRule": None,
            "scheduledAtId": None,
        },
        {
            "name": "E2",
            "label": "Dose",
            "description": "",
            "type": factory.cdisc_dummy(),
            "environmentalSetting": [],
            "contactModes": [],
            "transitionStartRule": None,
            "transitionEndRule": None,
            "scheduledAtId": None,
        },
        {
            "name": "E3",
            "label": "Check Up",
            "description": "",
            "type": factory.cdisc_dummy(),
            "environmentalSetting": [],
            "contactModes": [],
            "transitionStartRule": None,
            "transitionEndRule": None,
            "scheduledAtId": None,
        },
    ]
    results = factory.set(Encounter, item_list)
    double_link(results, "previousId", "nextId")
    add_cross_ref(results, globals)
    return results


def create_activity_instances(factory, globals):
    item_list = [
        {
            "name": "SAI_1",
            "description": "",
            "label": "",
            "timelineExitId": None,
            "encounterId": None,
            "scheduledInstanceTimelineId": None,
            "defaultConditionId": None,
            "epochId": None,
            "activityIds": [],
        },
        {
            "name": "SAI_2",
            "description": "",
            "label": "",
            "timelineExitId": None,
            "encounterId": None,
            "scheduledInstanceTimelineId": None,
            "defaultConditionId": None,
            "epochId": None,
            "activityIds": [],
        },
        {
            "name": "SAI_3",
            "description": "",
            "label": "",
            "timelineExitId": None,
            "encounterId": None,
            "scheduledInstanceTimelineId": None,
            "defaultConditionId": None,
            "epochId": None,
            "activityIds": [],
        },
    ]
    results = factory.set(ScheduledActivityInstance, item_list)
    results[0].defaultConditionId = results[1].id
    results[1].defaultConditionId = results[2].id
    add_cross_ref(results, globals)
    return results


def scenario_1(factory, globals):
    dummy_cell = factory.item(
        StudyCell, {"armId": "X", "epochId": "Y", "elementIds": ["Z"]}
    )
    dummy_arm = factory.item(
        StudyArm,
        {
            "name": "Arm1",
            "type": factory.cdisc_dummy(),
            "dataOriginDescription": "xxx",
            "dataOriginType": factory.cdisc_dummy(),
        },
    )
    activities = create_activities(factory, globals)
    epochs = create_epochs(factory, globals)
    encounters = create_encounters(factory, globals)
    activity_instances = create_activity_instances(factory, globals)
    timings = create_timings(factory, globals)
    conditions = create_conditions(factory, globals)

    activity_instances[0].activityIds = [activities[0].id, activities[1].id]
    activity_instances[0].encounterId = encounters[0].id
    activity_instances[0].epochId = epochs[0].id
    activity_instances[1].activityIds = [activities[1].id, activities[2].id]
    activity_instances[1].encounterId = encounters[1].id
    activity_instances[1].epochId = epochs[1].id
    activity_instances[2].activityIds = [
        activities[2].id,
        activities[3].id,
        activities[4].id,
    ]
    activity_instances[2].encounterId = encounters[2].id
    activity_instances[2].epochId = epochs[2].id
    timings[0].relativeFromScheduledInstanceId = activity_instances[0].id
    timings[0].relativeToScheduledInstanceId = activity_instances[1].id
    timings[1].relativeFromScheduledInstanceId = activity_instances[1].id
    timings[1].relativeToScheduledInstanceId = activity_instances[1].id
    timings[2].relativeFromScheduledInstanceId = activity_instances[2].id
    timings[2].relativeToScheduledInstanceId = activity_instances[1].id
    conditions[0].appliesToIds = [activities[0].id]
    conditions[0].contextIds = [activity_instances[0].id]
    conditions[1].appliesToIds = [activities[3].id]
    populations = create_populations(factory, globals)

    exit = factory.item(ScheduleTimelineExit, {})
    activity_instances[-1].timelineExitId = exit.id
    timeline = factory.item(
        ScheduleTimeline,
        {
            "name": "Study Design",
            "label": "",
            "description": "",
            "mainTimeline": True,
            "entryCondition": "Condition",
            "entryId": activity_instances[0].id,
            "exits": [exit],
            "instances": activity_instances,
            "timings": timings,
        },
    )
    model_code = factory.cdisc_code("C12345", "Model Code")
    phase_code = factory.cdisc_code("C12345", "Phase Code")
    alias_phase = factory.alias_code(phase_code, [])
    study_design = factory.item(
        InterventionalStudyDesign,
        {
            "name": "Study Design",
            "label": "",
            "description": "",
            "studyPhase": alias_phase,
            "rationale": "XXX",
            "interventionModel": factory.cdisc_dummy(),
            "arms": [dummy_arm],
            "studyCells": [dummy_cell],
            "epochs": epochs,
            "activities": activities,
            "scheduledTimelines": [timeline],
            "population": populations[0],
            "model": model_code,
        },
    )

    study_title = factory.item(
        StudyTitle,
        {
            "text": "Title",
            "type": factory.cdisc_code("C44444", "Official Study Title"),
        },
    )
    organization_1 = factory.item(
        Organization,
        {
            "name": "Sponsor",
            "type": factory.cdisc_code("C188863", "reg 1"),
            "identifier": "REG 1",
            "identifierScheme": "DUNS",
            "legalAddress": None,
        },
    )
    identifier = factory.item(
        StudyIdentifier, {"text": "SPONSOR-1234", "scopeId": organization_1.id}
    )
    study_version = factory.item(
        StudyVersion,
        {
            "versionIdentifier": "1",
            "rationale": "Study version rationale",
            "titles": [study_title],
            "studyDesigns": [study_design],
            "documentVersionId": None,
            "studyIdentifiers": [identifier],
            "dateValues": [],
            "amendments": [],
            "organizations": [organization_1],
            "conditions": conditions,
        },
    )
    return study_version, study_design, timeline


def test_create(mocker, globals, factory):
    bs = factory.base_sheet(mocker)
    study_version, study_design, timeline = scenario_1(factory, globals)
    soa = SoA(bs, study_version, study_design, timeline)
    result = soa.generate()
    # print(f"RESULT: {result}")
    labels = []
    for row in range(len(result)):
        labels.append([])
        for col in range(len(result[row])):
            if "set" in result[row][col].keys():
                label = "X" if result[row][col]["set"] else ""
            else:
                label = translate_reference(result[row][col]["label"], globals)
            if "condition" in result[row][col].keys():
                label = f"{label} [c]"
            labels[row].append(label)
    assert labels == [
        # ['',           '0',            '1',            '2'],
        ["", "Epoch A", "Epoch B", "Epoch C"],
        ["", "Screening", "Dose", "Check Up"],
        ["", "-2 Days", "Dose", "7 Days"],
        ["", "", "", "1..1 Days"],
        ["Activity 1", "X [c]", "", ""],
        ["Activity 2", "X", "X", ""],
        ["Activity 3", "", "X", "X"],
        ["Activity 4 [c]", "", "", "X"],
        ["Activity 5", "", "", "X"],
    ]
