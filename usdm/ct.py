import yaml
from .api_base_model import ApiBaseModel
from fastapi import HTTPException

class CT(ApiBaseModel):

  def search(self, klass_name, attribute_name):
    with open("data/ct.yaml") as file:
      try:
        ct = yaml.load(file, Loader=yaml.FullLoader)
        data = ct[klass_name][attribute_name]
        return data
      except:
        raise HTTPException(status_code=404, detail="Item not found")
