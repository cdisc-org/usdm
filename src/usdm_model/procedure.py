from typing import Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .code import Code

class Procedure(ApiBaseModelWithIdNameLabelAndDesc):
  procedureType: str
  code: Code
  studyInterventionId: Union[str, None] = None
  instanceType: Literal['Procedure'] = 'Procedure'
