"""
XHTML sanitiser for USDM content fields.

Cleans HTML content to produce valid XHTML that conforms to CDISC CORE rules
(CORE-001069 for NarrativeContentItem, CORE-000945 for SyntaxTemplate).

Fixes applied:
  - Removes disallowed elements (e.g. <style>, <script>)
  - Removes disallowed attributes (e.g. 'type' on <ol>)
  - Repairs malformed/unclosed tags via BeautifulSoup
"""

import re
import warnings
from bs4 import BeautifulSoup, Tag

# Attributes that are NOT allowed in strict XHTML used by CDISC
_DISALLOWED_ATTRIBUTES = {
    "ol": {"type", "start", "reversed"},
    "ul": {"type"},
    "li": {"type", "value"},
}

# Elements not permitted in the XHTML subset
_DISALLOWED_ELEMENTS = {"style", "script", "meta", "link"}


def sanitise_xhtml(html: str) -> tuple[str, list[str]]:
    """
    Sanitise an HTML string to produce valid XHTML.

    Returns:
        tuple of (cleaned_html, list_of_warnings)
        Each warning describes a fix that was applied.
    """
    if not html or not html.strip():
        return html, []

    fixes = []

    with warnings.catch_warnings(record=True):
        soup = BeautifulSoup(html, "html.parser")

    # 1. Remove disallowed elements
    for tag_name in _DISALLOWED_ELEMENTS:
        for element in soup.find_all(tag_name):
            fixes.append(f"Removed disallowed <{tag_name}> element")
            element.decompose()

    # 2. Remove disallowed attributes
    for tag_name, attrs in _DISALLOWED_ATTRIBUTES.items():
        for element in soup.find_all(tag_name):
            for attr in attrs:
                if element.has_attr(attr):
                    fixes.append(
                        f"Removed disallowed '{attr}' attribute from <{tag_name}>"
                    )
                    del element[attr]

    # 3. Detect whether BeautifulSoup repaired malformed HTML.
    #    Re-parse the *original* HTML and re-serialise it; if it differs
    #    from the raw input, BS had to fix tag structure.
    #    Ignore changes to usdm: namespaced tags — these are internal custom
    #    elements (e.g. <usdm:section>) that BS may close but CORE doesn't check.
    if not fixes:
        with warnings.catch_warnings(record=True):
            original_soup = BeautifulSoup(html, "html.parser")
        reserialised = str(original_soup)
        if reserialised != html and not _only_usdm_ns_changes(html, reserialised):
            fixes.append("Repaired malformed HTML (mismatched/unclosed tags)")

    # Only return BS-processed output when real fixes were applied.
    # BS can alter custom tags (e.g. <usdm:section>, <usdm:tag>) during
    # re-serialisation by adding closing tags and stripping the self-close
    # slash.  Restore the original self-closing form.
    if fixes:
        return _restore_usdm_tags(str(soup)), fixes
    return html, fixes


# Pattern matching closing tags for usdm: namespaced elements
_USDM_CLOSE_TAG = re.compile(r"</usdm:[^>]+>")

# Pattern matching self-closing syntax on usdm: elements (e.g. <usdm:tag .../>)
_USDM_SELF_CLOSE = re.compile(r"(<usdm:[^>]*?)\s*/>")

# BS converts <usdm:tag .../> into <usdm:tag ...></usdm:tag>.
# This pattern matches the open-then-immediately-close form so we can
# convert it back to self-closing.
_USDM_OPEN_CLOSE = re.compile(r"(<usdm:[^>]*)>(</usdm:[^>]+>)")


def _restore_usdm_tags(html: str) -> str:
    """Restore usdm: namespaced tags to their self-closing form after BS."""
    # First turn <usdm:tag ...></usdm:tag> back into <usdm:tag .../>
    result = _USDM_OPEN_CLOSE.sub(r"\1/>", html)
    # Then strip any remaining orphan </usdm:*> closing tags
    result = _USDM_CLOSE_TAG.sub("", result)
    return result


def _normalise_usdm_tags(html: str) -> str:
    """Normalise usdm: namespace tags so self-closing and BS forms compare equal."""
    result = _USDM_CLOSE_TAG.sub("", html)
    result = _USDM_SELF_CLOSE.sub(r"\1>", result)
    return result


def _only_usdm_ns_changes(original: str, reserialised: str) -> bool:
    """Return True if the only difference is usdm: tag closing style."""
    return _normalise_usdm_tags(original) == _normalise_usdm_tags(reserialised)
