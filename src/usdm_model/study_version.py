from typing import List, Literal, Union
from .api_base_model import ApiBaseModelWithId
from .code import Code
from .identifier import StudyIdentifier, ReferenceIdentifier
from .study_design import InterventionalStudyDesign, ObservationalStudyDesign
from .governance_date import GovernanceDate
from .study_amendment import StudyAmendment
from .study_title import StudyTitle
from .eligibility_criterion import EligibilityCriterionItem
from .narrative_content import NarrativeContentItem
from .comment_annotation import CommentAnnotation
from .abbreviation import Abbreviation
from .study_role import StudyRole
from .organization import Organization
from .study_intervention import StudyIntervention
from .administrable_product import AdministrableProduct
from .medical_device import MedicalDevice
from .product_organization_role import ProductOrganizationRole
from .biomedical_concept import BiomedicalConcept
from .biomedical_concept_category import BiomedicalConceptCategory
from .biomedical_concept_surrogate import BiomedicalConceptSurrogate
from .syntax_template_dictionary import SyntaxTemplateDictionary
from .condition import Condition


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
    eligibilityCriterionItems: List[EligibilityCriterionItem] = []
    narrativeContentItems: List[NarrativeContentItem] = []
    abbreviations: List[Abbreviation] = []
    roles: List[StudyRole] = []
    organizations: List[Organization] = []
    studyInterventions: List[StudyIntervention] = []
    administrableProducts: List[AdministrableProduct] = []
    medicalDevices: List[MedicalDevice] = []
    productOrganizationRoles: List[ProductOrganizationRole] = []
    biomedicalConcepts: List[BiomedicalConcept] = []
    bcCategories: List[BiomedicalConceptCategory] = []
    bcSurrogates: List[BiomedicalConceptSurrogate] = []
    dictionaries: List[SyntaxTemplateDictionary] = []
    conditions: List[Condition] = []
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
            if org and org.type.code == "C54149":
                return identifier
        return None

    #  Now in StudyDesign
    #  def phase(self):
    #    return self.studyPhase.standardCode

    def organization(self, id: str) -> Organization:
        return next((x for x in self.organizations if x.id == id), None)
