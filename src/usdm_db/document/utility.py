import logging
import warnings
import traceback
from bs4 import BeautifulSoup
from usdm_db.errors.errors import Errors

def usdm_reference(item, attribute):
  return f'<usdm:ref klass="{item.__class__.__name__}" id="{item.id}" attribute="{attribute}"></usdm:ref>'

def get_soup(text, errors, logger):
  try:
    with warnings.catch_warnings(record=True) as warning_list:
      result =  BeautifulSoup(text, 'html.parser')
    if warning_list:
      for item in warning_list:
        errors.add(f"Warning raised within Soup package, processing '{text}'\nMessage returned '{item.message}'", Errors.WARNING)
    return result
  except Exception as e:
    log_exception(logger, f"Parsing '{text}' with soup")
    errors.add(f"Exception raised parsing '{text}'. Ignoring value", Errors.ERROR)
    return ""

def log_exception(logger: logging, message, e):
  logger.exception(f"Exception '{e}' raised.\n\n{message}\n\n{traceback.format_exc()}")
  