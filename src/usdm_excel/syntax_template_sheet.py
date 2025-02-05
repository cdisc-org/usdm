import re
from usdm_excel.globals import Globals
from usdm_excel.base_sheet import BaseSheet
from usdm_model.syntax_template_dictionary import SyntaxTemplateDictionary


class SyntaxTemplateSheet(BaseSheet):
    def __init__(
        self, file_path: str, globals: Globals, sheet_name: str, optional: bool = True
    ):
        try:
            super().__init__(
                file_path=file_path,
                globals=globals,
                sheet_name=sheet_name,
                optional=optional,
            )
        except Exception as e:
            self._sheet_exception(e)

    def _validate_references(
        self, row: int, column_name: str, text: str, dictionary_name: str
    ) -> None:
        if dictionary_name:
            column = self.column_present(column_name)
            dictionary = self.globals.cross_references.get(
                SyntaxTemplateDictionary, dictionary_name
            )
            if not dictionary:
                self._warning(row, column, f"Dictionary '{dictionary_name}' not found")
                return
            tags = re.findall(r"\[([^]]*)\]", text)
            for tag in tags:
                entry = next(
                    (item for item in dictionary.parameterMaps if item.tag == tag), None
                )
                if not entry:
                    # if not tag in dictionary.parameterMap:
                    self._warning(
                        row,
                        column,
                        f"Failed to find '{tag}' in dictionary '{dictionary_name}'",
                    )

    def _get_dictionary_id(self, dictionary_name: str) -> str:
        if dictionary_name:
            dictionary = self.globals.cross_references.get(
                SyntaxTemplateDictionary, dictionary_name
            )
            if dictionary:
                return dictionary.id
            else:
                self._general_error(
                    f"Unable to find dictionary with name '{dictionary_name}'"
                )
        return None
