from pydantic import BaseModel, constr
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

  #IdField = constr(min_length=1)
  #NameField = constr(min_length=1)
  
  def to_json(self):
    return json.dumps(self, default=_serialize_as_json)

  def to_json_with_type(self):
    return json.dumps(self, default=_serialize_as_json_with_type)

class ApiBaseModelWithId(ApiBaseModel):
  id: constr(min_length=1)

class ApiBaseModelWithIdAndDesc(ApiBaseModelWithId):
  description: Union[str, None] = None

class ApiBaseModelWithIdAndName(ApiBaseModelWithId):
  name: constr(min_length=1)

class ApiBaseModelWithIdNameAndLabel(ApiBaseModelWithIdAndName):
  label: Union[str, None] = None

class ApiBaseModelWithIdNameLabelAndDesc(ApiBaseModelWithIdNameAndLabel):
  description: Union[str, None] = None

class ApiBaseModelWithIdNameAndDesc(ApiBaseModelWithIdAndName):
  description: Union[str, None] = None
