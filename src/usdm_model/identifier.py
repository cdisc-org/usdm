from typing import Literal
from .api_base_model import ApiBaseModelWithId
from .code import Code


class Identifier(ApiBaseModelWithId):
    text: str
    scopeId: str
    instanceType: Literal["Identifier"]


class ReferenceIdentifier(Identifier):
    type: Code
    instanceType: Literal["ReferenceIdentifier"]


class StudyIdentifier(Identifier):
    instanceType: Literal["StudyIdentifier"]


class AdministrableProductIdentifier(Identifier):
    instanceType: Literal["AdministrableProductIdentifier"]


class MedicalDeviceIdentifier(Identifier):
    type: Code
    instanceType: Literal["MedicalDeviceIdentifier"]
