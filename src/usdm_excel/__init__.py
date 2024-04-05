import json
import traceback
#from usdm_excel.id_manager import id_manager
from usdm_excel.configuration_sheet import ConfigurationSheet
from usdm_excel.study_sheet.study_sheet import StudySheet
# from usdm_excel.export_as_yworks_dict import ExportAsYworksDict
# from usdm_excel.export_as_neo4j_dict import ExportAsNeo4jDict
# from usdm_excel.export_as_timeline import ExportAsTimeline
#from usdm_excel.cross_ref import cross_references
#from usdm_excel.ct_version_manager import ct_version_manager
#from usdm_excel.errors.errors import error_manager, Errors
#from usdm_excel.option_manager import option_manager as om # Using 'om' as a name clash in pytest
#from usdm_excel.cdisc_biomedical_concept import cdisc_bc_library
from usdm_excel.managers import Managers
from usdm_model.wrapper import Wrapper
from usdm_info import __model_version__ as usdm_version, __package_version__ as system_version

class USDMExcel():

  def __init__(self, file_path, manager):
    # id_manager.clear()
    # self.managers.cross_references.clear()
    # ct_version_manager.clear()
    # self.managers.errors.clear()
    # om.clear()
    # #self.configuration = ConfigurationSheet(file_path, self.manager)
    self.managers = Managers()
    self.study = StudySheet(file_path, self.managers)
    self.wrapper = Wrapper(study=self._excel.study, usdmVersion=usdm_version, systemName=self.SYSTEM_NAME, systemVersion=system_version)

  # def identifier(self):
  #   study = self.study.the_study()
  #   if study == None:
  #     return None
  #   else:
  #     return study.study_identifier()

  # def the_study(self):
  #   return self.study.the_study()
  
  # def to_json(self):
  #   try:
  #     raw_json = self.study.api_root().to_json()
  #   except Exception as e:
  #     message = f"Failed to generate JSON output, exception {e}\n{traceback.format_exc()}"
  #     self.managers.errors.add(None, None, None, message)
  #     raw_json = json.dumps({'error': message}, indent = 2)
  #   return raw_json

  # def to_html(self, highlight=False):
  #   try:
  #     html = self.study.to_html(highlight)
  #   except Exception as e:
  #     message = f"Failed to generate HTML output, exception {e}"
  #     self.managers.errors.add(None, None, None, message)
  #     html = f"<p>{message}</p>"
  #   return html

  # def to_pdf(self, test=True):
  #   try:
  #     bytes = self.study.to_pdf(test)
  #   except Exception as e:
  #     message = f"Failed to generate PDF output, exception {e}"
  #     self.managers.errors.add(None, None, None, message)
  #     bytes = bytearray()
  #     bytes.extend(map(ord, message))    
  #   return bytes

  # def to_nodes_and_edges(self, view=FULL_VIEW):
  #   return ExportAsYworksDict(self.study.the_study(), view).export()

  # def to_yworks_dict(self, view=FULL_VIEW):
  #   return ExportAsYworksDict(self.study.the_study(), view).export()

  # def to_neo4j_dict(self):
  #   return ExportAsNeo4jDict(self.study.the_study()).export()

  # def to_timeline(self, level=FULL_HTML):
  #   return ExportAsTimeline(self.study.the_study()).export(level)

  def errors(self):
    return self.managers.errors.dump(Errors.WARNING)