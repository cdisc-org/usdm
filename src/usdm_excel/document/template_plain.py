from yattag import Doc
from usdm_excel.document.template_base import TemplateBase
from usdm_excel.document.soa import SoA
from usdm_excel.base_sheet import BaseSheet
from usdm_model.schedule_timeline import ScheduleTimeline
from usdm_model.study import Study


class TemplatePlain(TemplateBase):
    # def __init__(self, parent: BaseSheet, study: Study):
    #   super().__init__(parent, study)

    def title_page(self, attributes):
        doc = Doc()
        with doc.tag("table"):
            self._title_page_entry(
                doc, "Full Title:", f"{self._elements.study_full_title()}"
            )
            self._title_page_entry(
                doc, "Trial Acronym:", f"{self._elements.study_acronym()}"
            )
            self._title_page_entry(
                doc, "Protocol Identifier:", f"{self._elements.study_identifier()}"
            )
            self._title_page_entry(
                doc, "Version Number:", f"{self._elements.study_version_identifier()}"
            )
            self._title_page_entry(
                doc, "Version Date:", f"{self._elements.study_approval_date()}"
            )
            self._title_page_entry(
                doc, "Amendment Identifier:", f"{self._elements.amendment()}"
            )
            self._title_page_entry(
                doc, "Amendment Scope:", f"{self._elements.amendment_scopes()}"
            )
            self._title_page_entry(
                doc, "Trial Phase:", f"{self._elements.study_phase()}"
            )
            self._title_page_entry(
                doc, "Short Title:", f"{self._elements.study_short_title()}"
            )
            self._title_page_entry(
                doc,
                "Sponsor Name and Address:",
                f"{self._elements.organization_name_and_address()}",
            )
            self._title_page_entry(
                doc,
                "Regulatory Agency Identifier Number(s):",
                f"{self._elements.study_regulatory_identifiers()}",
            )
            self._title_page_entry(
                doc, "Spondor Approval Date:", f"{self._elements.approval_date()}"
            )
        result = doc.getvalue()
        return result

    def inclusion(self, attributes: dict):
        return self._criteria("C25532")

    def exclusion(self, attributes: dict):
        return self._criteria("C25370")

    def objective_endpoints(self, attributes: dict):
        doc = Doc()
        with doc.tag("table", klass="table"):
            for item in self._objective_endpoints_list():
                self._objective_endpoints_entry(
                    doc, item["objective"], item["endpoints"]
                )
        return doc.getvalue()

    def soa(self, attributes: dict):
        try:
            doc = Doc()
            for timeline in self._study_design.scheduleTimelines:
                doc.asis(self.timeline({"timeline": timeline}))
        except Exception as e:
            self.parent._general_exception(f"Error raised generating SoA", e)
        return doc.getvalue()

    def timeline(self, attributes: dict):
        try:
            doc = Doc()
            timeline = None
            timeline = self._resolve_timeline(attributes)
            footnote = 1
            footnotes = []
            soa = SoA(self.parent, self._study_version, self._study_design, timeline)
            result = soa.generate()
            with doc.tag("div", klass="page soa-page table-responsive"):
                with doc.tag("p"):
                    with doc.tag("b"):
                        doc.asis(
                            f"Timeline: {timeline.label}, {timeline.entryCondition}"
                        )
                with doc.tag(
                    "table", klass="table table-bordered table-sm", style="width:100%"
                ):
                    for row in range(len(result)):
                        with doc.tag("tr"):
                            for col in range(len(result[row])):
                                if "set" in result[row][col].keys():
                                    label = "X" if result[row][col]["set"] else ""
                                else:
                                    label = result[row][col]["label"]
                                with doc.tag("td"):
                                    klass = (
                                        "soa-activity-text"
                                        if col == 0
                                        else "soa-body-text"
                                    )
                                    with doc.tag("p", klass=klass):
                                        doc.asis(label)
                                        if "condition" in result[row][col].keys():
                                            with doc.tag("sup"):
                                                footnote_str = str(footnote)
                                                doc.text(footnote_str)
                                            footnotes.append(
                                                {
                                                    "number": footnote_str,
                                                    "text": result[row][col][
                                                        "condition"
                                                    ].text,
                                                }
                                            )
                                            footnote += 1
                if footnotes:
                    with doc.tag("table", klass="table table-borderless table-sm"):
                        for item in footnotes:
                            with doc.tag("tr"):
                                with doc.tag("td"):
                                    with doc.tag("p", klass="soa-footnote-text"):
                                        with doc.tag("sup"):
                                            doc.text(item["number"])
                                with doc.tag("td"):
                                    with doc.tag("p", klass="soa-footnote-text"):
                                        doc.asis(item["text"])
        except Exception as e:
            if timeline:
                self.parent._general_exception(
                    f"Error raised generating timeline '{timeline.name}'", e
                )
                return "Error encountered creating timeline {timeline.name}"
            else:
                self.parent._general_exception(
                    f"Error raised generating timeline, name not available", e
                )
                return "Error encountered creating timeline"
        return doc.getvalue()

    def _resolve_timeline(self, attributes):
        return (
            attributes["timeline"]
            if isinstance(attributes["timeline"], ScheduleTimeline)
            else self.parent.globals.cross_references.get(
                ScheduleTimeline, attributes["timeline"]
            )
        )

    def _criteria(self, type):
        doc = Doc()
        with doc.tag("table", klass="table"):
            for criterion in self._criteria_list(type):
                self._critieria_entry(doc, criterion["identifier"], criterion["text"])
        return doc.getvalue()

    def _critieria_entry(self, doc, identifier, entry):
        with doc.tag("tr"):
            with doc.tag("td"):
                self._add_checking_for_tag(doc, "p", identifier)
            with doc.tag("td"):
                self._add_checking_for_tag(doc, "p", entry)

    def _objective_endpoints_entry(self, doc, objective, endpoints):
        with doc.tag("tr"):
            with doc.tag("td"):
                self._add_checking_for_tag(doc, "p", objective)
            with doc.tag("td"):
                for endpoint in endpoints:
                    self._add_checking_for_tag(doc, "p", endpoint)

    def _title_page_entry(self, doc, title, entry):
        with doc.tag("tr"):
            with doc.tag("th"):
                self._add_checking_for_tag(doc, "p", title)
            with doc.tag("td"):
                self._add_checking_for_tag(doc, "p", entry)

    def _criteria_list(self, type):
        results = []
        criteria = {x.id: x for x in self._study_design.eligibilityCriteria}
        items = [
            criteria[c]
            for c in self._study_design.population.criterionIds
            if criteria[c].category.code == type
        ]
        items.sort(key=lambda d: d.identifier)
        for item in items:
            criterion_item = self._critierion_item(item.criterionItemId)
            if criterion_item:
                result = {
                    "identifier": item.identifier,
                    "text": self._reference(criterion_item, "text"),
                }
                results.append(result)
            else:
                self.parent._general_warning(
                    f"Could not resolve criterion item for criterion '{item.name}'"
                )
        return results

    def _objective_endpoints_list(self):
        results = []
        for item in self._study_design.objectives:
            result = {"objective": self._reference(item, "text"), "endpoints": []}
            for endpoint in item.endpoints:
                result["endpoints"].append(self._reference(endpoint, "text"))
            results.append(result)
        return results
