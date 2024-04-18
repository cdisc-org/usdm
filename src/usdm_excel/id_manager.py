from usdm_excel.errors_and_logging.errors_and_logging import ErrorsAndLogging

class IdManager():

  def __init__(self, errors_and_logging: ErrorsAndLogging):
    self._errors_and_logging = errors_and_logging
    self._id_index = {}
    self.clear()

  def clear(self):
    self._id_index = {
      'Address': 0,
      'Code': 0,
      'AliasCode': 0,
      'Organization': 0,
      'StudyIdentifier': 0,
      'StudyEpoch': 0,
      'StudyArm': 0,
      'StudyCell': 0,
      'Entry': 0, 
      'ScheduleTimelineExit': 0, 
      'ScheduledActivityInstance': 0,
      'ScheduledDecisionInstance': 0,
      'ScheduleTimeline': 0, 
      'Timing': 0, 
      'StudyDesign': 0, 
      'Study': 0, 
      'StudyVersion': 0, 
      'Activity': 0, 
      'Encounter': 0, 
      'BiomedicalConceptSurrogate': 0, 
      'BiomedicalConcept': 0,
      'BiomedicalConceptProperty': 0,
      'ResponseCode': 0,
      'StudyIntervention': 0,
      'Indication': 0,
      'StudyDesignPopulation': 0,
      'Objective': 0,
      'Endpoint': 0,
      'IntercurrentEvent': 0,
      'Estimand': 0,
      'AnalysisPopulation': 0,
      'StudyProtocolDocumentVersion': 0,
      'StudyProtocolDocument': 0,
      'Procedure': 0,
      'TransitionRule': 0,
      'StudyElement': 0,
      'NarrativeContent': 0,
      'GovernanceDate': 0,
      'GeographicScope': 0,
      'StudyAmendment': 0,
      'StudyAmendmentReason': 0,
      'SubjectEnrollment': 0,
      'SyntaxTemplateDictionary': 0,
      'EligibilityCriterion': 0,
      'AgentAdministration': 0,
      'AdministrationDuration': 0,
      'Quantity': 0,
      'Range': 0,
      'StudyCohort': 0,
      'StudyTitle': 0,
      'Masking': 0,
      'ResearchOrganization': 0,
      'StudySite': 0,
      'Condition': 0,
      'ParameterMap': 0,
      'ConditionAssignment': 0,
      'Characteristic': 0
    }

  def build_id(self, klass):
    klass_name = klass if isinstance(klass, str) else str(klass.__name__)
    self._id_index[klass_name] += 1
    return f"{klass_name}_{self._id_index[klass_name]}"


