import json
import os
from usdm_excel.globals import Globals
from usdm_excel.code_base import CodeBase


class ISO3166(CodeBase):
    def __init__(self, globals: Globals):
        super().__init__(globals)
        f = open(os.path.join(os.path.dirname(__file__), "data", "iso_3166.json"))
        self.db = json.load(f)

    def code(self, code):
        code, decode = self._get_decode(code)
        return self._build(
            code=code, system="ISO 3166 1 alpha3", version="2020-08", decode=decode
        )

    def region_code(self, decode):
        code, decode = self._get_region_decode(decode)
        return self._build(
            code=code, system="ISO 3166 1 alpha3", version="2020-08", decode=decode
        )

    def _get_decode(self, code):
        if len(code) == 2:
            field = "alpha-2"
        else:
            field = "alpha-3"
        entry = next((item for item in self.db if item[field] == code), None)
        if entry == None:
            return "DNK", "Denmark"
        else:
            return entry["alpha-3"], entry["name"]

    def _get_region_decode(self, decode):
        for scope in ["region", "sub-region", "intermediate-region"]:
            entry = next(
                (item for item in self.db if item[scope].upper() == decode.upper()),
                None,
            )
            if entry:
                return entry[f"{scope}-code"], entry[scope]
        return "150", "Europe"
