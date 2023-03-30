from pydantic import BaseModel
import json
import enum
import datetime

def _serialize_as_json(obj):
  #print("OBJ:", type(obj))
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

  def to_json(self):
    return json.dumps(self, default=_serialize_as_json)

  def to_json_with_type(self):
    return json.dumps(self, default=_serialize_as_json_with_type)

