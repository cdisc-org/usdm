import logging
from usdm_excel.id_manager import IdManager
from usdm_excel.cross_ref import CrossRef
from usdm_excel.ct_version_manager import CTVersionManager
from usdm_excel.errors.errors import Errors
from usdm_excel.option_manager import OptionManager
from usdm_excel.cdisc_ct_library import CDISCCTLibrary
from usdm_excel.cdisc_bc_library import CDISCBCLibrary

class Globals():

  def __init__(self):
    self.logger = None
    self.errors = None
    self.id_manager = None
    self.ct_version_manager = None
    self.option_manager = None
    self.cross_references = None
    self.cdisc_ct_library = None
    self.cdisc_bc_library = None

  def create(self):
    self.logger = logging.getLogger(__name__)
    self.logger.addHandler(logging.NullHandler())
    self.errors = Errors(self.logger)
    self.id_manager = IdManager(self.logger)
    self.ct_version_manager = CTVersionManager(self.logger)
    self.option_manager = OptionManager(self.logger)
    self.cross_references = CrossRef(self.errors, self.logger)
    self.cdisc_ct_library = CDISCCTLibrary(self.errors, self.logger)
    self.cdisc_bc_library = CDISCBCLibrary(self.errors, self.logger, self.cdisc_ct_library, self.id_manager)

