import json
import traceback
from uuid import uuid4
from usdm_excel import USDMExcel
from usdm_model.wrapper import Wrapper
from usdm_db.document.document import Document
from usdm_db.fhir.to_fhir import ToFHIR
from usdm_db.fhir.from_fhir import FromFHIR
from usdm_db.errors_and_logging.errors_and_logging import ErrorsAndLogging
from usdm_db.neo4j_dict import Neo4jDict
from usdm_db.timeline import Timeline


class USDMDb:
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

    def default_template(self):
        return self._excel.default_template()

    def templates(self):
        return self._excel.templates()

    def from_fhir(self, data: str):
        fhir = FromFHIR(self._errors_and_logging)
        self._wrapper = fhir.from_fhir(data)
        return True

    def was_m11(self) -> bool:
        self._errors_and_logging.deprecated(
            "Method 'was_m11' deprecated, use 'is_m11' going forward"
        )
        return self._excel.was_m11()

    def is_m11(self) -> bool:
        return self._excel.is_m11()

    def to_json(self):
        try:
            raw_json = self._wrapper.to_json()
        except Exception as e:
            message = self._format_exception("Failed to generate JSON output", e)
            raw_json = json.dumps({"error": message}, indent=2)
        return raw_json

    def to_fhir(self, template):
        try:
            study = self._wrapper.study
            fhir = ToFHIR(study, template)
            raw_json = fhir.to_fhir(uuid4())
        except Exception as e:
            message = self._format_exception("Failed to generate FHIR output", e)
            raw_json = json.dumps({"error": message}, indent=2)
        return raw_json

    def to_html(self, template_name: str, highlight: bool = False):
        try:
            study = self._wrapper.study
            doc = Document(study, template_name, self._errors_and_logging)
            html = doc.to_html(highlight)
        except Exception as e:
            message = self._format_exception("Failed to generate HTML output", e)
            html = f"<p>{message}</p>"
        return html

    def to_pdf(self, template_name: str, test: bool = True):
        try:
            study = self._wrapper.study
            doc = Document(study, template_name, self._errors_and_logging)
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
