import warnings
from bs4 import BeautifulSoup
from usdm_db.errors_and_logging.errors_and_logging import ErrorsAndLogging


def usdm_reference(item, attribute):
    return f'<usdm:ref klass="{item.__class__.__name__}" id="{item.id}" attribute="{attribute}"></usdm:ref>'


def get_soup(text: str, errors_and_logging: ErrorsAndLogging):
    try:
        with warnings.catch_warnings(record=True) as warning_list:
            result = BeautifulSoup(text, "html.parser")
        if warning_list:
            for item in warning_list:
                errors_and_logging.debug(
                    f"Warning raised within Soup package, processing '{text}'\nMessage returned '{item.message}'"
                )
        return result
    except Exception as e:
        errors_and_logging.exception(f"Parsing '{text}' with soup", e)
        return ""
