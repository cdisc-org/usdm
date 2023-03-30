from .api_base_model import ApiBaseModel

class IntercurrentEvent(ApiBaseModel):
  intercurrentEventId: str
  intercurrentEventName: str
  intercurrentEventDescription: str
  intercurrentEventStrategy: str
