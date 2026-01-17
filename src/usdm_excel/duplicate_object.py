from usdm_model.api_base_model import ApiBaseModelWithId
from usdm_excel.globals import Globals
from usdm_excel.utility import build_unique_name
from usdm_model import *


def duplicate_object(item: ApiBaseModelWithId, globals: Globals) -> object:
    try:
        return duplicate_klass(item.model_dump(), globals)
    except Exception as e:
        print(f"DUP: {e}")
        return None


def duplicate_klass(item: dict, globals: Globals, prefix: str | None = None) -> ApiBaseModelWithId:
    cls = eval(item["instanceType"])
    for k, v in item.items():
        if k == "id":
            item["id"] = globals.id_manager.build_id(cls)
            if "name" in item:
                item["name"], prefix = build_unique_name(item["name"], item["id"], prefix)
        elif k == "instanceType":
            pass
        elif isinstance(v, list):
            for index, x in enumerate(v):
                v[index] = duplicate_klass(x, globals, prefix)
            item[k] = v
        elif isinstance(v, dict):
            item[k] = duplicate_klass(v, globals, prefix)
    return cls(**item)
