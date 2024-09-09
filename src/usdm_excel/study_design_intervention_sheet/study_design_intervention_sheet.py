from usdm_excel.base_sheet import BaseSheet
from usdm_excel.alias import Alias
from usdm_model.study_intervention import StudyIntervention
from usdm_model.administration import Administration
from usdm_model.administration_duration import AdministrationDuration
from usdm_excel.globals import Globals

class StudyDesignInterventionSheet(BaseSheet):

  SHEET_NAME = 'studyDesignInterventions'

  def __init__(self, file_path: str, globals: Globals):
    try:
      self.items = []
      super().__init__(file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME)
      self.current_name = None
      self.current_intervention = None
      for index, row in self.sheet.iterrows():
        admin_duration = self._create_administration_duration(index)
        agent_admin = self._create_administration(index, admin_duration)
        self._create_intervention(index, agent_admin)
    except Exception as e:
      self._sheet_exception(e)

  def _create_intervention(self, index, agent_admin):
    name = self.read_cell_by_name(index, 'name')
    if name and name != self.current_name:
      self.current_name = name
      params = {
        'name': name,
        'description': self.read_cell_by_name(index, 'description', must_be_present=False),
        'label': self.read_cell_by_name(index, 'label', must_be_present=False),
        'codes': self.read_other_code_cell_multiple_by_name(index, "codes"),
        'role': self.read_cdisc_klass_attribute_cell_by_name("StudyIntervention", "role", index, "role"),
        'type': self.read_cdisc_klass_attribute_cell_by_name("StudyIntervention", "type", index, "type"),
        'productDesignation': self.read_cdisc_klass_attribute_cell_by_name("StudyIntervention", "productDesignation", index, "productDesignation"),
        'minimumResponseDuration': self.read_quantity_cell_by_name(index, "minimumResponseDuration"),
        'administrations': [agent_admin]
      }
      item = self.create_object(StudyIntervention, params)
      if item:
        self.current_intervention = item
        self.items.append(item)
        self.globals.cross_references.add(name, item)
    else:
      self.current_intervention.administrations.append(agent_admin)

  def _create_administration(self, index, admin_duration):
    params = {
      'name': self.read_cell_by_name(index, 'administrationName'), 
      'description': self.read_cell_by_name(index, 'administrationDescription', must_be_present=False), 
      'label': self.read_cell_by_name(index, 'administrationLabel', must_be_present=False),
      'duration': admin_duration,
      'dose': self.read_quantity_cell_by_name(index, "administrationDose"),
      'route': Alias(self.globals).code(self.read_cdisc_klass_attribute_cell_by_name("Administration", "route", index, "administrationRoute"), []),
      'frequency': Alias(self.globals).code(self.read_cdisc_klass_attribute_cell_by_name("Administration", "frequency", index, "administrationFrequency"), [])
    }
    item = self.create_object(Administration, params)
    if item:
      self.globals.cross_references.add(item.name, item)
    return item
    
  def _create_administration_duration(self, index):
    params = {
      'description': self.read_cell_by_name(index, 'administrationDurationDescription', must_be_present=False),
      'durationWillVary': self.read_boolean_cell_by_name(index, 'administrationDurationWillVary'),
      'reasonDurationWillVary': self.read_cell_by_name(index, 'administrationDurationWillVaryReason'),
      'quantity': self.read_quantity_cell_by_name(index, 'administrationDurationQuantity')
    }
    return self.create_object(AdministrationDuration, params)
