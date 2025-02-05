from usdm_excel.base_sheet import BaseSheet

# from usdm_excel.cross_ref import cross_references
# from usdm_excel.id_manager import id_manager
from usdm_model.intercurrent_event import IntercurrentEvent
from usdm_model.analysis_population import AnalysisPopulation
from usdm_model.estimand import Estimand
from usdm_model.study_intervention import StudyIntervention
from usdm_model.endpoint import Endpoint
from usdm_model.population_definition import StudyDesignPopulation, StudyCohort
from usdm_excel.globals import Globals


class StudyDesignEstimandsSheet(BaseSheet):
    SHEET_NAME = "studyDesignEstimands"

    def __init__(self, file_path: str, globals: Globals):
        try:
            self.estimands = []
            self.populations = []
            super().__init__(
                file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME
            )
            current = None
            current_ice_name = None
            current_ice_description = None
            for index, row in self.sheet.iterrows():
                e_name = self.read_cell_by_name(index, ["name", "xref"])
                e_summary = self.read_cell_by_name(index, "summaryMeasure")
                ap_description = self.read_cell_by_name(index, "populationDescription")
                ap_subset = self.read_cell_by_name(index, "populationSubset")
                ice_name = self.read_cell_by_name(index, ["intercurrentEventName"])
                ice_description = self.read_cell_by_name(
                    index, ["intercurrentEventDescription", "description"]
                )
                ice_label = self.read_cell_by_name(
                    index, "label", must_be_present=False
                )
                ice_strategy = self.read_cell_by_name(
                    index, "intercurrentEventStrategy"
                )
                ice_text = self.read_cell_by_name(index, "intercurrentEventText")
                treatment_xref = self.read_cell_by_name(index, "treatmentXref")
                endpoint_xref = self.read_cell_by_name(index, "endpointXref")
                if not e_summary == "":
                    population = self._get_population(ap_subset)
                    if population:
                        ap = self.create_object(
                            AnalysisPopulation,
                            {
                                "name": f"AP_{index + 1}",
                                "text": ap_description,
                                "subsetOfIds": [population.id],
                            },
                        )
                        if ap:
                            self.populations.append(ap)
                            params = {
                                "name": e_name,
                                "description": "",
                                "label": e_name,
                                "populationSummary": e_summary,
                                "analysisPopulationId": ap.id,
                                "interventionIds": [
                                    self._get_treatment(treatment_xref)
                                ],
                                "variableOfInterestId": self._get_endpoint(
                                    endpoint_xref
                                ),
                                "intercurrentEvents": [],
                            }
                            current = self.create_object(Estimand, params)
                            if current:
                                self.estimands.append(current)
                if current is not None:
                    ice_name = current_ice_name if ice_name == "" else ice_name
                    ice_description = (
                        current_ice_description
                        if ice_description == ""
                        else ice_description
                    )
                    ice = self.create_object(
                        IntercurrentEvent,
                        {
                            "name": ice_name,
                            "description": ice_description,
                            "label": ice_label,
                            "strategy": ice_strategy,
                            "text": ice_text,
                        },
                    )
                    current_ice_name = ice_name
                    current_ice_description = ice_description
                    if ice:
                        current.intercurrentEvents.append(ice)
                else:
                    self._general_error(
                        "Failed to add IntercurrentEvent, no Estimand set"
                    )

        except Exception as e:
            self._sheet_exception(e)

    def _get_treatment(self, name):
        return self._get_cross_reference(StudyIntervention, name)

    def _get_endpoint(self, name):
        return self._get_cross_reference(Endpoint, name)

    def _get_population(self, name):
        for klass in [StudyDesignPopulation, StudyCohort]:
            item = self.globals.cross_references.get(klass, name)
            if item:
                return item
        self._general_error(f"Unable to find population or cohort with name '{name}'")
        return None
