import logging
from usdm_excel.id_manager import IdManager
from usdm_excel.cross_ref import CrossRef
from usdm_excel.ct_version_manager import CTVersionManager
from usdm_excel.errors.errors import Errors
from usdm_excel.option_manager import OptionManager
from usdm_excel.cdisc_ct_library import CDISCCTLibrary

class Managers():

  def __init__(self):
    self.logger = logging.getLogger(__name__)
    self.logger.addHandler(logging.NullHandler())
    self.errors = Errors()
    self.id_manager = IdManager()
    self.ct_version_manager = CTVersionManager()
    self.option_manager = OptionManager()
    self.cross_references = CrossRef()
    self.cdisc_ct_library = CDISCCTLibrary(self.errors, self.logger)


