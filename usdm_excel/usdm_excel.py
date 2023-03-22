from usdm_excel.id_manager import IdManager
from usdm_excel.configuration_sheet import ConfigurationSheet
from usdm_excel.study_sheet.study_sheet import StudySheet
from usdm_excel.nodes_and_edges import NodesAndEdges
from usdm_excel.cross_ref import cross_references
from usdm_excel.ct_version_manager import ct_version_manager

class USDMExcel():

  def __init__(self, file_path):
    self.id_manager = IdManager()
    cross_references.clear()
    ct_version_manager.clear()
    self.configuration = ConfigurationSheet(file_path, self.id_manager)
    self.study = StudySheet(file_path, self.id_manager)

  def identifier(self):
    study = self.study.the_study()
    if study == None:
      return None
    else:
      return study.study_identifier()

  def the_study(self):
    return self.study.the_study()
  
  def to_json(self):
    return self.study.the_study().to_json()

  def to_nodes_and_edges(self):
    return NodesAndEdges(self.study.the_study()).nodes_and_edges()
