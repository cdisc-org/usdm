import pandas as pd
from usdm_excel.base_sheet import BaseSheet
from usdm_model.code import Code
from usdm_model.alias_code import AliasCode


class Factory:
    def __init__(self, globals):
        self.globals = globals

    def item(self, cls, params):
        params["id"] = (
            params["id"] if "id" in params else self.globals.id_manager.build_id(cls)
        )
        params["instanceType"] = cls.__name__
        return cls(**params)

    def set(self, cls, item_list):
        results = []
        for item in item_list:
            results.append(self.item(cls, item))
        return results

    def base_sheet(self, mocker):
        mocked_open = mocker.mock_open(read_data="File")
        mocker.patch("builtins.open", mocked_open)
        data = []
        mock_read = mocker.patch("pandas.read_excel")
        mock_read.return_value = pd.DataFrame(data, columns=[])
        return BaseSheet("", self.globals, "")

    def code(self, code, decode):
        return self._build_code(code=code, system="yyy", version="2", decode=decode)

    def geo_code(self, code, decode):
        return self._build_code(
            code=code, system="ISO 3166 1 alpha3", version="2020-08", decode=decode
        )

    def cdisc_code(self, code, decode):
        return self._build_code(code=code, system="xxx", version="1", decode=decode)

    def english(self):
        return self._build_code(
            code="en", system="ISO639", version="2007", decode="English"
        )

    def cdisc_dummy(self):
        return self.cdisc_code("C12345", "decode")

    def alias_code(self, standard_code, alias_codes=[]):
        return self.item(
            AliasCode,
            {"standardCode": standard_code, "standardCodeAliases": alias_codes},
        )

    def _build_code(self, code, system, version, decode):
        return self.item(
            Code,
            {
                "code": code,
                "codeSystem": system,
                "codeSystemVersion": version,
                "decode": decode,
            },
        )
