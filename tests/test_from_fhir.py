from usdm_model.narrative_content import NarrativeContent
from usdm_db.fhir.from_fhir import FromFHIR
from usdm_db import USDMDb


def test_create(mocker, globals, minimal, factory):
    fhir = FromFHIR(globals.errors_and_logging)
    assert fhir is not None


def test_from_fhir_1(mocker, globals, minimal, factory):
    with open(f"tests/integration_test_files/full_1_fhir.json", "r") as f:
        data = f.read()
    fhir = FromFHIR(globals.errors_and_logging)
    wrapper = fhir.from_fhir(data)
    assert wrapper is not None


def test_from_fhir_1(mocker, globals, minimal, factory):
    with open(f"tests/integration_test_files/full_1_fhir.json", "r") as f:
        data = f.read()
    usdm = USDMDb()
    fhir = usdm.from_fhir(data)
    html = usdm.to_html("document")
    print(html)
