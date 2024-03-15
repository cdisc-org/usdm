from usdm_excel.cdisc_biomedical_concept import cdisc_bc_library


print(f"CAT: {cdisc_bc_library.catalogue()}")
print(f"PM: {cdisc_bc_library.package_metadata}")
print(f"BC: {cdisc_bc_library.usdm('WEIGHT')}")