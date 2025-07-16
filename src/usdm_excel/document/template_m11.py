import re
from yattag import Doc
from .template_base import TemplateBase
from usdm_excel.base_sheet import BaseSheet
from usdm_model.study import Study


class TemplateM11(TemplateBase):
    # def __init__(self, parent: BaseSheet, study: Study):
    #   super().__init__(parent, study)

    def title_page(self, attributes):
        doc = Doc()
        with doc.tag("table"):
            self._title_page_entry(doc, "Sponsor Confidentiality Statement:", "")
            self._title_page_entry(
                doc, "Full Title:", f"{self._elements.study_full_title()}"
            )
            self._title_page_entry(
                doc, "Trial Acronym:", f"{self._elements.study_acronym()}"
            )
            self._title_page_entry(
                doc, "Protocol Identifier:", f"{self._elements.study_identifier()}"
            )
            self._title_page_entry(doc, "Original Protocol:", "")
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
            self._title_page_entry(doc, "Compound Codes(s):", "")
            self._title_page_entry(doc, "Compound Name(s):", "")
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
                doc,
                "Sponsor Approval Date:",
                f"{self._elements.document_approval_date()}",
            )

            # Enter Nonproprietary Name(s)
            # Enter Proprietary Name(s)
            # Globally/Locally/Cohort
            # Primary Reason for Amendment
            # Region Identifier
            # Secondary Reason for Amendment

        result = doc.getvalue()
        # print(f"DOC: {result}")
        return result

    def inclusion(self, attributes):
        return self._criteria("C25532")

    def exclusion(self, attributes):
        return self._criteria("C25370")

    def objective_endpoints(self, attributes):
        # print(f"M11 TP:")
        doc = Doc()
        with doc.tag("table"):
            for item in self._objective_endpoints_list():
                self._objective_endpoints_entry(
                    doc, item["objective"], item["endpoints"]
                )
        return doc.getvalue()

    def _criteria(self, type):
        # print(f"M11 TP:")
        heading = {
            "C25532": "Patients may be included in the study only if they meet <strong>all</strong> the following criteria:",
            "C25370": "Patients may be excluded in the study for <strong>any</strong> of the following reasons:",
        }
        doc = Doc()
        with doc.tag("p"):
            doc.asis(heading[type])
        with doc.tag("table"):
            for criterion in self._criteria_list(type):
                self._critieria_entry(doc, criterion["identifier"], criterion["text"])
        return doc.getvalue()

    def _critieria_entry(self, doc, number, entry):
        with doc.tag("tr"):
            with doc.tag("td", style="vertical-align: top; text-align: left"):
                with doc.tag("p"):
                    doc.asis(number)
            with doc.tag("td", style="vertical-align: top; text-align: left"):
                with doc.tag("p"):
                    doc.asis(entry)

    def _objective_endpoints_entry(self, doc, objective, endpoints):
        with doc.tag("tr"):
            with doc.tag("td", style="vertical-align: top; text-align: left"):
                with doc.tag("p"):
                    doc.asis(objective)
            with doc.tag("td", style="vertical-align: top; text-align: left"):
                for endpoint in endpoints:
                    with doc.tag("p"):
                        doc.asis(endpoint)

    def _title_page_entry(self, doc, title, entry):
        with doc.tag("tr"):
            with doc.tag("th", style="vertical-align: top; text-align: left"):
                with doc.tag("p"):
                    doc.asis(title)
            with doc.tag("td", style="vertical-align: top; text-align: left"):
                with doc.tag("p"):
                    doc.asis(entry)

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
