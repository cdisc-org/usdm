from usdm_excel.base_sheet import BaseSheet
from usdm_model.study_amendment import StudyAmendment
from usdm_model.study_change import StudyChange
from usdm_model.document_content_reference import DocumentContentReference
from usdm_excel.globals import Globals


class StudyAmendmentChangesSheet(BaseSheet):
    SHEET_NAME = "amendmentChanges"

    def __init__(self, file_path: str, globals: Globals):
        try:
            self.items = []
            super().__init__(
                file_path=file_path,
                globals=globals,
                sheet_name=self.SHEET_NAME,
                optional=True,
            )
            if self.success:
                for index, row in self.sheet.iterrows():
                    amendment = self.read_cell_by_name(index, "amendment")
                    name = self.read_cell_by_name(index, ["name"])
                    description = self.read_cell_by_name(index, ["description"])
                    label = self.read_cell_by_name(
                        index, "label", default="", must_be_present=False
                    )
                    rationale = self.read_cell_by_name(index, "rationale")
                    summary = self.read_cell_by_name(index, "summary")
                    sections = self._section_list(index)
                    item = self.create_object(
                        StudyChange,
                        {
                            "name": name,
                            "description": description,
                            "label": label,
                            "rationale": rationale,
                            "summary": summary,
                            "changedSections": sections,
                        },
                    )
                    if item:
                        self.items.append(item)
                        parent = self.globals.cross_references.get(
                            StudyAmendment, amendment
                        )
                        if parent:
                            parent.changes.append(item)
                        else:
                            self._error(
                                index,
                                "amendment",
                                f"Failed to find amendment with name '{amendment}'",
                            )

        except Exception as e:
            self._sheet_exception(e)

    def _section_list(self, index):
        result = []
        section_list = self.read_cell_multiple_by_name(index, "sections")
        for section in section_list:
            parts = section.split(":")
            if len(parts) == 2:
                ref = self.create_object(
                    DocumentContentReference,
                    {
                        "sectionNumber": parts[0].strip(),
                        "sectionTitle": parts[1].strip(),
                        "appliesToId": "TempId",
                    },
                )
                if ref:
                    result.append(ref)
            else:
                self._error(
                    index,
                    self._get_column_index("sections"),
                    f"Could not decode section reference '{section}'.",
                )
        return result
