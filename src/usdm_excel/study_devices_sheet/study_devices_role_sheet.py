from usdm_excel.base_sheet import BaseSheet
from usdm_model.product_organization_role import ProductOrganizationRole
from usdm_model.organization import Organization
from usdm_excel.globals import Globals

class StudyDeviceRoleSheet(BaseSheet):

  SHEET_NAME = 'deviceRoles'

  def __init__(self, file_path: str, globals: Globals):
    try:
      self.items = []
      super().__init__(file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME, optional=True)
      if self.success:
        for index, row in self.sheet.iterrows():
          params = {
            'name': self.read_cell_by_name(index, 'name'), 
            'description': self.read_cell_by_name(index, 'description', default=''), 
            'label': self.read_cell_by_name(index, 'label', default=''), 
            'organizationId': self.globals.cross_references.get(Organization, self.read_cell_by_name(index, 'organization')).id, 
            'code': self.read_cdisc_klass_attribute_cell_by_name("ProductOrganizationRole", "code", index, "role")
          }
          item = self.create_object(ProductOrganizationRole, params)
          if item:
            self.items.append(item)
            self.globals.cross_references.add(item.name, item)     
    except Exception as e:
      self._sheet_exception(e)

