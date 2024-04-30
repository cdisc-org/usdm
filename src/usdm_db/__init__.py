import json
import traceback
from uuid import uuid4
from usdm_excel import USDMExcel
from usdm_model.wrapper import Wrapper
from usdm_db.document.document import Document
from usdm_db.fhir.fhir import FHIR
from usdm_db.errors_and_logging.errors_and_logging import ErrorsAndLogging
from usdm_db.neo4j_dict import Neo4jDict
from usdm_db.timeline import Timeline

class USDMDb():

  SYSTEM_NAME = "CDISC E2J"

  FULL_HTML = Timeline.FULL
  BODY_HTML = Timeline.BODY
  
  def __init__(self):
    self._wrapper = None
    self._excel = None
    self._errors_and_logging = ErrorsAndLogging()

  def errors(self):
    return self._errors_and_logging.errors().dump()
  
  def wrapper(self):
    return self._wrapper
  
  def excel(self):
    return self._excel

  def from_json(self, data):
    self._wrapper = Wrapper.model_validate(data)
    
  def from_excel(self, file_path):
    self._excel = USDMExcel(file_path)
    self._wrapper = self._excel.execute()
    return self._excel.errors()

  def to_json(self):
    try:
      raw_json = self._wrapper.to_json()
    except Exception as e:
      message = self._format_exception("Failed to generate JSON output", e)
      raw_json = json.dumps({'error': message}, indent = 2)
    return raw_json

  def to_fhir(self):
    try:
      study = self._wrapper.study
      title = self._get_title()
      fhir = FHIR(title, study, self._errors_and_logging)
      raw_json = fhir.to_fhir(uuid4())
    except Exception as e:
      message = self._format_exception("Failed to generate FHIR output", e)
      raw_json = json.dumps({'error': message}, indent = 2)
    return raw_json

  def to_html(self, highlight=False):
    try:
      study = self._wrapper.study
      title = self._get_title()
      doc = Document(title, study, self._errors_and_logging)
      html = doc.to_html(highlight)
    except Exception as e:
      message = self._format_exception("Failed to generate HTML output", e)
      html = f"<p>{message}</p>"
    return html

  def to_pdf(self, test=True):
    try:
      study = self._wrapper.study
      title = self._get_title()
      doc = Document(title, study, self._errors_and_logging)
      bytes = doc.to_pdf(test)
    except Exception as e:
      message = self._format_exception("Failed to generate PDF output", e)
      bytes = bytearray()
      bytes.extend(map(ord, message))    
    return bytes

  def to_neo4j_dict(self):
    return Neo4jDict(self._wrapper.study).to_dict()

  def to_timeline(self, level=FULL_HTML):
    return Timeline(self._wrapper.study).to_html(level)

  def _format_exception(self, message, e):
    return f"{message}, exception {e}\n{traceback.format_exc()}"
  
  def _get_title(self):
    study = self._wrapper.study
    study_version = study.versions[0]
    title_type = 'Official Study Title'
    for title in study_version.titles:
      if title.type.decode == title_type:
        return title.text
    return None