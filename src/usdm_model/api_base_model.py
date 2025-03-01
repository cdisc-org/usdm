import json
import enum
import datetime
from uuid import UUID
from typing import Union, List
from pydantic import BaseModel, Field
from .extension import ExtensionAttribute


# Example, see https://stackoverflow.com/questions/10252010/serializing-class-instance-to-json
def _serialize_as_json(obj):
    if isinstance(obj, enum.Enum):
        return obj.value
    elif isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, UUID):
        return str(obj)
    else:
        return obj.__dict__


def _serialize_as_json_with_type(obj):
    if isinstance(obj, enum.Enum):
        return obj.value
    elif isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, UUID):
        return str(obj)
    else:
        result = obj.__dict__
        result["_type"] = obj.__class__.__name__
        return result


class ApiBaseModel(BaseModel):
    def __init__(self, *args, **kwargs):
        kwargs["instanceType"] = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def to_json(self):
        return json.dumps(self, default=_serialize_as_json)

    def to_json_with_type(self):
        return json.dumps(self, default=_serialize_as_json_with_type)


class ApiBaseModelWithIdOnly(ApiBaseModel):
    id: str = Field(min_length=1)


class ApiBaseModelWithId(ApiBaseModelWithIdOnly):
    extensionAttributes: List[ExtensionAttribute] = []


class ApiBaseModelWithIdAndDesc(ApiBaseModelWithId):
    description: Union[str, None] = None


class ApiBaseModelWithIdAndName(ApiBaseModelWithId):
    name: str = Field(min_length=1)


class ApiBaseModelWithIdNameAndLabel(ApiBaseModelWithIdAndName):
    label: Union[str, None] = None


class ApiBaseModelWithIdNameLabelAndDesc(ApiBaseModelWithIdNameAndLabel):
    description: Union[str, None] = None


class ApiBaseModelWithIdNameAndDesc(ApiBaseModelWithIdAndName):
    description: Union[str, None] = None
