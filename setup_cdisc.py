import glob
import os
import argparse
import logging

DIR = "src/usdm_excel/data/"


def file_delete(pattern):
    try:
        for f in glob.glob(os.path.join(DIR, pattern)):
            if f not in [f"{DIR}cdisc_ct_config.yaml"]:
                os.remove(f)
    except Exception as e:
        print(f"Exception '{e}' deleteing file {pattern}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="USDM CDISC Data Preparation",
        description="Builds CDISC BC abd CT load files",
        epilog="Note: Not that sophisticated! :)",
    )
    parser.add_argument(
        "--delete_ct", action="store_true", help="Delete the current CT files"
    )
    parser.add_argument(
        "--delete_bc", action="store_true", help="Delete the current BC files"
    )
    parser.add_argument(
        "--debug", action="store_true", help="print debug messages to stderr"
    )
    args = parser.parse_args()
    delete_ct = args.delete_ct
    delete_bc = args.delete_bc
    debug = args.debug
    level = logging.DEBUG if debug else logging.INFO

    print(f"DELETE: CT={delete_ct}, BC={delete_bc}")
    print(f"DEBUG: {debug} {level}")
    log = logging.basicConfig(level=level)
    if delete_bc:
        print("Deleting BC File")
        file_delete("cdisc_bcs.yaml")
    if delete_ct:
        print("Deleting CT File")
        file_delete("cdisc_ct*.yaml")

    from src.usdm_excel.cdisc_ct_library import CDISCCTLibrary
    from src.usdm_excel.cdisc_bc_library import CDISCBCLibrary
    from src.usdm_excel.errors_and_logging.errors_and_logging import ErrorsAndLogging
    from src.usdm_excel.id_manager import IdManager

    errors_and_logging = ErrorsAndLogging()
    id_manager = IdManager(errors_and_logging)
    ct = CDISCCTLibrary(errors_and_logging)
    bc = CDISCBCLibrary(errors_and_logging, ct, id_manager)
