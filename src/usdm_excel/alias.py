from usdm_excel.globals import Globals
from usdm_model.alias_code import AliasCode


class Alias:
    def __init__(self, globals: Globals):
        self._globals = globals

    def code(self, standard_code, aliases):
        return (
            AliasCode(
                id=self._globals.id_manager.build_id(AliasCode),
                standardCode=standard_code,
                standardCodeAliases=aliases,
            )
            if standard_code
            else None
        )
