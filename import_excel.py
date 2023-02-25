from usdm_excel.usdm_excel import USDMExcel
import os

#study = "Roche Phase 3 NCT04320615"
#study = "cycles_1_v2"
study = "simple_1"
#study = "simple_2"

notebook_path = os.path.abspath("notebook.ipynb")
file_path = os.path.join(os.path.dirname(notebook_path), "source_data/%s.xlsx" % (study))
x = USDMExcel(file_path)
print(x.the_study())