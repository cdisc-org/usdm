from usdm_excel.managers import Managers

def test_create():
  managers = Managers()
  assert managers.errors  is not None
  assert managers.id_manager  is not None
  assert managers.ct_version_manager  is not None
  assert managers.option_manager  is not None
  assert managers.cross_references  is not None
  assert managers.cdisc_ct_library  is not None
