import logging
from usdm_excel.id_manager import IdManager
from usdm_excel.cross_ref import CrossRef
from usdm_excel.ct_version_manager import CTVersionManager
from usdm_excel.errors.errors import Errors
from usdm_excel.option_manager import OptionManager
from usdm_excel.cdisc_ct_library import CDISCCTLibrary
from usdm_excel.cdisc_biomedical_concept import CDISCBiomedicalConcepts

class Managers():

  def __init__(self):
    self.logger = logging.getLogger(__name__)
    self.logger.addHandler(logging.NullHandler())
    self.errors = Errors(self.logger)
    self.id_manager = IdManager(self.logger)
    self.ct_version_manager = CTVersionManager(self.logger)
    self.option_manager = OptionManager(self.logger)
    self.cross_references = CrossRef(self.errors, self.logger)
    self.cdisc_ct_library = CDISCCTLibrary(self.errors, self.logger)
    cdisc_bc_library = CDISCBiomedicalConcepts(self.errors, self.logger)


