from usdm_excel.id_manager import IdManager
from usdm_excel.cross_ref import CrossRef
from usdm_excel.ct_version_manager import CTVersionManager
from usdm_excel.template_manager import TemplateManager
from usdm_excel.errors_and_logging.errors_and_logging import ErrorsAndLogging
from usdm_excel.option_manager import OptionManager
from usdm_excel.cdisc_ct_library import CDISCCTLibrary
from usdm_excel.cdisc_bc_library import CDISCBCLibrary


class Globals:
    def __init__(self):
        self.errors_and_logging = None
        self.id_manager = None
        self.ct_version_manager = None
        self.template_manager = None
        self.option_manager = None
        self.cross_references = None
        self.cdisc_ct_library = None
        self.cdisc_bc_library = None

    def create(self):
        self.errors_and_logging = ErrorsAndLogging()
        self.id_manager = IdManager(self.errors_and_logging)
        self.ct_version_manager = CTVersionManager(self.errors_and_logging)
        self.template_manager = TemplateManager(self.errors_and_logging)
        self.option_manager = OptionManager(self.errors_and_logging)
        self.cross_references = CrossRef(self.errors_and_logging)
        self.cdisc_ct_library = CDISCCTLibrary(self.errors_and_logging)
        self.cdisc_bc_library = CDISCBCLibrary(
            self.errors_and_logging, self.cdisc_ct_library, self.id_manager
        )
