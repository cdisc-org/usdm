from usdm_excel.id_manager import id_manager
from usdm_model.alias_code import AliasCode

class Alias():

  def code(self, standard_code, aliases):
    return AliasCode(id=id_manager.build_id(AliasCode), standardCode=standard_code, standardCodeAliases=aliases)