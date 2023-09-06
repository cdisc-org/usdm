from .api_base_model import ApiBaseModelWithId

class Code(ApiBaseModelWithId):
  code: str
  codeSystem: str
  codeSystemVersion: str
  decode: str
