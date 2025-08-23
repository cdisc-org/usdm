from usdm_excel.configuration_sheet import ConfigurationSheet
from usdm_excel.study_sheet.study_sheet import StudySheet
from usdm_excel.errors_and_logging.errors import Errors
from usdm_excel.globals import Globals
from usdm_excel.annotation_sheet.annotation_sheet import AnnotationSheet
from usdm_excel.abbreviation_sheet.abbreviation_sheet import AbbreviationSheet
from usdm_excel.study_identifier_and_organization_sheets.study_identifiers_sheet import (
    StudyIdentifiersSheet,
)
from usdm_excel.study_identifier_and_organization_sheets.study_references_sheet import (
    StudyReferencesSheet,
)
from usdm_excel.study_design_sheet.study_design_sheet import StudyDesignSheet
from usdm_excel.study_soa_v2_sheet.study_soa_v2_sheet import StudySoAV2Sheet
from usdm_excel.study_design_indication_sheet.study_design_indication_sheet import (
    StudyDesignIndicationSheet,
)
from usdm_excel.study_design_intervention_sheet.study_design_intervention_sheet import (
    StudyDesignInterventionSheet,
)
from usdm_excel.study_product_sheet.study_product_sheet import StudyProductSheet
from usdm_excel.study_design_population_sheet.study_design_population_sheet import (
    StudyDesignPopulationSheet,
)
from usdm_excel.study_design_objective_endpoint_sheet.study_design_objective_endpoint_sheet import (
    StudyDesignObjectiveEndpointSheet,
)
from usdm_excel.study_design_estimands_sheet.study_design_estimands_sheet import (
    StudyDesignEstimandsSheet,
)
from usdm_excel.study_design_procedure_sheet.study_design_procedure_sheet import (
    StudyDesignProcedureSheet,
)
from usdm_excel.study_design_encounter_sheet.study_design_encounter_sheet import (
    StudyDesignEncounterSheet,
)
from usdm_excel.study_design_element_sheet.study_design_element_sheet import (
    StudyDesignElementSheet,
)
from usdm_excel.study_design_arm_sheet.study_design_arm_sheet import StudyDesignArmSheet
from usdm_excel.study_design_epoch_sheet.study_design_epoch_sheet import (
    StudyDesignEpochSheet,
)
from usdm_excel.study_design_activity_sheet.study_design_activity_sheet import (
    StudyDesignActivitySheet,
)
from usdm_excel.study_design_timing_sheet.study_design_timing_sheet import (
    StudyDesignTimingSheet,
)
from usdm_excel.study_definition_document.document_content_sheet import (
    DocumentContentSheet,
)
from usdm_excel.study_definition_document.document_template_sheet import (
    DocumentTemplates,
)
from usdm_excel.study_amendment_sheet.study_amendment_sheet import StudyAmendmentSheet
from usdm_excel.study_amendment_sheet.study_amendment_changes_sheet import (
    StudyAmendmentChangesSheet,
)
from usdm_excel.study_amendment_sheet.study_amendment_impact_sheet import (
    StudyAmendmentImpactSheet,
)
from usdm_excel.study_design_dictionary_sheet.study_design_dictionary_sheet import (
    StudyDesignDictionarySheet,
)
from usdm_excel.study_design_eligibility_criteria_sheet.study_design_eligibility_criteria_sheet import (
    StudyDesignEligibilityCriteriaSheet,
)
from usdm_excel.study_design_sites_sheet.study_design_sites_sheet import (
    StudyDesignSitesSheet,
)
from usdm_excel.study_design_conditions_sheet.study_design_conditions_sheet import (
    StudyDesignConditionSheet,
)
from usdm_excel.study_design_characteristics_sheet.study_design_characteristics_sheet import (
    StudyDesignCharacteristicSheet,
)
from usdm_excel.assigned_person_sheet.assigned_person_sheet import AssignedPersonSheet
from usdm_excel.study_role_sheet.study_role_sheet import StudyRoleSheet
from usdm_excel.study_identifier_and_organization_sheets.study_identifiers_sheet import (
    StudyIdentifiersSheet,
)
from usdm_excel.study_identifier_and_organization_sheets.study_references_sheet import (
    StudyReferencesSheet,
)
from usdm_excel.study_identifier_and_organization_sheets.study_organizations_sheet import (
    StudyOrganizationsSheet,
)
from usdm_excel.study_product_sheet.study_devices_sheet import StudyDevicesSheet
from usdm_excel.study_product_sheet.study_product_organization_role_sheet import (
    StudyProductOrganizationRoleSheet,
)
from usdm_excel.study_design_specimen_retention_sheet.study_design_specimen_retention_sheet import (
    StudyDesignSpecimenRetentionSheet,
)
from usdm_excel.option_manager import Options, EmptyNoneOption
from usdm_excel.cdisc_ct import CDISCCT
from usdm_excel.other_ct import OtherCT
from usdm_excel.duplicate_object import duplicate_object
from usdm_model.study import Study
from usdm_model.study_design import StudyDesign
from usdm_model.study_version import StudyVersion
from usdm_model.study_definition_document_version import StudyDefinitionDocumentVersion
from usdm_model.study_definition_document import StudyDefinitionDocument
from usdm_model.wrapper import Wrapper
from usdm_info import (
    __model_version__ as usdm_version,
    __package_version__ as system_version,
)


class USDMExcel:
    SYSTEM_NAME = "CDISC USDM E2J"
    STUDY_VERSION_DATE = "study_version"
    PROTOCOL_VERSION_DATE = "protocol_document"

    def __init__(self, file_path):
        self._globals = Globals()
        self._file_path = file_path

    def execute(self):
        self._globals.create()
        return self._process()

    def errors(self):
        return self._globals.errors_and_logging.errors().dump(Errors.WARNING)

    def is_m11(self):
        return self._globals.template_manager.includes("M11")

    def was_m11(self):
        self._globals.errors_and_logging.deprecated(
            "Method 'was_m11' deprecated, use 'is_m11' going forward"
        )
        return self._globals.template_manager.includes("M11")

    def default_template(self):
        return self._globals.template_manager.default_template

    def templates(self):
        return self._globals.template_manager.templates()

    def _process(self):
        try:
            # Read the configuration. Override the template if requested and present, otherwise leave as configured
            self.configuration = ConfigurationSheet(self._file_path, self._globals)

            # Process all the remaining sheets
            self.notes = AnnotationSheet(self._file_path, self._globals)
            self.abbreviations = AbbreviationSheet(self._file_path, self._globals)
            self.organizations = StudyOrganizationsSheet(self._file_path, self._globals)
            self.specimen_retentions = StudyDesignSpecimenRetentionSheet(
                self._file_path, self._globals
            )
            self.products = StudyProductSheet(self._file_path, self._globals)
            self.devices = StudyDevicesSheet(self._file_path, self._globals)
            self.study = StudySheet(self._file_path, self._globals)
            self.timings = StudyDesignTimingSheet(self._file_path, self._globals)
            self.study_amendments = StudyAmendmentSheet(self._file_path, self._globals)
            self.study_amendment_impacts = StudyAmendmentImpactSheet(
                self._file_path, self._globals
            )
            self.study_amendment_changes = StudyAmendmentChangesSheet(
                self._file_path, self._globals
            )
            self.study_identifiers = StudyIdentifiersSheet(
                self._file_path, self._globals
            )
            self.study_references = StudyReferencesSheet(self._file_path, self._globals)
            self.procedures = StudyDesignProcedureSheet(self._file_path, self._globals)
            self.encounters = StudyDesignEncounterSheet(self._file_path, self._globals)
            self.elements = StudyDesignElementSheet(self._file_path, self._globals)
            self.arms = StudyDesignArmSheet(self._file_path, self._globals)
            self.epochs = StudyDesignEpochSheet(self._file_path, self._globals)
            self.activities = StudyDesignActivitySheet(self._file_path, self._globals)
            self.study_design = StudyDesignSheet(self._file_path, self._globals)
            self._process_soa()
            self.indications = StudyDesignIndicationSheet(
                self._file_path, self._globals
            )
            self.interventions = StudyDesignInterventionSheet(
                self._file_path, self._globals
            )
            self.study_characteristics = StudyDesignCharacteristicSheet(
                self._file_path, self._globals
            )
            self.study_population = StudyDesignPopulationSheet(
                self._file_path, self._globals
            )

            self.contents = DocumentContentSheet(self._file_path, self._globals)
            self.doc_templates = DocumentTemplates(self._file_path, self._globals)

            self.dictionaries = StudyDesignDictionarySheet(
                self._file_path, self._globals
            )
            self.oe = StudyDesignObjectiveEndpointSheet(self._file_path, self._globals)
            self.eligibility_criteria = StudyDesignEligibilityCriteriaSheet(
                self._file_path, self._globals
            )
            self.estimands = StudyDesignEstimandsSheet(self._file_path, self._globals)
            self.sites = StudyDesignSitesSheet(self._file_path, self._globals)
            self.conditions = StudyDesignConditionSheet(self._file_path, self._globals)

            self.people = AssignedPersonSheet(self._file_path, self._globals)
            self.roles = StudyRoleSheet(self._file_path, self._globals)
            self.product_organization_roles = StudyProductOrganizationRoleSheet(
                self._file_path, self._globals
            )

            # Study Design assembly
            study_design: StudyDesign = self.study_design.items[0]
            if self.soa.timeline:
                study_design.scheduleTimelines.append(self.soa.timeline)
            study_design.encounters = self.encounters.items
            study_design.activities = self.soa.activities
            activity_ids = [item.id for item in study_design.activities]
            biomedicalConcepts = self.soa.biomedical_concepts
            bcSurrogates = self.soa.biomedical_concept_surrogates
            for key, tl in self.study.timelines.items():
                study_design.scheduleTimelines.append(tl.timeline)
                for activity in tl.activities:
                    if activity.id not in activity_ids:
                        study_design.activities.append(activity)
                        activity_ids.append(activity.id)
                biomedicalConcepts += tl.biomedical_concepts
                bcSurrogates += tl.biomedical_concept_surrogates
            self._double_link(study_design.activities, "previousId", "nextId")
            study_design.indications = self.indications.items
            study_design.studyInterventionIds = [x.id for x in self.interventions.items]
            study_design.population = self.study_population.population
            study_design.objectives = self.oe.objectives
            study_design.estimands = self.estimands.estimands
            study_design.analysisPopulations = self.estimands.populations
            study_design.eligibilityCriteria = self.eligibility_criteria.items
            study_design.population.criterionIds = [
                x.id for x in self.eligibility_criteria.items
            ]
            # study_design.dictionaries = self.dictionaries.items
            # study_design.conditions = self.conditions.items

            self.definition_documents = []
            self.definition_document_version_ids = []
            self.definition_document_version = []
            for index, template in enumerate(self.doc_templates.items):
                # Final assembly
                try:
                    dates = []
                    for x in self.study.dates[self.PROTOCOL_VERSION_DATE]:
                        if index == 0:
                            dates.append(x)
                        else:
                            dates.append(duplicate_object(x, self._globals))
                    definition_document_version = StudyDefinitionDocumentVersion(
                        id=self._globals.id_manager.build_id(
                            StudyDefinitionDocumentVersion
                        ),
                        version=self.study.protocol_version,
                        status=self.study.protocol_status
                        if index == 0
                        else duplicate_object(
                            self.study.protocol_status, self._globals
                        ),
                        dateValues=dates,
                        contents=template.items,
                    )
                    self.definition_document_version.append(definition_document_version)
                    self.definition_document_version_ids.append(
                        definition_document_version.id
                    )
                    self._globals.cross_references.add(
                        definition_document_version.id, definition_document_version
                    )
                except Exception as e:
                    self._globals.errors_and_logging.exception(
                        f"Error creating StudyDefinitionDocumentVersion object", e
                    )

                try:
                    definition_document = StudyDefinitionDocument(
                        id=self._globals.id_manager.build_id(StudyDefinitionDocument),
                        name=f"Protocol_Document_{self.study.name}",
                        versions=[definition_document_version],
                        language=OtherCT(self._globals).code(
                            "en", "ISO", "1", "English"
                        ),
                        type=CDISCCT(self._globals).code("C70817", "Protocol"),
                        templateName=template.name,
                    )
                    self.definition_documents.append(definition_document)
                    self.study_amendments.set_document(definition_document)
                except Exception as e:
                    self._globals.errors_and_logging.exception(
                        f"Error creating StudyDefinitionDocument object", e
                    )

            try:
                self.study_version = StudyVersion(
                    id=self._globals.id_manager.build_id(StudyVersion),
                    versionIdentifier=self.study.version,
                    businessTherapeuticAreas=self.study.therapeutic_areas,
                    rationale=self.study.rationale,
                    studyIdentifiers=self.study_identifiers.items,
                    referenceIdentifiers=self.study_references.items,
                    documentVersionIds=self.definition_document_version_ids,
                    studyDesigns=self.study_design.items,
                    dateValues=self.study.dates[self.STUDY_VERSION_DATE],
                    amendments=self.study_amendments.items,
                    titles=self.study.titles,
                    eligibilityCriterionItems=self.eligibility_criteria.criterion_items,
                    narrativeContentItems=self.contents.items,
                    abbreviations=self.abbreviations.items,
                    organizations=self.organizations.items,
                    roles=self.roles.items,
                    medicalDevices=self.devices.items,
                    administrableProducts=self.products.items,
                    productOrganizationRoles=self.product_organization_roles.items,
                    studyInterventions=self.interventions.items,
                    conditions=self.conditions.items,
                    biomedicalConcepts=biomedicalConcepts,
                    bcSurrogates=bcSurrogates,
                    dictionaries=self.dictionaries.items,
                )
                self._globals.cross_references.add(
                    self.study_version.id, self.study_version
                )
            except Exception as e:
                self._globals.errors_and_logging.exception(
                    f"Error creating StudyVersion object", e
                )

            try:
                self.study = Study(
                    id=None,  # No Id, will be allocated a UUID
                    name=self.study.name,
                    label=self.study.label,
                    description=self.study.description,
                    versions=[self.study_version],
                    documentedBy=self.definition_documents,
                )
                self._globals.cross_references.add("STUDY", self.study)
                for document in self.definition_document_version:
                    self.contents.resolve(
                        self.study_version, document
                    )  # Now we have full study, resolve references in the content
            except Exception as e:
                self._globals.errors_and_logging.exception(
                    f"Error creating Study object", e
                )

            return Wrapper(
                study=self.study,
                usdmVersion=usdm_version,
                systemName=self.SYSTEM_NAME,
                systemVersion=system_version,
            )

        except Exception as e:
            self._globals.errors_and_logging.exception(
                f"Error processing Excel workbook", e
            )
            return None

    def _process_soa(self):
        tls = []
        for timeline in self.study_design.other_timelines:
            tl = StudySoAV2Sheet(self._file_path, self._globals, timeline, False)
            tls.append(tl)
            self.study.timelines[timeline] = tl
            self._globals.cross_references.add(timeline, tl.timeline)
        self.soa = StudySoAV2Sheet(
            self._file_path, self._globals, self.study_design.main_timeline, True
        )
        if self.soa.timeline:
            self._globals.cross_references.add(
                self.study_design.main_timeline, self.soa.timeline
            )
            tls.append(self.soa)
        self._set_timing_references(tls)
        self._check_timing_references(tls)

    def _check_timing_references(self, tls):
        timing_check = {}
        for timing in self.timings.items:
            timing_check[timing.name] = None
        for tl in tls:
            tl_items = tl.check_timing_references(self.timings.items, timing_check)
            tl.timeline.timings = tl_items
        for timing in self.timings.items:
            if not timing_check[timing.name]:
                self._globals.errors_and_logging.error(
                    f"Timing with name '{timing.name}' not referenced"
                )

    def _set_timing_references(self, tls):
        for timing in self.timings.items:
            found = {"from": False, "to": False}
            for tl in tls:
                if not found["from"]:
                    instance = tl.timing_match(timing.relativeFromScheduledInstanceId)
                    if instance:
                        item = instance.item
                        timing.relativeFromScheduledInstanceId = item.id
                        found["from"] = True
                if not found["to"]:
                    instance = tl.timing_match(timing.relativeToScheduledInstanceId)
                    if instance:
                        item = instance.item
                        timing.relativeToScheduledInstanceId = item.id
                        found["to"] = True
            if not found["from"]:
                self._globals.errors_and_logging.error(
                    f"Unable to find timing 'from' reference with name {timing.relativeFromScheduledInstanceId}"
                )
            if not found["to"]:
                self._globals.errors_and_logging.error(
                    f"Unable to find timing 'to' reference with name {timing.relativeToScheduledInstanceId}"
                )

    def _double_link(self, items, prev, next):
        try:
            for idx, item in enumerate(items):
                if idx == 0:
                    if (
                        self._globals.option_manager.get(Options.EMPTY_NONE)
                        == EmptyNoneOption.EMPTY.value
                    ):
                        setattr(item, prev, "")
                    else:
                        setattr(item, prev, None)
                else:
                    the_id = getattr(items[idx - 1], "id")
                    setattr(item, prev, the_id)
                if idx == len(items) - 1:
                    if (
                        self._globals.option_manager.get(Options.EMPTY_NONE)
                        == EmptyNoneOption.EMPTY.value
                    ):
                        setattr(item, next, "")
                    else:
                        setattr(item, next, None)
                else:
                    the_id = getattr(items[idx + 1], "id")
                    setattr(item, next, the_id)
        except Exception as e:
            self._globals.errors_and_logging.exception(
                f"Error in double_link: {items}", e
            )
