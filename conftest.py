import pytest
from src.usdm_model import *
from src.usdm_excel.globals import Globals as GlobalsClass
from tests.test_factory import Factory as FactoryClass
from tests.test_data_factory import MinimalStudy as MinimalStudyClass

global_instance = GlobalsClass()
global_instance.create()
factory_instance = FactoryClass(global_instance)


@pytest.fixture
def globals():
    return global_instance


@pytest.fixture
def factory():
    return factory_instance


@pytest.fixture
def minimal():
    return MinimalStudyClass(global_instance)
