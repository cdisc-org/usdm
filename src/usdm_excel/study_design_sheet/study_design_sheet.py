import traceback
from usdm_excel.base_sheet import BaseSheet
from usdm_model.study_epoch import StudyEpoch
from usdm_model.study_arm import StudyArm
from usdm_model.study_element import StudyElement
from usdm_model.study_cell import StudyCell
from usdm_model.study_design import (
    StudyDesign,
    ObservationalStudyDesign,
    InterventionalStudyDesign,
)
from usdm_model.masking import Masking
from usdm_excel.alias import Alias
from usdm_model.biospecimen_retention import BiospecimenRetention
from usdm_model.population_definition import StudyDesignPopulation
from usdm_excel.option_manager import *
from usdm_excel.cdisc_ct import CDISCCT
from usdm_excel.globals import Globals


class StudyDesignSheet(BaseSheet):
    SHEET_NAME = "studyDesign"

    NAME_KEY = ["studyDesignName", "name"]
    DESCRIPTION_KEY = ["studyDesignDescription", "description"]
    LABEL_KEY = ["label"]
    TA_KEY = ["therapeuticAreas"]
    RATIONALE_KEY = ["studyDesignRationale"]
    BLINDING_KEY = ["studyDesignBlindingScheme"]
    INTENT_KEY = ["trialIntentTypes"]
    SUB_TYPES_KEY = ["trialSubTypes"]
    MODEL_KEY = ["interventionModel", "model"]
    MAIN_TIMELINE_KEY = ["mainTimeline"]
    OTHER_TIMELINES_KEY = ["otherTimelines"]
    MASKING_ROLE_KEY = ["masking"]
    PHASE_KEY = ["studyDesignPhase", "studyPhase"]
    STUDY_TYPE_KEY = ["studyDesignType", "studyType"]
    SPECIMEN_RETENTION_KEY = ["specimenRetentions"]
    TIME_PERSPECTIVE_KEY = ["timePerspective"]
    SAMPLING_METHOD_KEY = ["samplingMethod"]
    CHARACTERISTICS_KEY = ["characteristics"]

    PARAMS_NAME_COL = 0
    PARAMS_DATA_COL = 1

    def __init__(self, file_path: str, globals: Globals):
        try:
            self.items = []
            self.interventional = True
            self.name = "TEST"
            self.description = "USDM Example Study Design"
            self.label = "USDM Example Study Design"
            self.epochs = []
            self.epoch_names = {}
            self.arms = []
            self.arm_names = {}
            self.cells = []
            self.elements = {}
            self.therapeutic_areas = []
            self.rationale = ""
            self.blinding = None
            self.trial_intents = []
            self.study_type = None
            self.trial_sub_types = []
            self.intervention_model = None
            self.main_timeline = None
            self.other_timelines = []
            self.masks = []
            self.phase = None
            self.specimen_retentions = []
            self.time_perspective = None
            self.sampling_methods = []
            self.characteristics = []
            super().__init__(
                file_path=file_path,
                globals=globals,
                sheet_name=self.SHEET_NAME,
                header=None,
            )
            self.process_sheet()
        except Exception as e:
            self._sheet_exception(e)

    def process_sheet(self):
        general_params = True
        resolved_epochs = [None] * self.sheet.shape[1]
        resolved_arms = [None] * self.sheet.shape[0]
        for rindex, row in self.sheet.iterrows():
            key = self.read_cell(rindex, self.PARAMS_NAME_COL)
            if general_params:
                if key in self.NAME_KEY:
                    self.name = self.read_cell(rindex, self.PARAMS_DATA_COL)
                elif key in self.LABEL_KEY:
                    self.label = self.read_cell(rindex, self.PARAMS_DATA_COL)
                elif key in self.DESCRIPTION_KEY:
                    self.description = self.read_cell(rindex, self.PARAMS_DATA_COL)
                elif key in self.TA_KEY:
                    self.therapeutic_areas = self.read_other_code_cell_mutiple(
                        rindex, self.PARAMS_DATA_COL
                    )
                elif key in self.RATIONALE_KEY:
                    self.rationale = self.read_cell(rindex, self.PARAMS_DATA_COL)
                elif key in self.BLINDING_KEY:
                    self.blinding = Alias(self.globals).code(
                        self.read_cdisc_klass_attribute_cell(
                            "StudyDesign",
                            "studyDesignBlindingScheme",
                            rindex,
                            self.PARAMS_DATA_COL,
                        ),
                        [],
                    )
                elif key in self.INTENT_KEY:
                    self.trial_intents = self.read_cdisc_klass_attribute_cell_multiple(
                        "StudyDesign", "trialIntentType", rindex, self.PARAMS_DATA_COL
                    )
                elif key in self.STUDY_TYPE_KEY:
                    self.study_type = self.read_cdisc_klass_attribute_cell(
                        "StudyDesign", "studyType", rindex, self.PARAMS_DATA_COL
                    )
                    if self.study_type.code == "C16084":
                        self.interventional = False
                elif key in self.SUB_TYPES_KEY:
                    self.trial_sub_types = (
                        self.read_cdisc_klass_attribute_cell_multiple(
                            "StudyDesign", "subTypes", rindex, self.PARAMS_DATA_COL
                        )
                    )
                elif key in self.MODEL_KEY:
                    self.intervention_model = self.read_cdisc_klass_attribute_cell(
                        "StudyDesign", "interventionModel", rindex, self.PARAMS_DATA_COL
                    )
                elif key in self.MAIN_TIMELINE_KEY:
                    # print(f"MAIN TL: {rindex}")
                    self.main_timeline = self.read_cell(rindex, self.PARAMS_DATA_COL)
                elif key in self.OTHER_TIMELINES_KEY:
                    # print(f"OTHER TL: {rindex}")
                    self.other_timelines = self.read_cell_multiple(
                        rindex, self.PARAMS_DATA_COL
                    )
                elif key in self.MASKING_ROLE_KEY:
                    self._warning(
                        rindex,
                        self.PARAMS_NAME_COL,
                        f"Masking has been moved to the 'roles' sheet, value ignored",
                    )
                    # self._set_masking(rindex, self.PARAMS_DATA_COL)
                elif key in self.PHASE_KEY:
                    phase = self.read_cdisc_klass_attribute_cell(
                        "StudyDesign", "studyPhase", rindex, self.PARAMS_DATA_COL
                    )
                    self.phase = Alias(self.globals).code(phase, [])
                elif key in self.SPECIMEN_RETENTION_KEY:
                    specimen_refs = self.read_cell_multiple(
                        rindex, self.PARAMS_DATA_COL
                    )
                    for ref in specimen_refs:
                        specimen = self.globals.cross_references.get(
                            BiospecimenRetention, ref
                        )
                        if specimen is not None:
                            self.specimen_retentions.append(specimen)
                elif key in self.TIME_PERSPECTIVE_KEY:
                    self.time_perspective = self.read_cdisc_klass_attribute_cell(
                        "StudyDesign", "timePerspective", rindex, self.PARAMS_DATA_COL
                    )
                elif key in self.SAMPLING_METHOD_KEY:
                    self.sampling_method = self.read_cdisc_klass_attribute_cell(
                        "StudyDesign", "samplingMethod", rindex, self.PARAMS_DATA_COL
                    )
                elif key in self.CHARACTERISTICS_KEY:
                    self.characteristics = (
                        self.read_cdisc_klass_attribute_cell_multiple(
                            "StudyDesign",
                            "characteristics",
                            rindex,
                            self.PARAMS_DATA_COL,
                        )
                    )
                elif key == "":
                    general_params = False
                    start_row = rindex + 1
                else:
                    self._warning(
                        rindex,
                        self.PARAMS_NAME_COL,
                        f"Unrecognized key '{key}', ignored",
                    )
            else:
                for cindex in range(0, len(self.sheet.columns)):
                    epoch_index = cindex - 1
                    cell = self.read_cell(rindex, cindex)
                    # print(f"ARMS EPOCHS: {rindex} = {cell}")
                    if rindex == start_row:
                        if cindex != 0:
                            resolved_epochs[epoch_index] = self._add_epoch(cell)
                    else:
                        arm_index = rindex - start_row - 1
                        if cindex == 0:
                            resolved_arms[arm_index] = self._add_arm(cell)
                        else:
                            cell_elements = []
                            element_names = self.read_cell_multiple(rindex, cindex)
                            for name in element_names:
                                element = self._add_element(name)
                                if element is not None:
                                    cell_elements.append(element.id)
                            cell_arm = resolved_arms[arm_index].id
                            cell_epoch = resolved_epochs[epoch_index].id
                            if cell_arm is not None and cell_epoch is not None:
                                self.cells.append(
                                    self._add_cell(
                                        arm=cell_arm,
                                        epoch=cell_epoch,
                                        elements=cell_elements,
                                    )
                                )
                            else:
                                self._general_error(
                                    f"Cannot resolve arm and/or epoch for cell [{arm_index + 1},{epoch_index + 1}]"
                                )

            self.double_link(self.epochs, "previousId", "nextId")

        study_design = self._create_design()
        if study_design:
            self.items.append(study_design)

    def _add_arm(self, name):
        arm = self.globals.cross_references.get(StudyArm, name)
        if arm is not None:
            if name not in self.arm_names:
                self.arm_names[name] = True
                self.arms.append(arm)
            return arm
        else:
            self._general_error(f"No arm definition found for arm '{name}'")
            return None

    def _add_epoch(self, name):
        epoch = self.globals.cross_references.get(StudyEpoch, name)
        if epoch is not None:
            if name not in self.epoch_names:
                self.epoch_names[name] = True
                self.epochs.append(epoch)
            return epoch
        else:
            self._general_error(f"No epoch definition found for epoch '{name}'")
            return None

    def _add_element(self, name):
        element = self.globals.cross_references.get(StudyElement, name)
        if element is not None:
            if name not in self.elements:
                self.elements[name] = element
            return element
        else:
            self._general_exception(f"No element definition found for element '{name}'")
            return None

    def _add_cell(self, arm, epoch, elements):
        try:
            return StudyCell(
                id=self.globals.id_manager.build_id(StudyCell),
                armId=arm,
                epochId=epoch,
                elementIds=elements,
            )
        except Exception as e:
            self._general_exception("Failed to create StudyCell object", e)
            return None

    def _create_design(self):
        try:
            dummy_population = self.create_object(
                StudyDesignPopulation,
                {"name": "Dummy Population", "includesHealthySubjects": True},
                id="DummyPopulationId",
            )
            if self.interventional:
                result = InterventionalStudyDesign(
                    id=self.globals.id_manager.build_id(InterventionalStudyDesign),
                    name=self.name,
                    description=self.description,
                    label=self.label,
                    intentTypes=self.trial_intents,
                    studyType=self.study_type,
                    studyPhase=self.phase,
                    subTypes=self.trial_sub_types,
                    model=self.intervention_model,
                    studyCells=self.cells,
                    arms=self.arms,
                    epochs=self.epochs,
                    elements=list(self.elements.values()),
                    therapeuticAreas=self.therapeutic_areas,
                    rationale=self.rationale,
                    blindingSchema=self.blinding,
                    biospecimenRetentions=self.specimen_retentions,
                    characteristics=self.characteristics,
                    population=dummy_population,
                )
            else:
                result = ObservationalStudyDesign(
                    id=self.globals.id_manager.build_id(ObservationalStudyDesign),
                    name=self.name,
                    description=self.description,
                    label=self.label,
                    studyType=self.study_type,
                    studyPhase=self.phase,
                    subTypes=self.trial_sub_types,
                    model=self.intervention_model,
                    timePerspective=self.time_perspective,
                    samplingMethod=self.sampling_method,
                    studyCells=self.cells,
                    arms=self.arms,
                    epochs=self.epochs,
                    elements=list(self.elements.values()),
                    therapeuticAreas=self.therapeutic_areas,
                    rationale=self.rationale,
                    biospecimenRetentions=self.specimen_retentions,
                    characteristics=self.characteristics,
                    population=dummy_population,
                )
            return result
        except Exception as e:
            self._general_exception("Failed to create StudyDesign object", e)
            return None

    # def _set_masking(self, rindex, cindex):
    #     # if self.globals.option_manager.get(Options.USDM_VERSION) == '2':
    #     #   return None
    #     # else:
    #     try:
    #         text = self.read_cell(rindex, cindex)
    #         parts = text.split("=")
    #         if len(parts) == 2:
    #             code = CDISCCT(self.globals).code_for_attribute(
    #                 "Masking", "role", parts[0].strip()
    #             )
    #             if code:
    #                 mask = Masking(
    #                     id=self.globals.id_manager.build_id(Masking),
    #                     description=parts[1].strip(),
    #                     role=code,
    #                 )
    #                 self.masks.append(mask)
    #                 self.globals.cross_references.add(mask.id, mask)
    #                 return mask
    #             else:
    #                 self._error(
    #                     rindex,
    #                     cindex,
    #                     f"Failed to decode masking role data '{text}', must be a valid role code '{parts[0]}'",
    #                 )
    #                 return None
    #         else:
    #             self._error(
    #                 rindex,
    #                 cindex,
    #                 f"Failed to decode masking role data '{text}', no '=' detected",
    #             )
    #             return None
    #     except Exception as e:
    #         self._exception(rindex, cindex, "Failed to create Masking object", e)
    #         return None
