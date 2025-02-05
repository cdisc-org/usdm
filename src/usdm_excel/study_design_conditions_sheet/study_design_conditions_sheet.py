import traceback
from usdm_excel.base_sheet import BaseSheet
from usdm_model.condition import Condition
from usdm_excel.globals import Globals


class StudyDesignConditionSheet(BaseSheet):
    SHEET_NAME = "studyDesignConditions"

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
                    name = self.read_cell_by_name(index, "name")
                    description = self.read_cell_by_name(index, "description")
                    label = self.read_cell_by_name(index, "label")
                    text = self.read_cell_by_name(index, "text")
                    context = self.read_cell_by_name(index, "context")
                    context_refs = self._process_context_references(context, index)
                    applies_to = self.read_cell_by_name(index, "appliesTo")
                    applies_refs = self._process_applies_to_references(
                        applies_to, index
                    )
                    params = {
                        "name": name,
                        "description": description,
                        "label": label,
                        "text": text,
                        "appliesToIds": applies_refs,
                        "contextIds": context_refs,
                    }
                    item = self.create_object(Condition, params)
                    if item:
                        self.items.append(item)
                        self.globals.cross_references.add(name, item)
        except Exception as e:
            self._sheet_exception(e)

    def _process_context_references(self, references_list, index):
        return self._process_references(
            references_list,
            ["ScheduledActivityInstance", "Activity"],
            index,
            "context",
            False,
        )

    def _process_applies_to_references(self, references_list, index):
        return self._process_references(
            references_list,
            [
                "Procedure",
                "Activity",
                "BiomedicalConcept",
                "BiomedicalConceotCategory",
                "BiomedicalConceptSurrogate",
            ],
            index,
            "appliesTo",
        )

    def _process_references(
        self, references_list, klasses, index, column_name, references_required=True
    ):
        references = [x.strip() for x in self._state_split(references_list)]
        # references = [x.strip() for x in references_list.split(',')]
        results = []
        for reference in references:
            if reference:
                found = False
                for klass in klasses:
                    xref = self.globals.cross_references.get(klass, reference)
                    if xref:
                        results.append(xref.id)
                        found = True
                        break
                if not found:
                    self._error(
                        index,
                        self._get_column_index(column_name),
                        f"Could not resolve condition reference '{reference}'",
                    )
        if not results and references_required:
            self._error(
                index,
                self._get_column_index(column_name),
                f"No condition references found for '{references_list}', at least one required",
            )
        return results
