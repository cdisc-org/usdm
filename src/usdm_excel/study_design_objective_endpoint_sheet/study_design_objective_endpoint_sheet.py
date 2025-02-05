from usdm_excel.globals import Globals
from usdm_excel.syntax_template_sheet import SyntaxTemplateSheet
from usdm_model.objective import Objective
from usdm_model.endpoint import Endpoint
from usdm_model.syntax_template_dictionary import SyntaxTemplateDictionary
from usdm_excel.globals import Globals


class StudyDesignObjectiveEndpointSheet(SyntaxTemplateSheet):
    SHEET_NAME = "studyDesignOE"

    def __init__(self, file_path: str, globals: Globals):
        try:
            self.objectives = []
            super().__init__(
                file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME
            )
            current = None
            for index, row in self.sheet.iterrows():
                o_text = self.read_cell_by_name(index, "objectiveText")
                ep_name = self.read_cell_by_name(
                    index, ["endpointXref", "endpointName"]
                )
                ep_description = self.read_cell_by_name(index, "endpointDescription")
                ep_label = self.read_cell_by_name(
                    index, ["endpointLabel"], must_be_present=False
                )
                ep_text = self.read_cell_by_name(index, "endpointText")
                ep_purpose = self.read_cell_by_name(
                    index,
                    ["endpointPurposeDescription", "endpointPurpose"],
                    default="None provided",
                )
                ep_level = self.read_cdisc_klass_attribute_cell_by_name(
                    "Endpoint", "endpointLevel", index, "endpointLevel"
                )
                ep_dictionary_name = self.read_cell_by_name(
                    index, "endpointDictionary", must_be_present=False
                )
                self._validate_references(
                    index, "endpointText", ep_text, ep_dictionary_name
                )

                if o_text:
                    o_name = self.read_cell_by_name(
                        index, ["objectiveXref", "objectiveName"]
                    )
                    o_description = self.read_cell_by_name(
                        index, "objectiveDescription"
                    )
                    o_label = self.read_cell_by_name(
                        index, ["objectiveLabel"], must_be_present=False
                    )
                    o_level = self.read_cdisc_klass_attribute_cell_by_name(
                        "Objective", "objectiveLevel", index, "objectiveLevel"
                    )
                    o_dictionary_name = self.read_cell_by_name(
                        index, "objectiveDictionary", must_be_present=False
                    )
                    self._validate_references(
                        index, "objectiveText", o_text, o_dictionary_name
                    )
                    try:
                        dictionary_id = self._get_dictionary_id(o_dictionary_name)
                        current = Objective(
                            id=self.globals.id_manager.build_id(Objective),
                            name=o_name,
                            description=o_description,
                            label=o_label,
                            text=o_text,
                            level=o_level,
                            endpoints=[],
                            dictionaryId=dictionary_id,
                        )
                    except Exception as e:
                        self._general_exception(f"Failed to create Objective object", e)
                    else:
                        self.objectives.append(current)
                        self.globals.cross_references.add(o_name, current)
                if current is not None:
                    try:
                        dictionary_id = self._get_dictionary_id(ep_dictionary_name)
                        ep = Endpoint(
                            id=self.globals.id_manager.build_id(Endpoint),
                            name=ep_name,
                            description=ep_description,
                            label=ep_label,
                            text=ep_text,
                            purpose=ep_purpose,
                            level=ep_level,
                            dictionaryId=dictionary_id,
                        )
                    except Exception as e:
                        self._general_exception(f"Failed to create Endpoint object", e)
                    else:
                        current.endpoints.append(ep)
                        self.globals.cross_references.add(ep_name, ep)
                else:
                    self._general_error("Failed to add Endpoint, no Objective set")

        except Exception as e:
            self._sheet_exception(e)
