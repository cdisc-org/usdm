from .api_base_model import ApiBaseModel

class Code(ApiBaseModel):
  codeId: str
  code: str
  codeSystem: str
  codeSystemVersion: str
  decode: str

