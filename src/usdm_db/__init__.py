import json
import traceback
from usdm_excel import USDMExcel
from usdm_model.wrapper import Wrapper
from usdm_db.document.document import Document
from usdm_db.neo4j_dict import Neo4jDict
from usdm_db.timeline import Timeline

class USDMDb():

  SYSTEM_NAME = "CDISC E2J"

  FULL_HTML = Timeline.FULL
  BODY_HTML = Timeline.BODY
  
  def __init__(self):
    self._wrapper = None
    self._excel = None

  def wrapper(self):
    return self._wrapper
  
  def excel(self):
    return self._excel

  def from_json(self, data):
    self._wrapper = Wrapper.model_validate(data)

  def from_excel(self, file_path):
    self._excel = USDMExcel(file_path)
    self._wrapper = self._excel.wrapper

  def to_json(self):
    try:
      raw_json = self._wrapper.to_json()
    except Exception as e:
      message = self._format_exception("Failed to generate JSON output", e)
      raw_json = json.dumps({'error': message}, indent = 2)
    return raw_json

  def to_html(self, highlight=False):
    try:
      study = self._wrapper.study
      doc = Document("XXXXXXX", study)
      html = doc.to_html(highlight)
    except Exception as e:
      message = self._format_exception("Failed to generate HTML output", e)
      html = f"<p>{message}</p>"
    return html

  def to_pdf(self, test=True):
    try:
      study = self._wrapper.study
      doc = Document("XXXXXXX", study)
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