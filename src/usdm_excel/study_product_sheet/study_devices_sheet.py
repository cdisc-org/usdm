from usdm_model.medical_device import MedicalDevice
from usdm_model.administrable_product import AdministrableProduct
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.globals import Globals


class StudyDevicesSheet(BaseSheet):
    SHEET_NAME = "studyDevices"

    def __init__(self, file_path, globals: Globals):
        try:
            self.items = []
            super().__init__(
                file_path=file_path,
                globals=globals,
                sheet_name=self.SHEET_NAME,
                optional=True,
            )
            if self.success:
                self._process_sheet()
        except Exception as e:
            self._sheet_exception(e)

    def _process_sheet(self):
        for index, row in self.sheet.iterrows():
            params = {
                "name": self.read_cell_by_name(index, "name"),
                "description": self.read_cell_by_name(index, "description"),
                "label": self.read_cell_by_name(index, "label"),
                "hardwareVersion": self.read_cell_by_name(index, "hardwareVersion"),
                "softwareVersion": self.read_cell_by_name(index, "softwareVersion"),
                "sourcing": self.read_cdisc_klass_attribute_cell_by_name(
                    "MedicalDevice", "sourcing", index, ["sourcing"]
                ),
            }
            product_name = self.read_cell_by_name(index, "product")
            product = self.globals.cross_references.get(
                AdministrableProduct, product_name
            )
            if product:
                params["embeddedProductId"] = product.id
            else:
                self._warning(
                    index,
                    "product",
                    f"Failed to find administrable product with name '{product_name}'",
                )
            notes = self.read_cell_multiple_by_name(
                index, "notes", must_be_present=False
            )
            item: MedicalDevice = self.create_object(MedicalDevice, params)
            if item:
                self.items.append(item)
                self.add_notes(item, notes)
                self.globals.cross_references.add(item.name, item)
