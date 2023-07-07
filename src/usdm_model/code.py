from .api_base_model import ApiIdModel

class Code(ApiIdModel):
  code: str
  codeSystem: str
  codeSystemVersion: str
  decode: str
