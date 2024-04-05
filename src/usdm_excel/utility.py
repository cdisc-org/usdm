import logging
import traceback

def general_sheet_exception(name, e):
  log_exception(f"Exception '{e}' raised reading sheet '{name}'")

def log_exception(logger: logging, message, e):
  logger.exception(f"Exception '{e}' raised.\n\n{message}\n\n{traceback.format_exc()}")

def log_error(logger: logging, message):
  logger.error(message)
