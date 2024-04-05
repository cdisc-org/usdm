from usdm_excel.id_manager import IdManager
from usdm_excel.cross_ref import CrossRef
from usdm_excel.ct_version_manager import CTVersionManager
from usdm_excel.errors.errors import Errors
from usdm_excel.option_manager import OptionManager

class Managers():

  def __init__(self):
    self.id_manager = IdManager()
    self.ct_version_manager = CTVersionManager()
    self.option_manager = OptionManager()
    self.cross_references = CrossRef()
    self.errors = Errors()


