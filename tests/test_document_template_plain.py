from src.usdm_excel.globals import Globals as GlobalsClass
from tests.test_factory import Factory as FactoryClass
from tests.test_data_factory import MinimalStudy
from usdm_model.eligibility_criterion import (
    EligibilityCriterion,
    EligibilityCriterionItem,
)
from usdm_excel.document.template_plain import TemplatePlain


def create_criteria(factory: FactoryClass, minimal: MinimalStudy):
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


def test_create(
    mocker, globals: GlobalsClass, minimal: MinimalStudy, factory: FactoryClass
):
    globals.id_manager.clear()
    criteria = create_criteria(factory, minimal)
    bs = factory.base_sheet(mocker)
    template = TemplatePlain(
        bs, minimal.study_version, minimal.study_definition_document_version
    )
    result = template.inclusion({})
    expected = (
        '<table class="table"><tr><td>01</td><td><usdm:ref klass="EligibilityCriterionItem" '
        'id="EligibilityCriterionItem_1" attribute="text"></usdm:ref></td></tr><tr><td>02</td><td>'
        '<usdm:ref klass="EligibilityCriterionItem" id="EligibilityCriterionItem_2" attribute="text"></usdm:ref>'
        "</td></tr></table>"
    )
    assert result == expected
