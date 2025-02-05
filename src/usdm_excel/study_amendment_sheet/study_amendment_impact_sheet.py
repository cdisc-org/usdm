from usdm_excel.base_sheet import BaseSheet
from usdm_model.study_amendment import StudyAmendment
from usdm_model.study_amendment_impact import StudyAmendmentImpact
from usdm_excel.globals import Globals


class StudyAmendmentImpactSheet(BaseSheet):
    SHEET_NAME = "amendmentImpact"

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
                    text = self.read_cell_by_name(index, "text")
                    substantial = self.read_boolean_cell_by_name(index, "substantial")
                    type = self.read_cdisc_klass_attribute_cell_by_name(
                        "StudyAmendmentImpact", "type", index, "type"
                    )
                    item = self.create_object(
                        StudyAmendmentImpact,
                        {"text": text, "isSubstantial": substantial, "type": type},
                    )
                    if item:
                        self.items.append(item)
                        parent = self.globals.cross_references.get(
                            StudyAmendment, amendment
                        )
                        if parent:
                            parent.impacts.append(item)
                        else:
                            column = self._get_column_index("amendment")
                            self._error(
                                index,
                                column,
                                f"Failed to find amendment with name '{amendment}'",
                            )
        except Exception as e:
            self._sheet_exception(e)
