from usdm_excel.base_sheet import BaseSheet
from usdm_model.comment_annotation import CommentAnnotation
from usdm_excel.globals import Globals


class AnnotationSheet(BaseSheet):
    SHEET_NAME = "notes"

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
                    text = self.read_cell_by_name(index, "text")
                    codes = self.read_other_code_cell_multiple_by_name(index, "codes")
                    params = {"text": text, "codes": codes}
                    item = self.create_object(CommentAnnotation, params)
                    if item:
                        self.items.append(item)
                        self.globals.cross_references.add(name, item)
        except Exception as e:
            self._sheet_exception(e)
