from usdm_excel.option_manager import option_manager
from usdm_excel.ct_version_manager import ct_version_manager
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
from usdm_excel.errors.errors import error_manager

def clear():
  option_manager.clear()
  ct_version_manager.clear()
  id_manager.clear()
  cross_references.clear()
  ct_version_manager.clear()
  error_manager.clear()
