import traceback
from usdm_excel.base_sheet import BaseSheet
from usdm_model.syntax_template_dictionary import SyntaxTemplateDictionary, ParameterMap
from usdm_excel.globals import Globals


class StudyDesignDictionarySheet(BaseSheet):
    SHEET_NAME = "dictionaries"

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
                current_name = None
                current_dictionary = None
                current_map = []
                for index, row in self.sheet.iterrows():
                    name = self.read_cell_by_name(index, "name")
                    if name:
                        if name != current_name:
                            current_name = name
                            if current_dictionary:
                                current_dictionary.parameterMaps = current_map
                                current_map = []
                            description = self.read_cell_by_name(index, "description")
                            label = self.read_cell_by_name(index, "label")
                            current_dictionary = self._dictionary(
                                name, description, label
                            )
                    key = self.read_cell_by_name(index, "key")
                    klass = self.read_cell_by_name(index, "class", default="")
                    xref_name = self.read_cell_by_name(index, "xref", default="")
                    attribute_path = self.read_cell_by_name(
                        index, ["attribute", "path"], default=""
                    )
                    value = self.read_cell_by_name(
                        index, "value", default="", must_be_present=False
                    )
                    if klass:
                        try:
                            instance, attribute = (
                                self.globals.cross_references.get_by_path(
                                    klass, xref_name, attribute_path
                                )
                            )
                        except Exception as e:
                            instance = None
                            col = self.column_present(["attribute", "path"])
                            self._error(index, col, str(e))
                        if instance:
                            map = self.create_object(
                                ParameterMap,
                                {
                                    "tag": key,
                                    "reference": f'<usdm:ref klass="{instance.__class__.__name__}" id="{instance.id}" attribute="{attribute}"></usdm:ref>',
                                },
                            )
                            if map:
                                current_map.append(map)
                    else:
                        map = self.create_object(
                            ParameterMap, {"tag": key, "reference": f"{value}"}
                        )
                        if map:
                            current_map.append(map)
                # Clean up last dictionary if present
                if current_dictionary:
                    current_dictionary.parameterMaps = current_map

        except Exception as e:
            self._sheet_exception(e)

    def _dictionary(self, name, description, label):
        try:
            item = SyntaxTemplateDictionary(
                id=self.globals.id_manager.build_id(SyntaxTemplateDictionary),
                name=name,
                description=description,
                label=label,
                parameterMaps=[],
            )
        except Exception as e:
            self._general_exception(
                f"Failed to create SyntaxTemplateDictionary object", e
            )
            return None
        else:
            self.items.append(item)
            self.globals.cross_references.add(name, item)
            return item
