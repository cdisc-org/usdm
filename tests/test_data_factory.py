from usdm_model.study_design import InterventionalStudyDesign
from usdm_model.study_epoch import StudyEpoch
from usdm_model.study_cell import StudyCell
from usdm_model.study_arm import StudyArm
from usdm_model.population_definition import *
from usdm_model.study import Study
from usdm_model.study_version import StudyVersion
from usdm_model.study_title import StudyTitle
from usdm_model.study_definition_document import StudyDefinitionDocument
from usdm_model.study_definition_document_version import StudyDefinitionDocumentVersion
from usdm_model.identifier import StudyIdentifier
from usdm_model.organization import Organization
from usdm_model.address import Address
from usdm_model.governance_date import GovernanceDate
from usdm_model.geographic_scope import GeographicScope
from usdm_model.subject_enrollment import SubjectEnrollment
from usdm_model.study_amendment import StudyAmendment
from usdm_model.study_amendment_reason import StudyAmendmentReason
from usdm_model.study_element import StudyElement
from usdm_model.quantity_range import Quantity
from usdm_excel.globals import Globals
from tests.test_factory import Factory


class MinimalStudy:
    def __init__(self, globals: Globals):
        globals.id_manager.clear()
        factory = Factory(globals)
        feedback_reason = factory.item(
            StudyAmendmentReason,
            {"code": factory.cdisc_code("C207605", "IRB/IEC Feedback")},
        )
        other_reason = factory.item(
            StudyAmendmentReason,
            {
                "code": factory.cdisc_code("C17649", "Other"),
                "otherReason": "Fix typographical errors",
            },
        )
        subjects = factory.item(Quantity, {"value": 10.0})
        enrollment = factory.item(
            SubjectEnrollment,
            {
                "name": "ENROLL1",
                "type": factory.cdisc_code("C68846", "Global"),
                "quantity": subjects,
            },
        )
        geo_scope = factory.item(
            GeographicScope, {"type": factory.cdisc_code("C68846", "Global")}
        )
        amendment = factory.item(
            StudyAmendment,
            {
                "name": "AMEND1",
                "number": "1",
                "summary": "Updated inclusion criteria",
                "substantialImpact": True,
                "primaryReason": feedback_reason,
                "secondaryReasons": [other_reason],
                "enrollments": [enrollment],
                "geographicScopes": [geo_scope],
            },
        )
        global_scope = factory.item(
            GeographicScope, {"type": factory.cdisc_code("C68846", "Global")}
        )
        europe_code = factory.alias_code(factory.geo_code("150", "Europe"), [])
        europe_scope = factory.item(
            GeographicScope,
            {"type": factory.cdisc_code("C41129", "Region"), "code": europe_code},
        )
        study_approval_date = factory.item(
            GovernanceDate,
            {
                "name": "D_APPROVE",
                "label": "Design Approval",
                "description": "Design approval date",
                "type": factory.cdisc_code("C132352", "Protocol Approval by Sponsor Date"),
                "dateValue": "2006-06-01",
                "geographicScopes": [global_scope],
            },
        )
        doc_approval_date = factory.item(
            GovernanceDate,
            {
                "name": "D_APPROVE",
                "label": "Design Approval",
                "description": "Design approval date",
                "type": factory.cdisc_code("C207598", "Sponsor Approval Date"),
                "dateValue": "2006-06-01",
                "geographicScopes": [europe_scope],
            },
        )
        phase_code = factory.cdisc_code("C12345", "Phase Code")
        alias_phase = factory.alias_code(phase_code, [])
        self.population = factory.item(
            StudyDesignPopulation,
            {
                "name": "POP1",
                "label": "",
                "description": "",
                "includesHealthySubjects": True,
                "criteria": [],
            },
        )
        element = factory.item(StudyElement, {"name": "Element1"})
        arm = factory.item(
            StudyArm,
            {
                "name": "Arm1",
                "type": factory.cdisc_dummy(),
                "dataOriginDescription": "xxx",
                "dataOriginType": factory.cdisc_dummy(),
            },
        )
        epoch = factory.item(
            StudyEpoch,
            {
                "name": "EP1",
                "label": "Epoch A",
                "description": "",
                "type": factory.cdisc_code("C22222", "Epoch Code"),
            },
        )
        cell = factory.item(
            StudyCell,
            {"armId": arm.id, "epochId": epoch.id, "elementIds": [element.id]},
        )
        study_title = factory.item(
            StudyTitle,
            {
                "text": "Title",
                "type": factory.cdisc_code("C44444", "Official Study Title"),
            },
        )
        study_short_title = factory.item(
            StudyTitle,
            {
                "text": "Short Title",
                "type": factory.cdisc_code("C33333", "Brief Study Title"),
            },
        )
        study_acronym = factory.item(
            StudyTitle,
            {"text": "ACRONYM", "type": factory.cdisc_code("C33333", "Study Acronym")},
        )
        self.study_definition_document_version = factory.item(
            StudyDefinitionDocumentVersion,
            {
                "version": "1",
                "status": factory.cdisc_dummy(),
                "dateValues": [doc_approval_date],
            },
        )
        self.study_definition_document = factory.item(
            StudyDefinitionDocument,
            {
                "name": "PD1",
                "label": "Protocol Document",
                "description": "",
                "language": factory.english(),
                "type": factory.cdisc_code("C70817", "Protocol"),
                "templateName": "Sponsor",
                "versions": [self.study_definition_document_version],
            },
        )
        self.study_design = factory.item(
            InterventionalStudyDesign,
            {
                "name": "Study Design",
                "label": "",
                "description": "",
                "rationale": "Study Design Rationale",
                "interventionModel": factory.cdisc_code("C98388", "Interventional"),
                "arms": [arm],
                "studyCells": [cell],
                "epochs": [epoch],
                "population": self.population,
                "studyPhase": alias_phase,
                "model": factory.cdisc_code("C82639", "Parallel Study"),
            },
        )
        address = factory.item(
            Address,
            {
                "line": "line 1",
                "city": "City",
                "district": "District",
                "state": "State",
                "postalCode": "12345",
                "country": factory.code("UKK", "UKK_decode"),
            },
        )
        organization_1 = factory.item(
            Organization,
            {
                "name": "Sponsor",
                "type": factory.cdisc_code("C54149", "Pharmaceutical Company"),
                "identifier": "123456789",
                "identifierScheme": "DUNS",
                "legalAddress": address,
            },
        )
        identifier = factory.item(
            StudyIdentifier, {"text": "SPONSOR-1234", "scopeId": organization_1.id}
        )
        organization_2 = factory.item(
            Organization,
            {
                "name": "Sponsor",
                "type": factory.cdisc_code("C188863", "reg 1"),
                "identifier": "REG 1",
                "identifierScheme": "DUNS",
                "legalAddress": address,
            },
        )
        reg_1_identifier = factory.item(
            StudyIdentifier, {"text": "REG 111111", "scopeId": organization_2.id}
        )
        organization_3 = factory.item(
            Organization,
            {
                "name": "Sponsor",
                "type": factory.cdisc_code("C93453", "reg 2"),
                "identifier": "REG 2",
                "identifierScheme": "DUNS",
                "legalAddress": address,
            },
        )
        reg_2_identifier = factory.item(
            StudyIdentifier, {"text": "REG 222222", "scopeId": organization_3.id}
        )
        self.study_version = factory.item(
            StudyVersion,
            {
                "versionIdentifier": "1",
                "rationale": "Study version rationale",
                "titles": [study_title, study_short_title, study_acronym],
                "studyDesigns": [self.study_design],
                "documentVersionId": self.study_definition_document_version.id,
                "studyIdentifiers": [identifier, reg_1_identifier, reg_2_identifier],
                "studyPhase": alias_phase,
                "dateValues": [study_approval_date],
                "amendments": [amendment],
                "organizations": [organization_1, organization_2, organization_3],
            },
        )
        self.study = factory.item(
            Study,
            {
                "id": None,
                "name": "Study",
                "label": "",
                "description": "",
                "versions": [self.study_version],
                "documentedBy": [self.study_definition_document],
            },
        )
        # print(f"MINIMAL: {self.study.to_json()}")
