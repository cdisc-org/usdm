from .api_base_model import ApiBaseModel

class Code(ApiBaseModel):
  code: str
  codeSystem: str
  codeSystemVersion: str
  decode: str
