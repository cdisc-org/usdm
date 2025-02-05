from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithId
from .code import Code
from .identifier import StudyIdentifier, ReferenceIdentifier
from .study_design import InterventionalStudyDesign, ObservationalStudyDesign
from .governance_date import GovernanceDate
from .study_amendment import StudyAmendment
from .study_title import StudyTitle
from .eligibility_criterion import EligibilityCriterion
from .narrative_content import NarrativeContentItem
from .comment_annotation import CommentAnnotation
from .abbreviation import Abbreviation
from .study_role import StudyRole
from .organization import Organization
from .administrable_product import AdministrableProduct
from .medical_device import MedicalDevice
from .product_organization_role import ProductOrganizationRole


class StudyVersion(ApiBaseModelWithId):
    versionIdentifier: str
    rationale: str
    documentVersionIds: List[str] = []
    dateValues: List[GovernanceDate] = []
    amendments: List[StudyAmendment] = []
    businessTherapeuticAreas: List[Code] = []
    studyIdentifiers: List[StudyIdentifier]
    referenceIdentifiers: List[ReferenceIdentifier] = []
    studyDesigns: List[Union[InterventionalStudyDesign, ObservationalStudyDesign]] = []
    titles: List[StudyTitle]
    criteria: List[EligibilityCriterion] = []  # Not in API
    narrativeContentItems: List[NarrativeContentItem] = []
    abbreviations: List[Abbreviation] = []
    roles: List[StudyRole] = []
    organizations: List[Organization] = []
    administrableProducts: List[AdministrableProduct] = []
    medicalDevices: List[MedicalDevice] = []
    productOrganizationRoles: List[ProductOrganizationRole] = []
    notes: List[CommentAnnotation] = []
    instanceType: Literal["StudyVersion"]

    def get_title(self, title_type):
        for title in self.titles:
            if title.type.decode == title_type:
                return title
        return None

    def sponsor_identifier(self):
        for identifier in self.studyIdentifiers:
            org = self.organization(identifier.scopeId)
            if org and org.type.code == "C70793":
                return identifier
        return None

    #  Now in StudyDesign
    #  def phase(self):
    #    return self.studyPhase.standardCode

    def organization(self, id: str) -> Organization:
        return next((x for x in self.organizations if x.id == id), None)
