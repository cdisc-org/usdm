from usdm_excel.base_sheet import BaseSheet
from usdm_model.study_amendment import StudyAmendment
from usdm_model.study_amendment_reason import StudyAmendmentReason
from usdm_model.subject_enrollment import SubjectEnrollment
from usdm_model.study_definition_document import StudyDefinitionDocument
from usdm_model.governance_date import GovernanceDate
from usdm_excel.cdisc_ct import CDISCCT
from usdm_excel.globals import Globals


class StudyAmendmentSheet(BaseSheet):
    SHEET_NAME = "studyAmendments"

    def __init__(self, file_path: str, globals: Globals):
        try:
            self.items = []
            self.template_names = []
            super().__init__(
                file_path=file_path,
                globals=globals,
                sheet_name=self.SHEET_NAME,
                optional=True,
            )
            if self.success:
                for index, row in self.sheet.iterrows():
                    secondaries = []
                    name = self.read_cell_by_name(index, ["name"])
                    description = self.read_cell_by_name(
                        index, ["description"], default="", must_be_present=False
                    )
                    label = self.read_cell_by_name(
                        index, "label", default="", must_be_present=False
                    )
                    number = self.read_cell_by_name(index, "number")
                    date_name = self.read_cell_by_name(
                        index, "date", must_be_present=False
                    )
                    date = self.globals.cross_references.get(GovernanceDate, date_name)
                    summary = self.read_cell_by_name(index, "summary")
                    template = self.read_cell_by_name(
                        index, "template", must_be_present=False
                    )
                    notes = self.read_cell_multiple_by_name(
                        index, "notes", must_be_present=False
                    )
                    primary_reason = self._read_primary_reason_cell(index)
                    primary = self._amendment_reason(primary_reason)
                    secondary_reasons = self._read_secondary_reason_cell(index)
                    for reason in secondary_reasons:
                        amendment_reason = self._amendment_reason(reason)
                        if amendment_reason:
                            secondaries.append(amendment_reason)
                    enrollments = self._read_enrollment_cell(index)
                    scopes = self.read_geographic_scopes_cell_by_name(
                        index, "geographicScope"
                    )
                    params = {
                        "name": name,
                        "description": description,
                        "label": label,
                        "number": number,
                        "summary": summary,
                        "primaryReason": primary,
                        "secondaryReasons": secondaries,
                        "enrollments": enrollments,
                        "geographicScopes": scopes,
                        "dateValues": [date] if date else [],
                    }
                    item = self.create_object(StudyAmendment, params)
                    if item:
                        template = (
                            template
                            if template
                            else self.globals.template_manager.default_template
                        )
                        self.items.append(item)
                        self.template_names.append(template)
                        self.globals.cross_references.add(item.number, item)
                        self.add_notes(item, notes)
                self.items.sort(key=lambda d: int(d.number))
                self.previous_link(self.items, "previousId")

        except Exception as e:
            self._sheet_exception(e)

    def set_document(self, document: StudyDefinitionDocument):
        try:
            for index, amendment in enumerate(self.items):
                self._general_info(
                    f"Checking document template '{document.templateName}' versus '{self.template_names}' "
                )
                if self.template_names[index].upper() == document.templateName.upper():
                    for change in amendment.changes:
                        for ref in change.changedSections:
                            ref.appliesToId = document.id
        except Exception as e:
            self._sheet_exception(e)

    def _amendment_reason(self, reason):
        item = self.create_object(
            StudyAmendmentReason,
            {"code": reason["code"], "otherReason": reason["other"]},
        )
        return item

    def _read_enrollment_cell(self, row_index):
        result = []
        col_index = self._get_column_index("enrollment")
        value = self.read_cell(row_index, col_index)
        if value.strip() == "":
            self._error(
                row_index,
                col_index,
                "Empty cell detected where enrollment values expected",
            )
        else:
            for item in self._state_split(value):
                key_value = self._key_value(item, row_index, col_index)
                if key_value[0] == "COHORT":
                    pass
                elif key_value[0] == "SITE":
                    pass
                elif key_value[0] == "GLOBAL":
                    quantity = self._get_quantity(key_value[1])
                    scope = self._scope("Global", None)
                    result.append(self._enrollment(quantity, scope=scope))
                elif key_value[0] == "REGION":
                    code, quantity = self._country_region_quantity(
                        key_value[1], "Region", row_index, col_index
                    )
                    if code:
                        scope = self._scope("Region", code)
                        result.append(self._enrollment(quantity, scope=scope))
                elif key_value[0] == "COUNTRY":
                    code, quantity = self._country_region_quantity(
                        key_value[1], "Country", row_index, col_index
                    )
                    if code:
                        scope = self._scope("Country", code)
                        result.append(self._enrollment(quantity, scope=scope))
        return result

    def _enrollment(self, quantity, **kwargs):
        for_geographic_scope = None
        for_study_cohort_id = None
        for_study_site_id = None
        if "scope" in kwargs:
            for_geographic_scope = kwargs["scope"]
        if "cohort" in kwargs:
            for_study_cohort_id = kwargs["cohort"]
        if "site" in kwargs:
            for_study_site_id = kwargs["site"]
        return self.create_object(
            SubjectEnrollment,
            {
                "name": "XXX",
                "quantity": quantity,
                "forGeographicScope": for_geographic_scope,
                "forStudyCohortId": for_study_cohort_id,
                "forStudySiteId": for_study_site_id,
            },
        )

    def _read_secondary_reason_cell(self, row_index):
        results = []
        col_index = self._get_column_index("secondaryReasons")
        value = self.read_cell(row_index, col_index)
        if not value.strip():
            return results
        parts = value.strip().split(",")
        for part in parts:
            result = self._extract_reason(part, row_index, col_index)
            if result:
                results.append(result)
        return results

    def _read_primary_reason_cell(self, row_index):
        col_index = self._get_column_index("primaryReason")
        value = self.read_cell(row_index, col_index)
        return self._extract_reason(value, row_index, col_index)

    def _extract_reason(self, value, row_index, col_index):
        if value.strip() == "":
            self._error(
                row_index,
                col_index,
                "Empty cell detected where CDISC CT value expected.",
            )
            return None
        elif value.strip().upper().startswith("OTHER"):
            text = value.strip()
            parts = text.split("=")
            if len(parts) == 2:
                return {
                    "code": CDISCCT(self.globals).code_for_attribute(
                        "StudyAmendmentReason", "code", "Other"
                    ),
                    "other": parts[1].strip(),
                }
            else:
                self._error(
                    row_index,
                    col_index,
                    f"Failed to decode reason data {text}, no '=' detected",
                )
        else:
            code = CDISCCT(self.globals).code_for_attribute(
                "StudyAmendmentReason", "code", value
            )
            if code is None:
                self._error(
                    row_index, col_index, f"CDISC CT not found for value '{value}'."
                )
            return {"code": code, "other": None}
