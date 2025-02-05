from typing import List, Union, Literal
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .administrable_product_property import AdministrableProductProperty
from .identifier import AdministrableProductIdentifier
from .ingredient import Ingredient
from .code import Code
from .alias_code import AliasCode
from .comment_annotation import CommentAnnotation


class AdministrableProduct(ApiBaseModelWithIdNameLabelAndDesc):
    pharmacologicClass: Union[Code, None] = None
    administrableDoseForm: AliasCode
    productDesignation: Code
    sourcing: Union[Code, None] = None
    properties: List[AdministrableProductProperty] = []
    identifiers: List[AdministrableProductIdentifier] = []
    ingredients: List[Ingredient] = []
    notes: List[CommentAnnotation] = []
    instanceType: Literal["AdministrableProduct"]
