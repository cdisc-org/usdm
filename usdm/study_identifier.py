from typing import Union
from uuid import UUID
from .api_base_model import ApiBaseModel
from .organisation import Organisation

class StudyIdentifier(ApiBaseModel):
  studyIdentifierId: str
  studyIdentifier: str
  studyIdentifierScope: Organisation

  @classmethod
  def scope_reuse(cls):
    return True

  @classmethod
  def search(cls, store, study_uuid):
    results = []
    items = store.get_by_klass_and_scope(cls.__name__, study_uuid)
    #print("IDENTIFIERS:", items)
    for item in items:
      results.append(cls.recursive_read(store, item['uuid']))
    return results

