from usdm_excel.id_manager import IdManager
from usdm.alias_code import AliasCode

class Alias():

  def __init__(self, id_manager: IdManager):
    self.id_manager = id_manager

  def code(self, standard_code, aliases):
    return AliasCode(aliasCodeId=self.id_manager.build_id(AliasCode), standardCode=standard_code, standardCodeAliases=aliases)