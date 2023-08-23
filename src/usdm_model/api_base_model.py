from pydantic import BaseModel, Field, constr
from typing import Union
import json
import enum
import datetime

def _serialize_as_json(obj):
  if isinstance(obj, enum.Enum):
    return obj.value
  elif isinstance(obj, datetime.date):
    return obj.isoformat()
  else:
    return obj.__dict__

def _serialize_as_json_with_type(obj):
  # Example, see https://stackoverflow.com/questions/10252010/serializing-class-instance-to-json
  if isinstance(obj, enum.Enum):
    return obj.value
  elif isinstance(obj, datetime.date):
    return obj.isoformat()
  else:
    result = obj.__dict__
    result['_type'] = obj.__class__.__name__
    return result


class ApiBaseModel(BaseModel):

  IdField = Field(min_length=1)
  NameField = Field(min_length=1)
  DescriptionField = Union[constr(), None] = None

  def to_json(self):
    return json.dumps(self, default=_serialize_as_json)

  def to_json_with_type(self):
    return json.dumps(self, default=_serialize_as_json_with_type)

class ApiIdModel(ApiBaseModel):
  id: ApiBaseModel.IdField

class ApiNameDescriptionModel(ApiIdModel):
  name: ApiBaseModel.NameField
  description: ApiBaseModel.DescriptionField

class ApiDescriptionModel(ApiIdModel):
  description: ApiBaseModel.DescriptionField

class ApiNameModel(ApiIdModel):
  name: ApiBaseModel.NameField
