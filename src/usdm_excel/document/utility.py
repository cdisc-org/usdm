import warnings
import traceback
from bs4 import BeautifulSoup


def usdm_reference(item, attribute):
    return f'<usdm:ref klass="{item.__class__.__name__}" id="{item.id}" attribute="{attribute}"></usdm:ref>'


def get_soup(text, parent):
    try:
        with warnings.catch_warnings(record=True) as warning_list:
            result = BeautifulSoup(text, "html.parser")
        if warning_list:
            for item in warning_list:
                parent._general_debug(
                    f"Warning raised within Soup package, processing '{text}'\nMessage returned '{item.message}'"
                )
        return result
    except Exception as e:
        parent._exception(f"Eerror raised parsing '{text}'", e)
        return ""
