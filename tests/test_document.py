from yattag import Doc
from usdm_model.eligibility_criterion import (
    EligibilityCriterion,
    EligibilityCriterionItem,
)
from usdm_model.narrative_content import NarrativeContent, NarrativeContentItem
from usdm_db.document.document import Document
from tests.test_factory import Factory
from bs4 import BeautifulSoup


def create_criteria(factory, minimal):
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


def test_wrap_in_span_and_modal_1(mocker, globals, minimal, factory):
    criteria = create_criteria(factory, minimal)
    document = Document(minimal.study, "sponsor", globals.errors_and_logging)
    soup = BeautifulSoup(
        'Before<usdm:ref id="EligibilityCriterion_1" klass="EligibilityCriterion" attribute="text"/>After',
        "html.parser",
    )
    ref = soup(["usdm:ref"])[0]
    document._wrap_in_span_and_modal(soup, ref, "1234")
    assert (
        str(soup)
        == 'Before<span class="usdm-highlight">\n<a class="link-dark usdm-highlight-link" data-bs-target="#usdmContent1" data-bs-toggle="modal" style="font-size: 12px;">\n<i class="ps-1 pe-1 bi bi-info-circle"></i>\n</a>\n1234\n<div class="modal fade" id="usdmContent1" tabindex="-1">\n<div class="modal-dialog">\n<div class="modal-content">\n<div class="modal-header">\n<h5 class="modal-title">Included using \'usdm:ref\'</h5>\n<button aria-label="Close" class="btn-close" data-bs-dismiss="modal" type="button"></button>\n</div>\n<div class="modal-body">\n              Attributes: <b>\'id\':</b> \'EligibilityCriterion_1\', <b>\'klass\':</b> \'EligibilityCriterion\', <b>\'attribute\':</b> \'text\'\n            </div>\n</div>\n</div>\n</div>\n</span>After'
    )


def test_replace_and_highlight_1(mocker, globals, minimal, factory):
    criteria = create_criteria(factory, minimal)
    document = Document(minimal.study, "sponsor", globals.errors_and_logging)
    soup = BeautifulSoup(
        'Before<usdm:ref id="EligibilityCriterion_1" klass="EligibilityCriterion" attribute="text"/>After',
        "html.parser",
    )
    ref = soup(["usdm:ref"])[0]
    result = document._replace_and_highlight(soup, ref, " ccc ", False)
    assert str(soup) == "Before ccc After"


def test_replace_and_highlight_2(mocker, globals, minimal, factory):
    criteria = create_criteria(factory, minimal)
    document = Document(minimal.study, "sponsor", globals.errors_and_logging)
    soup = BeautifulSoup(
        'Before<usdm:ref id="EligibilityCriterion_1" klass="EligibilityCriterion" attribute="text"/>After',
        "html.parser",
    )
    ref = soup(["usdm:ref"])[0]
    result = document._replace_and_highlight(soup, ref, " TEXT HERE ", True)
    assert (
        str(soup)
        == 'Before<span class="usdm-highlight">\n<a class="link-dark usdm-highlight-link" data-bs-target="#usdmContent1" data-bs-toggle="modal" style="font-size: 12px;">\n<i class="ps-1 pe-1 bi bi-info-circle"></i>\n</a>\n TEXT HERE \n<div class="modal fade" id="usdmContent1" tabindex="-1">\n<div class="modal-dialog">\n<div class="modal-content">\n<div class="modal-header">\n<h5 class="modal-title">Included using \'usdm:ref\'</h5>\n<button aria-label="Close" class="btn-close" data-bs-dismiss="modal" type="button"></button>\n</div>\n<div class="modal-body">\n              Attributes: <b>\'id\':</b> \'EligibilityCriterion_1\', <b>\'klass\':</b> \'EligibilityCriterion\', <b>\'attribute\':</b> \'text\'\n            </div>\n</div>\n</div>\n</div>\n</span>After'
    )


def test_translate_rererences_1(mocker, globals, minimal, factory):
    criteria = create_criteria(factory, minimal)
    document = Document(minimal.study, "sponsor", globals.errors_and_logging)
    result = document._translate_references(
        '<usdm:macro id="section" name="inclusion"/>', False
    )
    assert str(result) == '<usdm:macro id="section" name="inclusion"></usdm:macro>'


def test_translate_rererences_2(mocker, globals, minimal, factory):
    criteria = create_criteria(factory, minimal)
    document = Document(minimal.study, "sponsor", globals.errors_and_logging)
    result = document._translate_references(
        '<usdm:ref id="EligibilityCriterionItem_1" klass="EligibilityCriterionItem" attribute="text"/>',
        False,
    )
    assert str(result) == "Only perform at baseline"


def test_content_to_html_1(mocker, globals, minimal, factory):
    criteria = create_criteria(factory, minimal)
    item = factory.item(
        NarrativeContentItem,
        {
            "name": "NCI1",
            "text": '<usdm:macro id="section" name="inclusion"/>',
            "childIds": [],
        },
    )
    content = factory.item(
        NarrativeContent,
        {
            "name": "NC1",
            "sectionNumber": "1.1.1",
            "displaySectionNumber": True,
            "sectionTitle": "Section Title",
            "displaySectionTitle": True,
            "contentItemId": item.id,
            "childIds": [],
        },
    )
    minimal.study.versions[0].narrativeContentItems = [item]
    minimal.study.documentedBy[0].versions[0].contents = [content]
    doc = Doc()
    document = Document(minimal.study, "sponsor", globals.errors_and_logging)
    document._content_to_html(content, doc)
    result = doc.getvalue()
    expected = '<div class=""><h3 id="section-1.1.1">1.1.1 Section Title</h3><usdm:macro id="section" name="inclusion"></usdm:macro></div>'
    assert result == expected
