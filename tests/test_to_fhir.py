from usdm_model.eligibility_criterion import (
    EligibilityCriterion,
    EligibilityCriterionItem,
)
from usdm_model.narrative_content import NarrativeContent, NarrativeContentItem
from usdm_db.fhir.to_fhir import ToFHIR
from tests.test_factory import Factory
from tests.test_data_factory import MinimalStudy
from uuid import UUID

fake_uuid = UUID(f"00000000-0000-4000-8000-{1:012}", version=4)


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


def test_create(mocker, globals, minimal, factory):
    x = create_criteria(factory, minimal)
    fhir = ToFHIR(minimal.study, "Sponsor")
    assert fhir is not None


def test_content_to_section(mocker, globals, minimal, factory):
    x = create_criteria(factory, minimal)
    fhir = ToFHIR(minimal.study, "Sponsor")
    item = factory.item(
        NarrativeContentItem, {"name": "NCI1", "text": "Something here for the text"}
    )
    content = factory.item(
        NarrativeContent,
        {
            "name": "C1",
            "sectionNumber": "1.1.1",
            "displaySectionNumber": True,
            "sectionTitle": "Section Title",
            "displaySectionTitle": True,
            "contentItemId": item.id,
            "childIds": [],
        },
    )
    result = fhir._content_to_section(content, item.text)
    expected = '{"title": "Section Title", "code": {"text": "section1.1.1-section-title"}, "text": {"status": "generated", "div": "Something here for the text"}}'
    assert result.json() == expected


def test_format_section(mocker, globals, minimal, factory):
    x = create_criteria(factory, minimal)
    fhir = ToFHIR(minimal.study, "Sponsor")
    assert fhir._format_section_title("A Section Heading") == "a-section-heading"


def test_clean_section_number(mocker, globals, minimal, factory):
    x = create_criteria(factory, minimal)
    fhir = ToFHIR(minimal.study, "Sponsor")
    assert fhir._clean_section_number("1.1") == "1.1"
    assert fhir._clean_section_number("1.1.") == "1.1"


# def test_add_section_heading(mocker, globals, minimal, factory):
#   x = create_criteria(factory, minimal)
#   fhir = ToFHIR(minimal.study, 'Sponsor')
#   item = factory.item(NarrativeContentItem, {'name': "NCI1", 'text': '<div xmlns="http://www.w3.org/1999/xhtml">Something here for the text</div>'})
#   content = factory.item(NarrativeContent, {'name': "C1", 'sectionNumber': '1.1.1', 'displaySectionNumber': True, 'sectionTitle': 'Section Title', 'displaySectionTitle': True, 'contentItemId': item.id, 'childIds': []})
#   div = BeautifulSoup(item.text, 'html.parser')
#   assert fhir._add_section_heading(content, div) == '<div xmlns="http://www.w3.org/1999/xhtml"><p>1.1.1 Section Title</p>Something here for the text</div>'


def test_remove_line_feeds(mocker, globals, minimal, factory):
    x = create_criteria(factory, minimal)
    fhir = ToFHIR(minimal.study, "Sponsor")
    text = "<p>CNS imaging (CT scan or MRI of brain) compatible with AD within past 1 year.</p>\n<p>The following findings are incompatible with AD:</p>\n"
    assert (
        fhir._remove_line_feeds(text)
        == "<p>CNS imaging (CT scan or MRI of brain) compatible with AD within past 1 year.</p><p>The following findings are incompatible with AD:</p>"
    )
