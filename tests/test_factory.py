from src.usdm_excel.id_manager import id_manager

class Factory():
  
  def item(self, cls, params):
    params['id'] = id_manager.build_id(cls)
    params['instanceType'] = cls.__name__
    return cls(**params)

  def set(self, cls, item_list):
    results = []
    for item in item_list:
      results.append(self.item(cls, item))
    return results
