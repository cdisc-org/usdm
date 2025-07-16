from typing import Union, List, Literal
from pydantic import BaseModel, Field


class Extension(BaseModel):
    id: str = Field(min_length=1)
    url: str


class BaseCode(BaseModel):
    id: str = Field(min_length=1)
    code: str
    codeSystem: str
    codeSystemVersion: str
    decode: str
    instanceType: Literal["Code"]
    extensionAttributes: List["ExtensionAttribute"] = []


class BaseAliasCode(BaseModel):
    id: str = Field(min_length=1)
    standardCode: BaseCode
    standardCodeAliases: List[BaseCode] = []
    instanceType: Literal["AliasCode"]
    extensionAttributes: List["ExtensionAttribute"] = []


class BaseQuantity(BaseModel):
    id: str = Field(min_length=1)
    value: float
    unit: Union[BaseAliasCode, None] = None
    instanceType: Literal["Quantity"]
    extensionAttributes: List["ExtensionAttribute"] = []


class BaseRange(BaseModel):
    id: str = Field(min_length=1)
    minValue: BaseQuantity
    maxValue: BaseQuantity
    isApproximate: bool
    instanceType: Literal["Range"]
    extensionAttributes: List["ExtensionAttribute"] = []


class ExtensionAttribute(Extension):
    # values or extension attributes, never both.
    valueString: Union[str, None] = None
    valueBoolean: Union[bool, None] = None
    valueInteger: Union[int, None] = None
    valueId: Union[str, None] = None
    valueQuantity: Union[BaseQuantity, None] = None
    valueRange: Union[BaseRange, None] = None
    valueCode: Union[BaseCode, None] = None
    valueAliasCode: Union[BaseAliasCode, None] = None
    valueExtensionClass: Union["ExtensionClass", None] = None
    extensionAttributes: List["ExtensionAttribute"] = []
    instanceType: Literal["ExtensionAttribute"]


class ExtensionClass(Extension):
    extensionAttributes: List["ExtensionAttribute"] = []
    instanceType: Literal["ExtensionClass"]
