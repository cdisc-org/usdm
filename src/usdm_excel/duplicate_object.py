from usdm_model.api_base_model import ApiBaseModelWithId
from usdm_excel.globals import Globals
from usdm_model import *


def duplicate_object(item: ApiBaseModelWithId, globals: Globals) -> object:
    try:
        return duplicate_klass(item.model_dump(), globals)
    except Exception as e:
        return None


def duplicate_klass(item: dict, globals: Globals) -> ApiBaseModelWithId:
    cls = eval(item["instanceType"])
    for k, v in item.items():
        if k == "id":
            item["id"] = globals.id_manager.build_id(cls)
        elif k == "instanceType":
            pass
        elif isinstance(v, list):
            for index, x in enumerate(v):
                v[index] = duplicate_klass(x, globals)
            item[k] = v
        elif isinstance(v, dict):
            item[k] = duplicate_klass(v, globals)
    return cls(**item)
