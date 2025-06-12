from usdm_excel.base_sheet import BaseSheet
from usdm_excel.alias import Alias
from usdm_model.administrable_product import AdministrableProduct
from usdm_model.ingredient import Ingredient
from usdm_model.substance import Substance
from usdm_model.strength import Strength
from usdm_model.quantity_range import Quantity, Range
from usdm_excel.globals import Globals


class StudyProductSheet(BaseSheet):
    SHEET_NAME = "studyProducts"

    def __init__(self, file_path: str, globals: Globals):
        try:
            self.items: list[AdministrableProduct] = []
            self._current_product: AdministrableProduct | None = None
            self._current_substance: Substance | None = None
            self._current_reference_substance: Substance | None = None
            super().__init__(
                file_path=file_path,
                globals=globals,
                sheet_name=self.SHEET_NAME,
                optional=True,
            )
            if self.success:
                for index, row in self.sheet.iterrows():
                    self._create_administrable_product(index)
                    self._create_ingredient_and_substance(index)
                    self._create_strength(index)
                    self._create_reference_substance(index)
                    self._create_reference_strength(index)
        except Exception as e:
            self._sheet_exception(e)

    def _create_administrable_product(self, index):
        name = self.read_cell_by_name(index, "name")
        if name:
            params = {
                "name": self.read_cell_by_name(index, "name"),
                "description": self.read_cell_by_name(
                    index, "description", must_be_present=False
                ),
                "label": self.read_cell_by_name(index, "label", must_be_present=False),
                "administrableDoseForm": Alias(self.globals).code(
                    self.read_cdisc_klass_attribute_cell_by_name(
                        "AdministrableProduct",
                        "administrableDoseForm",
                        index,
                        "administrableDoseForm",
                    ),
                    [],
                ),
                "pharmacologicClass": self.read_other_code_cell_by_name(
                    index, "pharmacologicClass"
                ),
                "productDesignation": self.read_cdisc_klass_attribute_cell_by_name(
                    "AdministrableProduct",
                    "productDesignation",
                    index,
                    "productDesignation",
                ),
                "sourcing": self.read_cdisc_klass_attribute_cell_by_name(
                    "AdministrableProduct", "sourcing", index, "productSourcing"
                ),
            }
            item = self.create_object(AdministrableProduct, params)
            if item:
                self.items.append(item)
                self.globals.cross_references.add(item.name, item)
                self._current_product = item

    def _create_ingredient_and_substance(self, index):
        name = self.read_cell_by_name(index, "substanceName")
        if name:
            params = {
                "name": name,
                "description": self.read_cell_by_name(
                    index, "substanceDescription", must_be_present=False
                ),
                "label": self.read_cell_by_name(
                    index, "substanceLabel", must_be_present=False
                ),
                "code": self.read_other_code_cell_by_name(index, "substanceCode"),
            }
            substance = self.create_object(Substance, params)
            if substance:
                params = {
                    "role": self.read_other_code_cell_by_name(index, "ingredientRole"),
                    "substance": substance,
                    "strengths": [],
                }
                ingredient = self.create_object(Ingredient, params)
                if ingredient:
                    self._current_product.ingredients.append(ingredient)
                    self._current_substance = substance

    def _create_reference_substance(self, index):
        name = self.read_cell_by_name(index, "referenceSubstanceName")
        if name:
            params = {
                "name": name,
                "description": self.read_cell_by_name(
                    index, "referenceSubstanceDescription", must_be_present=False
                ),
                "label": self.read_cell_by_name(
                    index, "referenceSubstanceLabel", must_be_present=False
                ),
                "code": self.read_other_code_cell_by_name(
                    index, "referenceSubstanceCode"
                ),
            }
            substance = self.create_object(Substance, params)
            if substance:
                self._current_substance.referenceSubstance = substance
                self._current_reference_substance = substance
                return
        self._current_reference_substance = None
        return

    def _create_strength(self, index):
        numerator = self._read_numerator(index, "strengthNumerator")
        # numerator_range = numerator if isinstance(numerator, Range) else None
        # numerator_quantity = numerator if isinstance(numerator, Quantity) else None
        params = {
            "name": self.read_cell_by_name(index, "strengthName"),
            "description": self.read_cell_by_name(
                index, "strengthdescription", must_be_present=False
            ),
            "label": self.read_cell_by_name(
                index, "strengthLabel", must_be_present=False
            ),
            "numerator": numerator,
            "denominator": self.read_quantity_cell_by_name(
                index, "strengthDenominator"
            ),
        }
        strength = self.create_object(Strength, params)
        if strength:
            self._current_substance.strengths.append(strength)

    def _create_reference_strength(self, index):
        name = self.read_cell_by_name(index, "referenceSubstanceStrengthName")
        if name:
            numerator = self._read_numerator(
                index, "referenceSubstanceStrengthNumerator"
            )
            # numerator_range = numerator if isinstance(numerator, Range) else None
            # numerator_quantity = numerator if isinstance(numerator, Quantity) else None
            params = {
                "name": name,
                "description": self.read_cell_by_name(
                    index,
                    "referenceSubstanceStrengthdescription",
                    must_be_present=False,
                ),
                "label": self.read_cell_by_name(
                    index, "referenceSubstanceStrengthLabel", must_be_present=False
                ),
                "numerator": numerator,
                "denominator": self.read_quantity_cell_by_name(
                    index, "referenceSubstanceStrengthDenominator"
                ),
            }
            strength = self.create_object(Strength, params)
            if strength:
                self._current_reference_substance.strengths.append(strength)

    def _read_numerator(self, index, field_name):
        text = self.read_cell_by_name(index, field_name)
        value = (
            self.read_range_cell_by_name(index, field_name, allow_empty=False)
            if ".." in text
            else self.read_quantity_cell_by_name(index, field_name, allow_empty=False)
        )
        if value is None:
            self._general_warning(f"Failed to create numerator from '{text}'")
        return value
