from pydantic import BaseModel
import json

def _serialize_as_json(obj):
  return obj.__dict__

def _serialize_as_yworks(obj):
  # Example, see https://stackoverflow.com/questions/10252010/serializing-class-instance-to-json
  result = obj.__dict__
  result['_type'] = obj.__class__.__name__
  return result

class ApiBaseModel(BaseModel):

  def to_json(self):
    return json.dumps(self, default=_serialize_as_json)

  def to_yworks(self):
    return json.dumps(self, default=_serialize_as_yworks)

