from pydantic import BaseModel
from usdm_db.cross_reference import CrossReference
from usdm_db.errors_and_logging.errors_and_logging import ErrorsAndLogging

class CRTest():

  def __init__(self, id, name):
    self.id = id
    self.name = name
    self.value = "VALUE"

class Study(BaseModel):
  id: str

study = Study(id="1")
errors_and_logging = ErrorsAndLogging()
cross_references = CrossReference(study, errors_and_logging)

def test_create():
  object = CrossReference(study, errors_and_logging)
  assert len(object._references.keys()) == 0
  assert object._references == {}

def test_get():
  item = CRTest(id="1234", name="name")
  cross_references._references = {}
  assert len(cross_references._references.keys()) == 0
  cross_references._references["CRTest.name"] = item
  assert cross_references.get(CRTest, "name") == item

