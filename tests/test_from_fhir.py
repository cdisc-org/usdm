
from usdm_model.narrative_content import NarrativeContent
from usdm_db.fhir.from_fhir import FromFHIR

def test_create(mocker, globals, minimal, factory):
  fhir = FromFHIR(globals.id_manager, globals.errors_and_logging)
  assert fhir is not None

def test_from_fhir_1(mocker, globals, minimal, factory):
  with open(f"tests/integration_test_files/full_1_fhir.json", 'r') as f:
    data = f.read()
  fhir = FromFHIR(globals.id_manager, globals.errors_and_logging)
  fhir.from_fhir(data)

# def test_content_to_section(mocker, globals, minimal, factory):
#   minimal.population.criteria = create_criteria(factory)
#   fhir = ToFHIR("xxx", minimal.study, globals.errors_and_logging)
#   #content = factory.item(NarrativeContent, {'name': "C1", 'sectionNumber': '1.1.1', 'sectionTitle': 'Section Title', 'text': '<usdm:macro id="section" name="inclusion"/>', 'childIds': []})
#   content = factory.item(NarrativeContent, {'name': "C1", 'sectionNumber': '1.1.1', 'sectionTitle': 'Section Title', 'text': 'Something here for the text', 'childIds': []})
#   result = fhir._content_to_section(content)
#   expected = '{"title": "Section Title", "code": {"text": "section1.1.1-section-title"}, "text": {"status": "generated", "div": "Something here for the text"}}'
#   assert result.json() == expected

# def test_format_section(mocker, globals, minimal, factory):
#   fhir = ToFHIR("xxx", minimal.study, globals.errors_and_logging)
#   assert fhir._format_section_title('A Section Heading') == 'a-section-heading'

# def test_clean_section_number(mocker, globals, minimal, factory):
#   fhir = ToFHIR("xxx", minimal.study, globals.errors_and_logging)
#   assert fhir._clean_section_number('1.1') == '1.1'
#   assert fhir._clean_section_number('1.1.') == '1.1'
