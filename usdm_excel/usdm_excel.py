from usdm_excel.id_manager import IdManager
from usdm_excel.study_sheet.study_sheet import StudySheet

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

  # def to_json(self):
  #   return self.export_node(self.study.the_study())

  # def export_node(self, node):
  #   if type(node) == list:
  #     result = []
  #     for item in node:
  #       result.append(self.export_node(item))
  #     return result
  #   elif type(node) == dict:
  #     result = {}
  #     for key, value in node.items():
  #       if key.startswith('_'):
  #         continue
  #       result[key] = self.export_node(value)
  #     return result
  #   else:
  #     return node

  def the_study(self):
    return self.study.the_study()