from usdm_excel.base_sheet import BaseSheet
from usdm_model.study_version import StudyVersion
from usdm_model.study_definition_document_version import StudyDefinitionDocumentVersion


class Elements:
    def __init__(
        self,
        parent: BaseSheet,
        study_version: StudyVersion,
        document_version: StudyDefinitionDocumentVersion,
    ):
        super().__init__()
        self._parent = parent
        self._study_version = study_version
        self._study_designs = self._study_version.studyDesigns
        self._document_version = document_version
        self._methods = [
            func
            for func in dir(self.__class__)
            if callable(getattr(self.__class__, func)) and not func.startswith("_")
        ]

    def valid_method(self, name: str) -> bool:
        return name in self._methods

    def study_phase(self) -> str:
        results = []
        for study_design in self._study_designs:
            phase = study_design.phase()
            results.append({"instance": phase, "klass": "Code", "attribute": "decode"})
        return self._set_of_references(results)

    def study_short_title(self) -> str:
        title = self._study_version.get_title("Brief Study Title")
        results = (
            [{"instance": title, "klass": "StudyTitle", "attribute": "text"}]
            if title
            else []
        )
        return self._set_of_references(results)

    def study_full_title(self) -> str:
        title = self._study_version.get_title("Official Study Title")
        results = (
            [{"instance": title, "klass": "StudyTitle", "attribute": "text"}]
            if title
            else []
        )
        return self._set_of_references(results)

    def study_acronym(self) -> str:
        title = self._study_version.get_title("Study Acronym")
        results = (
            [{"instance": title, "klass": "StudyTitle", "attribute": "text"}]
            if title
            else []
        )
        return self._set_of_references(results)

    def study_rationale(self) -> str:
        results = [
            {
                "instance": self._study_version,
                "klass": "StudyVersion",
                "attribute": "rationale",
            }
        ]
        return self._set_of_references(results)

    def study_version_identifier(self) -> str:
        results = [
            {
                "instance": self._study_version,
                "klass": "StudyVersion",
                "attribute": "versionIdentifier",
            }
        ]
        return self._set_of_references(results)

    def study_identifier(self) -> str:
        identifier = self._study_version.sponsor_identifier()
        results = [
            {"instance": identifier, "klass": "StudyIdentifier", "attribute": "text"}
        ]
        return self._set_of_references(results)

    def study_regulatory_identifiers(self) -> str:
        results = []
        identifiers = self._study_version.studyIdentifiers
        for identifier in identifiers:
            org = self._study_version.organization(identifier.scopeId)
            if org.type.code == "C188863" or org.type.code == "C93453":
                item = {
                    "instance": identifier,
                    "klass": "StudyIdentifier",
                    "attribute": "text",
                }
                results.append(item)
        return self._set_of_references(results)

    def document_approval_date(self) -> str:
        dates = self._document_version.dateValues
        for date in dates:
            if date.type.code == "C207598":
                results = [
                    {
                        "instance": date,
                        "klass": "GovernanceDate",
                        "attribute": "dateValue",
                    }
                ]
                return self._set_of_references(results)
        return ""

    def study_approval_date(self) -> str:
        dates = self._study_version.dateValues
        for date in dates:
            if date.type.code == "C132352":
                results = [
                    {
                        "instance": date,
                        "klass": "GovernanceDate",
                        "attribute": "dateValue",
                    }
                ]
                return self._set_of_references(results)
        return ""

    def organization_name_and_address(self) -> str:
        identifier = self._study_version.sponsor_identifier()
        org = self._study_version.organization(identifier.scopeId)
        results = [
            {"instance": org, "klass": "Organization", "attribute": "label"},
            {"instance": org.legalAddress, "klass": "Address", "attribute": "text"},
        ]
        return self._set_of_references(results)

    def organization_address(self) -> str:
        identifier = self._study_version.sponsor_identifier()
        org = self._study_version.organization(identifier.scopeId)
        results = [
            {"instance": org.legalAddress, "klass": "Address", "attribute": "text"},
        ]
        return self._set_of_references(results)

    def organization_name(self) -> str:
        identifier = self._study_version.sponsor_identifier()
        org = self._study_version.organization(identifier.scopeId)
        results = [
            {"instance": org, "klass": "Organization", "attribute": "name"},
        ]
        return self._set_of_references(results)

    def amendment(self) -> str:
        amendments = self._study_version.amendments
        if amendments:
            results = [
                {
                    "instance": amendments[-1],
                    "klass": "StudyAmendment",
                    "attribute": "number",
                }
            ]
            return self._set_of_references(results)
        else:
            return ""

    def amendment_scopes(self) -> str:
        results = []
        amendments = self._study_version.amendments
        if amendments:
            amendment = self._study_version.amendments[-1]
            for item in amendment.geographicScopes:
                if item.type.code == "C68846":
                    results = [
                        {"instance": item.type, "klass": "Code", "attribute": "decode"}
                    ]
                    return self._set_of_references(results)
                else:
                    entry = {
                        "instance": item.code.standardCode,
                        "klass": "Code",
                        "attribute": "decode",
                    }
                    results.append(entry)
            return self._set_of_references(results)
        else:
            return ""

    def no_value_for_test(self):
        return ""

    def _set_of_references(self, items):
        if items:
            return ", ".join(
                [
                    f'<usdm:ref klass="{item["klass"]}" id="{item["instance"].id}" attribute="{item["attribute"]}"/>'
                    for item in items
                ]
            )
        else:
            return ""
