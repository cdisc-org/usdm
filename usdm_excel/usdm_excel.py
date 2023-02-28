from usdm_excel.id_manager import IdManager
from usdm_excel.study_sheet.study_sheet import StudySheet
from usdm_excel.nodes_and_edges import NodesAndEdges

class USDMExcel():

  def __init__(self, file_path):
    self.id_manager = IdManager()
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
