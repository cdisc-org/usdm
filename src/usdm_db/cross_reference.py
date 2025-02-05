import logging
from datetime import date
from uuid import UUID
from usdm_db.errors_and_logging.errors_and_logging import ErrorsAndLogging


class CrossReference:
    def __init__(self, study, errors_and_logging: ErrorsAndLogging):
        self._errors_and_logging = errors_and_logging
        self._study = study
        self._references = {}
        self._logger = logging.getLogger(__name__)
        self._process_node(self._study)

    def get(self, klass, id):
        key = self._key(klass, id)
        if key in self._references:
            return self._references[key]
        else:
            # print(f"REFERENCES: {list(self._references.keys())}")
            return None

    def _process_node(self, node):
        if type(node) == list:
            if node:
                for item in node:
                    self._process_node(item)
        elif type(node) == str:
            pass
        elif type(node) == float:
            pass
        elif type(node) == date:
            pass
        elif type(node) == bool:
            pass
        elif type(node) == UUID:
            pass
        elif node is None:
            pass
        else:
            if hasattr(node, "instanceType"):
                key = self._key(node.instanceType, node.id)
                self._references[key] = node
            for name, field in node.model_fields.items():
                self._process_node(getattr(node, name))

    def _key(self, klass, id):
        klass_name = self._klass_name(klass)
        return f"{klass_name}.{id}"

    def _klass_name(self, klass):
        return klass if isinstance(klass, str) else klass.__name__
