from typing import Literal
from .api_base_model import ApiBaseModelWithId
from .organization import Organization
from .code import Code

class Identifier(ApiBaseModelWithId):
  text: str
  scope: Organization
  instanceType: Literal['Identifier']

class ReferenceIdentifier(Identifier):
  type: Code
  instanceType: Literal['ReferenceIdentifier']

class StudyIdentifier(Identifier):
  instanceType: Literal['StudyIdentifier']
