from pydantic import BaseModel
from usdm_db.document.utility import *
from usdm_db.errors_and_logging.errors_and_logging import ErrorsAndLogging

class ClassA(BaseModel):
  id: str

errors_and_logging = ErrorsAndLogging()

def test_usdm_reference():
  a = ClassA(id='123')
  ref = usdm_reference(a, 'attribute')
  assert ref == '<usdm:ref klass="ClassA" id="123" attribute="attribute"></usdm:ref>'
  

# def test_get_soup():
#   result = get_soup('', errors_and_logging)
#   assert result == ''
