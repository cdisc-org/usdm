from usdm_excel.managers import Managers
from usdm_model.alias_code import AliasCode

class Alias():

  def __init__(self, managers: Managers):
    self._managers = managers

  def code(self, standard_code, aliases):
    return AliasCode(id=self._managers.id_manager.build_id(AliasCode), standardCode=standard_code, standardCodeAliases=aliases) if standard_code else None