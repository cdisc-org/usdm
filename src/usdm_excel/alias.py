from usdm_excel.id_manager import id_manager
from usdm_model.alias_code import AliasCode

class Alias():

  @classmethod
  def code(self, standard_code, aliases):
    return AliasCode(id=self.managers.id_manager.build_id(AliasCode), standardCode=standard_code, standardCodeAliases=aliases) if standard_code else None