from usdm_excel.base_sheet import BaseSheet
from usdm_model.population_definition import StudyDesignPopulation, StudyCohort
from usdm_model.quantity_range import Quantity, Range
from usdm_model.characteristic import Characteristic
from usdm_model.indication import Indication
from usdm_excel.globals import Globals


class StudyDesignPopulationSheet(BaseSheet):
    SHEET_NAME = "studyDesignPopulations"

    def __init__(self, file_path: str, globals: Globals):
        try:
            self._cohorts = []
            super().__init__(
                file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME
            )
            self.population = None
            for index, row in self.sheet.iterrows():
                level = self.read_cell_by_name(index, "level")
                name = self.read_cell_by_name(index, "name")
                description = self.read_cell_by_name(index, "description")
                label = self.read_cell_by_name(index, "label")
                completion_number = self._read_range_quantity(
                    index,
                    "plannedCompletionNumber",
                )
                enrollment_number = self._read_range_quantity(
                    index,
                    "plannedEnrollmentNumber",
                )

                planned_age = self.read_range_cell_by_name(
                    index, "plannedAge", require_units=True, allow_empty=True
                )
                healthy = self.read_boolean_cell_by_name(
                    index, "includesHealthySubjects", must_be_present=False
                )
                characteristics = self.read_cell_multiple_by_name(
                    index, "characteristics", must_be_present=False
                )
                indications = self.read_cell_multiple_by_name(
                    index, "indications", must_be_present=False
                )
                codes = self._build_codes(row, index)
                if level.upper() == "MAIN":
                    self.population = self._study_population(
                        name,
                        description,
                        label,
                        enrollment_number,
                        completion_number,
                        planned_age,
                        healthy,
                        codes,
                    )
                else:
                    cohort = self._study_cohort(
                        name,
                        description,
                        label,
                        enrollment_number,
                        completion_number,
                        planned_age,
                        healthy,
                        codes,
                        characteristics,
                        indications,
                    )
            if self.population:
                self.population.cohorts = self._cohorts
            else:
                self._general_error(f"Not main study population detected")
        except Exception as e:
            self._sheet_exception(e)

    def _build_codes(self, row, index):
        code = self.read_cdisc_klass_attribute_cell_by_name(
            "StudyDesignPopulation",
            "plannedSexOfParticipants",
            index,
            "plannedSexOfParticipants",
            allow_empty=True,
        )
        return [code] if code else []

    def _study_population(
        self,
        name: str,
        description: str,
        label: str,
        enrollment_number: Range | Quantity,
        completion_number: Range | Quantity,
        planned_age: Range,
        healthy: bool,
        codes: list,
    ) -> StudyDesignPopulation:
        # planned_completion_range = (
        #     completion_number if isinstance(completion_number, Range) else None
        # )
        # planned_completion_quantity = (
        #     completion_number if isinstance(completion_number, Quantity) else None
        # )
        # planned_enrollment_range = (
        #     enrollment_number if isinstance(enrollment_number, Range) else None
        # )
        # planned_enrollment_quantity = (
        #     enrollment_number if isinstance(enrollment_number, Quantity) else None
        # )
        params = {
            "name": name,
            "description": description,
            "label": label,
            "includesHealthySubjects": healthy,
            "plannedEnrollmentNumber": enrollment_number,
            "plannedCompletionNumber": completion_number,
            "plannedAge": planned_age,
            "plannedSex": codes,
        }
        item = self.create_object(StudyDesignPopulation, params)
        if item:
            self.globals.cross_references.add(name, item)
        return item

    def _study_cohort(
        self,
        name: str,
        description: str,
        label: str,
        enrollment_number: Range | Quantity,
        completion_number: Range | Quantity,
        planned_age: Range,
        healthy: bool,
        codes: list,
        characteristics: list,
        indications: list,
    ) -> StudyCohort:
        # planned_completion_range = (
        #     completion_number if isinstance(completion_number, Range) else None
        # )
        # planned_completion_quantity = (
        #     completion_number if isinstance(completion_number, Quantity) else None
        # )
        # planned_enrollment_range = (
        #     enrollment_number if isinstance(enrollment_number, Range) else None
        # )
        # planned_enrollment_quantity = (
        #     enrollment_number if isinstance(enrollment_number, Quantity) else None
        # )
        characteristic_refs = self._resolve_characteristics(characteristics)
        indication_refs = self._resolve_indications(indications)
        params = {
            "name": name,
            "description": description,
            "label": label,
            "includesHealthySubjects": healthy,
            "plannedEnrollmentNumber": enrollment_number,
            "plannedCompletionNumber": completion_number,
            "plannedAge": planned_age,
            "plannedSex": codes,
            "characteristics": characteristic_refs,
            "indicationIds": [indication.id for indication in indication_refs],
        }
        item = self.create_object(StudyCohort, params)
        if item:
            self.globals.cross_references.add(name, item)
            self._cohorts.append(item)
        return item

    def _resolve_characteristics(self, names):
        results = []
        for name in names:
            object = self.globals.cross_references.get(Characteristic, name)
            if object:
                results.append(object)
            else:
                self._general_warning(f"Characterisitc '{name}' not found")
        return results

    def _resolve_indications(self, names):
        # print(f"Resolving indications: {names}")
        results = []
        for name in names:
            object = self.globals.cross_references.get(Indication, name)
            if object:
                results.append(object)
            else:
                self._general_warning(f"Indication '{name}' not found")
        return results

    def _read_range_quantity(self, index, field_name):
        text = self.read_cell_by_name(index, field_name)
        return (
            self.read_range_cell_by_name(
                index, field_name, require_units=False, allow_empty=True
            )
            if ".." in text
            else self.read_quantity_cell_by_name(
                index, field_name, allow_missing_units=True, allow_empty=True
            )
        )
