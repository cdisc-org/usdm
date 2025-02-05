from usdm_excel.globals import Globals
from usdm_excel.syntax_template_sheet import SyntaxTemplateSheet
from usdm_model.characteristic import Characteristic


class StudyDesignCharacteristicSheet(SyntaxTemplateSheet):
    SHEET_NAME = "studyDesignCharacteristics"

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
                    dictionary_name = self.read_cell_by_name(index, "dictionary")
                    self._validate_references(index, "text", text, dictionary_name)
                    item = self._characteristic(
                        name, description, label, text, dictionary_name
                    )
                    if item:
                        self.globals.cross_references.add(item.name, item)
                        self.items.append(item)
        except Exception as e:
            self._sheet_exception(e)

    def _characteristic(
        self, name: str, description: str, label: str, text: str, dictionary_name: str
    ) -> Characteristic:
        dictionary_id = self._get_dictionary_id(dictionary_name)
        params = {
            "name": name,
            "description": description,
            "label": label,
            "text": text,
            "dictionaryId": dictionary_id,
        }
        return self.create_object(Characteristic, params)
