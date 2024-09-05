import traceback
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
        # Read the adminstrations and durations
        admin_duration = self._create_administration_duration(index)
        agent_admin = self._create_agent_administration(index, admin_duration)
        # Read intervention in present
        self._create_intervention(index, agent_admin)
    except Exception as e:
      self._sheet_exception(e)

  def _create_intervention(self, index, agent_admin):
    name = self.read_cell_by_name(index, 'name')
    if name and name != self.current_name:
      self.current_name = name
      description = self.read_cell_by_name(index, 'description', must_be_present=False)
      label = self.read_cell_by_name(index, 'label', must_be_present=False)
      codes = self.read_other_code_cell_multiple_by_name(index, "codes")
      role = self.read_cdisc_klass_attribute_cell_by_name("StudyIntervention", "role", index, "role")
      type = self.read_cdisc_klass_attribute_cell_by_name("StudyIntervention", "type", index, "type")
      pharm_class = self.read_other_code_cell_by_name(index, "pharmacologicalClass")
      product_designation = self.read_cdisc_klass_attribute_cell_by_name("StudyIntervention", "productDesignation", index, "productDesignation")
      min_duration =self.read_quantity_cell_by_name(index, "minimumResponseDuration")
      self.current_intervention = self._intervention(name, description, label, role, codes, type, pharm_class, product_designation, min_duration, agent_admin)
    else:
      self.current_intervention.administrations.append(agent_admin)

  def _intervention(self, name, description, label, role, codes, type, pharm_class, product_designation, minimum_duration, agent_administration):
    try:
      item = StudyIntervention(
        id=self.globals.id_manager.build_id(StudyIntervention), 
        name=name, 
        description=description, 
        label=label,
        role=role,
        type=type,
        minimumResponseDuration=minimum_duration,
        codes=codes,
        productDesignation=product_designation,
        pharmacologicClass=pharm_class,
        administrations=[agent_administration]
      )
    except Exception as e:
      self._general_error(f"Failed to create StudyIntervention object", e)
    else:
      self.items.append(item)
      self.globals.cross_references.add(name, item)
      return item    

  def _create_agent_administration(self, index, admin_duration):
    name = self.read_cell_by_name(index, 'administrationName')
    descriptiopn = self.read_cell_by_name(index, 'administrationDescription', must_be_present=False)
    label = self.read_cell_by_name(index, 'administrationLabel', must_be_present=False)
    route = self.read_cdisc_klass_attribute_cell_by_name("Administration", "route", index, "administrationRoute")
    dose = self.read_quantity_cell_by_name(index, "administrationDose")
    frequency = self.read_cdisc_klass_attribute_cell_by_name("Administration", "frequency", index, "administrationFrequency")
    return self._agent_administration(name, descriptiopn, label, route, dose, frequency, admin_duration)

  def _agent_administration(self, name, description, label, route, dose, frequency, admin_duration):
    try:
      item = Administration(
        id=self.globals.id_manager.build_id(Administration), 
        name=name, 
        description=description, 
        label=label,
        duration=admin_duration,
        dose=dose,
        route=Alias(self.globals).code(route, []),
        frequency=Alias(self.globals).code(frequency, [])
      )
    except Exception as e:
      self._general_error(f"Failed to create Administration object", e)
    else:
      self.globals.cross_references.add(name, item)
      return item

  def _create_administration_duration(self, index):
    description = self.read_cell_by_name(index, 'administrationDurationDescription', must_be_present=False)
    will_vary = self.read_boolean_cell_by_name(index, 'administrationDurationWillVary')
    will_vary_reason = self.read_cell_by_name(index, 'administrationDurationWillVaryReason')
    quantity = self.read_quantity_cell_by_name(index, 'administrationDurationQuantity')
    return self._administration_duration(description, will_vary, will_vary_reason, quantity)

  def _administration_duration(self, description, will_vary, will_vary_reason, quantity):
    try:
      item = AdministrationDuration(
        id=self.globals.id_manager.build_id(AdministrationDuration), 
        description=description,
        durationWillVary=will_vary,
        reasonDurationWillVary=will_vary_reason,
        quantity=quantity
      )
    except Exception as e:
      self._general_error(f"Failed to create AdministrationDuration object", e)
    else:
      return item
