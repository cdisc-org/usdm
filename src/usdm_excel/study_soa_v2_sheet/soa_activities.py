from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_soa_v2_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.study_soa_v2_sheet.soa_activity import SoAActivity


class SoAActivities:
    def __init__(self, parent: BaseSheet):
        self._parent_sheet = parent
        self.items = []
        self._map = {}
        self._parent_activity = None
        for row_index, col_def in self._parent_sheet.sheet.iterrows():
            if row_index >= SoAColumnRows.FIRST_ACTIVITY_ROW:
                activity = SoAActivity(self._parent_sheet, row_index, self._map)
                the_activity = activity.activity
                if the_activity:
                    self.items.append(activity)

    def group_and_link(self):
        activities = []
        biomedical_concepts = []
        biomedical_concept_surrogates = []
        for item in self.items:
            the_activity = item.activity
            activities.append(the_activity)
            biomedical_concept_surrogates += item.usdm_biomedical_concept_surrogates
            biomedical_concepts += item.usdm_biomedical_concepts
        self._parent_sheet.double_link(activities, "previousId", "nextId")
        return activities, biomedical_concepts, biomedical_concept_surrogates

    def set_parents(self):
        parents = any([x.is_parent for x in self.items])
        if parents:
            parent_activity = None
            for item in self.items:
                the_activity = item.activity
                if item.is_parent:
                    parent_activity = the_activity
                elif parent_activity:
                    parent_activity.childIds.append(the_activity.id)
                else:
                    self._parent_sheet._general_error(
                        f"Child activity with name '{the_activity.name}' does not have a parent specified"
                    )
