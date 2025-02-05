import traceback
import pandas as pd
from usdm_excel.base_sheet import BaseSheet
from usdm_model.procedure import Procedure
from usdm_excel.globals import Globals


class StudyDesignProcedureSheet(BaseSheet):
    SHEET_NAME = "studyDesignProcedures"

    def __init__(self, file_path: str, globals: Globals):
        try:
            self.procedures = []
            super().__init__(
                file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME
            )
            for index, row in self.sheet.iterrows():
                xref = self.read_cell_by_name(
                    index, "xref", default="", must_be_present=False
                )
                name = self.read_cell_by_name(index, ["procedureName", "name"])
                description = self.read_cell_by_name(
                    index, ["procedureDescription", "description"]
                )
                label = self.read_cell_by_name(
                    index, "label", default="", must_be_present=False
                )
                type = self.read_cell_by_name(index, "procedureType")
                code = self.read_other_code_cell_by_name(
                    index, ["procedureCode", "code"]
                )
                try:
                    item = Procedure(
                        id=self.globals.id_manager.build_id(Procedure),
                        name=name,
                        description=description,
                        label=label,
                        procedureType=type,
                        code=code,
                    )
                except Exception as e:
                    self._general_exception(f"Failed to create Procedure object", e)
                else:
                    self.procedures.append(item)
                    cross_ref = xref if xref else name
                    self.globals.cross_references.add(cross_ref, item)
        except Exception as e:
            self._sheet_exception(e)
