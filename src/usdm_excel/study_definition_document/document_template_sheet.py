from usdm_excel.base_sheet import BaseSheet
from usdm_model.narrative_content import NarrativeContent, NarrativeContentItem
from usdm_excel.globals import Globals


class DocumentTemplates:
    def __init__(self, file_path: str, globals: Globals):
        self.items = []
        for template, sheet in globals.template_manager.items():
            document = DocumentTemplateSheet(file_path, template, sheet, globals)
            self.items.append(document)


class DocumentTemplateSheet(BaseSheet):
    def __init__(
        self, file_path: str, template_name: str, sheet_name: str, globals: Globals
    ):
        try:
            self.items = []
            self.name = template_name
            super().__init__(
                file_path=file_path,
                globals=globals,
                sheet_name=sheet_name,
                optional=True,
                converters={"sectionName": str},
            )
            if self.success:
                current_level = 0
                new_level = 0
                self._parent_stack = []
                previous_item = None
                for index, row in self.sheet.iterrows():
                    name = self.read_cell_by_name(index, "name")
                    section_number = self.read_cell_by_name(index, "sectionNumber")
                    name = f"SECTION {section_number}" if not name else name
                    new_level = self._get_level(section_number)
                    section_title = self.read_cell_by_name(index, "sectionTitle")
                    display_section_number = self.read_boolean_cell_by_name(
                        index, "displaySectionNumber"
                    )
                    display_section_title = self.read_boolean_cell_by_name(
                        index, "displaySectionTitle"
                    )
                    content_name = self.read_cell_by_name(index, "content")
                    # print(f"TEMPLATE: '{content_name}'")
                    if content_name:
                        content = self.globals.cross_references.get(
                            NarrativeContentItem, content_name
                        )
                        if not content:
                            self._general_warning(
                                f"Unable to find content item with name '{content_name}'"
                            )
                    else:
                        self._general_warning(
                            f"No content item specified for section '{section_number}', '{section_title}'"
                        )
                        content = None
                    params = {
                        "name": name,
                        "sectionNumber": section_number,
                        "displaySectionNumber": display_section_number,
                        "sectionTitle": section_title,
                        "displaySectionTitle": display_section_title,
                        "contentItemId": content.id if content else None,
                    }
                    item = self.create_object(NarrativeContent, params)
                    if item:
                        self.items.append(item)
                        self.globals.cross_references.add(name, item)
                        if new_level == current_level:
                            # Same level
                            self._add_child_to_parent(item)
                        elif new_level > current_level:
                            # Down
                            if (new_level - current_level) > 1:
                                self._error(
                                    index,
                                    self._get_column_index("sectionNumber"),
                                    f"Error with section number incresing by more than one level, section '{section_number}'.",
                                )
                                raise BaseSheet.FormatError
                            if previous_item:
                                self._push_parent(previous_item)
                            self._add_child_to_parent(item)
                            current_level = new_level
                        else:
                            # Up
                            self._pop_parent(current_level, new_level)
                            self._add_child_to_parent(item)
                            current_level = new_level
                        previous_item = item
                    self.double_link(self.items, "previousId", "nextId")
        except Exception as e:
            self._sheet_exception(e)

    def _get_level(self, section_number):
        sn = section_number[:-1] if section_number.endswith(".") else section_number
        parts = sn.split(".")
        return len(parts)

    def _push_parent(self, parent):
        self._parent_stack.append(parent)

    def _pop_parent(self, current_level, new_level):
        for p_count in range(new_level, current_level):
            popped = self._parent_stack.pop()

    def _add_child_to_parent(self, child):
        if self._parent_stack:
            parent = self._parent_stack[-1]
            parent.childIds.append(child.id)
