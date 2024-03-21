import os
import argparse
import logging

import glob, os

DIR = 'src/usdm_excel/data/'

def file_delete(pattern):
  try:
    for f in glob.glob(os.path.join(DIR, pattern)):
      #print(f"FILE1: {f}")
      if f not in [f"{DIR}cdisc_ct_config.yaml"]:
        #print(f"FILE2: {f}")
        os.remove(f)
  except Exception as e:
    print(f"Exception '{e}' deleteing file {pattern}")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    prog='USDM CDISC Data Preparation',
    description='Builds CDISC BC abd CT load files',
    epilog='Note: Not that sophisticated! :)'
  )
  parser.add_argument("--delete_ct", action="store_true", help="Delete the current CT files") 
  parser.add_argument("--delete_bc", action="store_true", help="Delete the current BC files") 
  parser.add_argument('--debug', action='store_true', help='print debug messages to stderr')
  args = parser.parse_args()
  delete_ct = args.delete_ct
  delete_bc = args.delete_bc
  debug = args.debug
  level = logging.DEBUG if debug else logging.INFO

  print(f"DELETE: CT={delete_ct}, BC={delete_bc}")
  print(f"DEBUG: {debug} {level}")
  log = logging.basicConfig(level=level)
  if delete_bc:
    print(f"Deleting BC File")
    file_delete("cdisc_bcs.yaml")
  if delete_ct:
    print(f"Deleting CT File")
    file_delete("cdisc_ct*.yaml")
  
  from usdm_excel.cdisc_ct_library import cdisc_ct_library
  from usdm_excel.cdisc_biomedical_concept import cdisc_bc_library
