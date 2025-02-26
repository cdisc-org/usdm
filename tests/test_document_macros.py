import base64
from tests.test_data_factory import MinimalStudy
from usdm_model.eligibility_criterion import (
    EligibilityCriterion,
    EligibilityCriterionItem,
)
from usdm_model.biomedical_concept import BiomedicalConcept
from usdm_model.activity import Activity
from usdm_model.abbreviation import Abbreviation
from usdm_excel.document.macros import Macros
from usdm_excel.globals import Globals
from tests.test_factory import Factory


def create_criteria(factory: Factory, minimal: MinimalStudy):
    INCLUSION = factory.cdisc_code("C25532", "Inc")
    EXCLUSION = factory.cdisc_code("C25370", "Exc")
    eci_list = [
        {
            "name": "ECI1",
            "text": "Only perform at baseline",
            "dictionaryId": None,
        },
        {
            "name": "ECI2",
            "text": "<p>Only perform on males</p>",
            "dictionaryId": None,
        },
    ]
    eci_results = factory.set(EligibilityCriterionItem, eci_list)
    ec_list = [
        {
            "name": "IE1",
            "label": "",
            "description": "",
            "category": INCLUSION,
            "identifier": "01",
            "nextId": None,
            "previousId": None,
            "contextId": None,
            "criterionItemId": eci_results[0].id,
        },
        {
            "name": "IE2",
            "label": "",
            "description": "",
            "category": INCLUSION,
            "identifier": "02",
            "nextId": None,
            "previousId": None,
            "contextId": None,
            "criterionItemId": eci_results[1].id,
        },
    ]
    results = factory.set(EligibilityCriterion, ec_list)
    # print(f"RESULTS: {results}")
    for criterion in results:
        minimal.population.criterionIds.append(criterion.id)
    minimal.study.versions[0].eligibilityCriterionItems = eci_results
    minimal.study.versions[0].studyDesigns[0].eligibilityCriteria = results
    return results


def create_bc(factory: Factory, globals: Globals):
    code = factory.cdisc_dummy()
    alias_code = factory.alias_code(code)
    bc = factory.item(
        BiomedicalConcept,
        {
            "name": "height",
            "label": "bc name",
            "reference": "something",
            "code": alias_code,
            "synonyms": ["body height", "Standing height"],
        },
    )
    activity = factory.item(
        Activity, {"name": "vitals", "biomedicalConceptIds": [bc.id]}
    )
    globals.cross_references.add(bc.id, bc)
    globals.cross_references.add(activity.name, activity)


def create_abbreviations(factory: Factory, globals: Globals):
    abbreviations = [
        {"abbreviatedText": "XXX", "expandedText": "X is X very X long"},
        {"abbreviatedText": "ECG", "expandedText": "Electrocardiogram"},
        {"abbreviatedText": "AD", "expandedText": "Alzheimer's"},
    ]
    for abbreviation in abbreviations:
        item = factory.item(Abbreviation, abbreviation)
        globals.cross_references.add(item.abbreviatedText, item)


def get_instance(mocker, globals: Globals, factory: Factory, minimal: MinimalStudy):
    globals.id_manager.clear()
    criteria = create_criteria(factory, minimal)
    bs = factory.base_sheet(mocker)
    macro = Macros(bs, minimal.study_version, minimal.study_definition_document_version)
    return macro


def test_create(mocker, globals, factory, minimal):
    macro = get_instance(mocker, globals, factory, minimal)
    assert macro is not None


def test_resolve_ok(mocker, globals, factory, minimal):
    macro = get_instance(mocker, globals, factory, minimal)
    result = macro.resolve('<usdm:macro id="section" name="inclusion"/>')
    expected = (
        '<table class="table"><tr><td>01</td><td><usdm:ref attribute="text" '
        'id="EligibilityCriterionItem_1" klass="EligibilityCriterionItem"></usdm:ref></td></tr><tr><td>02'
        '</td><td><usdm:ref attribute="text" id="EligibilityCriterionItem_2" klass="EligibilityCriterionItem">'
        "</usdm:ref></td></tr></table>"
    )
    assert result == expected


def test_invalid_method(mocker, globals, factory, minimal):
    macro = get_instance(mocker, globals, factory, minimal)
    result = macro.resolve('<usdm:macro id="xxx" name="inclusion"/>')
    expected = "Missing content: invalid method name"
    assert result == expected


def test_invalid_exception(mocker, globals, factory, minimal):
    macro = get_instance(mocker, globals, factory, minimal)
    result = macro.resolve('<usdm:macro name="inclusion"/>')
    expected = "Missing content: exception"
    assert result == expected


def test_bc_ok_name(mocker, globals, factory, minimal):
    macro = get_instance(mocker, globals, factory, minimal)
    create_bc(factory, globals)
    result = macro.resolve('<usdm:macro id="bc" name="height" activity="vitals"/>')
    expected = '<usdm:ref attribute="label" id="BiomedicalConcept_1" klass="BiomedicalConcept"></usdm:ref>'
    assert result == expected


def test_bc_ok_synonym_1(mocker, globals, factory, minimal):
    macro = get_instance(mocker, globals, factory, minimal)
    create_bc(factory, globals)
    result = macro.resolve('<usdm:macro id="bc" name="body HEIGHT" activity="vitals"/>')
    expected = '<usdm:ref attribute="label" id="BiomedicalConcept_1" klass="BiomedicalConcept"></usdm:ref>'
    assert result == expected


def test_bc_ok_synonym_2(mocker, globals, factory, minimal):
    macro = get_instance(mocker, globals, factory, minimal)
    create_bc(factory, globals)
    result = macro.resolve(
        '<usdm:macro id="bc" name=" standing height " activity="vitals"/>'
    )
    expected = '<usdm:ref attribute="label" id="BiomedicalConcept_1" klass="BiomedicalConcept"></usdm:ref>'
    assert result == expected


def test_bc_error(mocker, globals, factory, minimal):
    macro = get_instance(mocker, globals, factory, minimal)
    create_bc(factory, globals)
    result = macro.resolve('<usdm:macro id="bc" name="heightX" activity="vitals"/>')
    expected = "Missing BC: failed to find BC in activity"
    assert result == expected


def test_activity_error(mocker, globals, factory, minimal):
    macro = get_instance(mocker, globals, factory, minimal)
    create_bc(factory, globals)
    result = macro.resolve('<usdm:macro id="bc" name="height" activity="vitalsX"/>')
    expected = "Missing activity: failed to find activity 'vitalsX'"
    assert result == expected


def test_image_ok(mocker, globals, factory, minimal):
    mock_image = mocker.patch("usdm_excel.document.macros.Macros._encode_image")
    mock_image.side_effect = [base64.b64encode(str.encode("01234567890ABCDEF"))]
    macro = get_instance(mocker, globals, factory, minimal)
    result = macro.resolve('<usdm:macro id="image" file="xxx.png" type="png"/>')
    expected = (
        '<img alt="Alt text" src="data:image/png;base64,MDEyMzQ1Njc4OTBBQkNERUY="/>'
    )
    assert result == expected


def test_image_error(mocker, globals, factory, minimal):
    macro = get_instance(mocker, globals, factory, minimal)
    result = macro.resolve('<usdm:macro id="image" file="xxx.png" type="png"/>')
    expected = "Missing image: failed to insert image 'xxx.png'"
    assert result == expected


def test_abbreviation_ok(mocker, globals, factory, minimal):
    macro = get_instance(mocker, globals, factory, minimal)
    create_abbreviations(factory, globals)
    result = macro.resolve('<usdm:macro id="abbreviations" items="XXX"/>')
    expected = '<usdm:ref attribute="abbreviatedText" id="Abbreviation_1" klass="Abbreviation"></usdm:ref> = <usdm:ref attribute="expandedText" id="Abbreviation_1" klass="Abbreviation"></usdm:ref>'
    assert result == expected


def test_abbreviation_separator(mocker, globals, factory, minimal):
    macro = get_instance(mocker, globals, factory, minimal)
    create_abbreviations(factory, globals)
    result = macro.resolve(
        '<usdm:macro id="abbreviations" items="XXX, ECG" separator=";"/>'
    )
    expected = '<usdm:ref attribute="abbreviatedText" id="Abbreviation_1" klass="Abbreviation"></usdm:ref> = <usdm:ref attribute="expandedText" id="Abbreviation_1" klass="Abbreviation"></usdm:ref>; <usdm:ref attribute="abbreviatedText" id="Abbreviation_2" klass="Abbreviation"></usdm:ref> = <usdm:ref attribute="expandedText" id="Abbreviation_2" klass="Abbreviation"></usdm:ref>'
    assert result == expected


def test_abbreviation_multiple_ok(mocker, globals, factory, minimal):
    macro = get_instance(mocker, globals, factory, minimal)
    create_abbreviations(factory, globals)
    result = macro.resolve('<usdm:macro id="abbreviations" items="XXX,  ECG,AD"/>')
    expected = '<usdm:ref attribute="abbreviatedText" id="Abbreviation_1" klass="Abbreviation"></usdm:ref> = <usdm:ref attribute="expandedText" id="Abbreviation_1" klass="Abbreviation"></usdm:ref>, <usdm:ref attribute="abbreviatedText" id="Abbreviation_2" klass="Abbreviation"></usdm:ref> = <usdm:ref attribute="expandedText" id="Abbreviation_2" klass="Abbreviation"></usdm:ref>, <usdm:ref attribute="abbreviatedText" id="Abbreviation_3" klass="Abbreviation"></usdm:ref> = <usdm:ref attribute="expandedText" id="Abbreviation_3" klass="Abbreviation"></usdm:ref>'
    assert result == expected


def test_abbreviation_error(mocker, globals, factory, minimal):
    macro = get_instance(mocker, globals, factory, minimal)
    result = macro.resolve('<usdm:macro id="abbreviations" items="AE"/>')
    expected = "Missing abbreviation: failed to find abbreviation 'AE'"
    assert result == expected
