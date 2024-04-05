from usdm_excel.base_sheet import BaseSheet
from usdm_excel.alias import Alias
#from usdm_excel.cross_ref import cross_references
#from usdm_excel.id_manager import id_manager
import traceback

from usdm_model.study_intervention import StudyIntervention
from usdm_model.agent_administration import AgentAdministration
from usdm_model.administration_duration import AdministrationDuration

class StudyDesignInterventionSheet(BaseSheet):

  def __init__(self, file_path, manager):
    try:
      super().__init__(file_path=file_path, manager=manager, sheet_name='studyDesignInterventions')
      self.items = []
      self.current_name = None
      self.current_intervention = None
      for index, row in self.sheet.iterrows():
        # Read the adminstrations and durations
        admin_duration = self._create_administration_duration(index)
        agent_admin = self._create_agent_administration(index, admin_duration)
        # Read intervention in present
        self._create_intervention(index, agent_admin)
    except Exception as e:
      self._general_error(f"Exception '{e}' raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

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
        id=self.managers.id_manager.build_id(StudyIntervention), 
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
      self._general_error(f"Failed to create StudyIntervention object, exception {e}")
      self._traceback(f"{traceback.format_exc()}")
    else:
      self.items.append(item)
      self.managers.cross_references.add(name, item)
      return item    

  def _create_agent_administration(self, index, admin_duration):
    name = self.read_cell_by_name(index, 'administrationName')
    descriptiopn = self.read_cell_by_name(index, 'administrationDescription', must_be_present=False)
    label = self.read_cell_by_name(index, 'administrationLabel', must_be_present=False)
    route = self.read_cdisc_klass_attribute_cell_by_name("AgentAdministration", "route", index, "administrationRoute")
    dose = self.read_quantity_cell_by_name(index, "administrationDose")
    frequency = self.read_cdisc_klass_attribute_cell_by_name("AgentAdministration", "frequency", index, "administrationFrequency")
    return self._agent_administration(name, descriptiopn, label, route, dose, frequency, admin_duration)

  def _agent_administration(self, name, description, label, route, dose, frequency, admin_duration):
    try:
      item = AgentAdministration(
        id=self.managers.id_manager.build_id(AgentAdministration), 
        name=name, 
        description=description, 
        label=label,
        duration=admin_duration,
        dose=dose,
        route=Alias.code(route, []),
        frequency=Alias.code(frequency, [])
      )
    except Exception as e:
      self._general_error(f"Failed to create AgentAdministration object, exception {e}")
      self._traceback(f"{traceback.format_exc()}")
    else:
      self.managers.cross_references.add(name, item)
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
        id=self.managers.id_manager.build_id(AdministrationDuration), 
        description=description,
        durationWillVary=will_vary,
        reasonDurationWillVary=will_vary_reason,
        quantity=quantity
      )
    except Exception as e:
      self._general_error(f"Failed to create AdministrationDuration object, exception {e}")
      self._traceback(f"{traceback.format_exc()}")
    else:
      return item
