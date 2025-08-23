from usdm_model.narrative_content import NarrativeContent
from usdm_db.fhir.from_fhir import FromFHIR
from usdm_db import USDMDb
from tests.test_integration import format_html

SAVE = False


def test_create(mocker, globals, minimal, factory):
    fhir = FromFHIR(globals.errors_and_logging)
    assert fhir is not None


def test_from_fhir_1_direct(mocker, globals, minimal, factory):
    with open(f"tests/other_test_files/fhir_1.json", "r") as f:
        data = f.read()
    fhir = FromFHIR(globals.errors_and_logging)
    wrapper = fhir.from_fhir(data)
    assert wrapper is not None


def test_from_fhir_1_usdm(mocker, globals, minimal, factory):
    with open(f"tests/other_test_files/fhir_1.json", "r") as f:
        data = f.read()
    usdm = USDMDb()
    fhir = usdm.from_fhir(data)
    html = usdm.to_html("M11")
    filename = "tests/other_test_files/fhir_1.html"
    if SAVE:
        with open(filename, "w") as f:
            f.write(format_html(html))
    with open(filename, "r") as f:
        expected = f.read()
    assert format_html(html) == expected
