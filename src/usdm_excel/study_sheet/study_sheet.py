from usdm_model.governance_date import GovernanceDate
from usdm_model.geographic_scope import GeographicScope
from usdm_model.study_title import StudyTitle
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.alias import Alias
from usdm_excel.cdisc_ct import CDISCCT
from usdm_excel.iso_3166 import ISO3166
from usdm_excel.option_manager import Options
from usdm_excel.globals import Globals


class StudySheet(BaseSheet):
    SHEET_NAME = "study"

    NAME_TITLE = "name"
    DESCRIPTION_TITLE = "description"
    LABEL_TITLE = "label"
    TITLE_TITLE = "studyTitle"
    VERSION_TITLE = "studyVersion"
    TYPE_TITLE = "studyType"
    PHASE_TITLE = "studyPhase"
    ACRONYM_TITLE = "studyAcronym"
    RATIONALE_TITLE = "studyRationale"
    TA_TITLE = "businessTherapeuticAreas"
    BRIEF_TITLE_TITLE = "briefTitle"
    OFFICAL_TITLE_TITLE = "officialTitle"
    PUBLIC_TITLE_TITLE = "publicTitle"
    SCIENTIFIC_TITLE_TITLE = "scientificTitle"
    PROTOCOL_VERSION_TITLE = "protocolVersion"
    PROTOCOL_STATUS_TITLE = "protocolStatus"

    PARAMS_NAME_COL = 0
    PARAMS_DATA_COL = 1

    STUDY_VERSION_DATE = "study_version"
    PROTOCOL_VERSION_DATE = "protocol_document"
    AMENDMENT_DATE = "amendment"

    def __init__(self, file_path: str, globals: Globals):
        try:
            super().__init__(
                file_path=file_path,
                globals=globals,
                sheet_name=self.SHEET_NAME,
                header=None,
            )
            self.date_categories = [
                self.STUDY_VERSION_DATE,
                self.PROTOCOL_VERSION_DATE,
                self.AMENDMENT_DATE,
            ]
            self.phase = None
            self.version = None
            self.type = None
            self.name = None
            self.description = None
            self.label = None
            self.brief_title = None
            self.official_title = None
            self.public_title = None
            self.scientific_title = None
            self.protocol_version = None
            self.protocol_status = None
            self.title = None
            self.titles = []
            self.acronym = None
            self.rationale = None
            self.study = None
            self.study_version = None
            self.protocol_document_version = None
            self.therapeutic_areas = []
            self.timelines = {}
            self.dates = {}
            for category in self.date_categories:
                self.dates[category] = []
            self._process_sheet()
        except Exception as e:
            self._sheet_exception(e)

    def _process_sheet(self):
        main_part = True
        dates_row = 15
        fields = ["category", "name", "description", "label", "type", "date", "scopes"]
        for rindex, row in self.sheet.iterrows():
            field_name = self.read_cell(rindex, self.PARAMS_NAME_COL)
            if main_part:
                if field_name == self.NAME_TITLE:
                    self.name = self.read_cell(rindex, self.PARAMS_DATA_COL)
                elif field_name == self.DESCRIPTION_TITLE:
                    self.description = self.read_cell(rindex, self.PARAMS_DATA_COL)
                elif field_name == self.LABEL_TITLE:
                    self.label = self.read_cell(rindex, self.PARAMS_DATA_COL)
                elif field_name == self.VERSION_TITLE:
                    self.version = self.read_cell(rindex, self.PARAMS_DATA_COL)
                elif field_name == self.TYPE_TITLE:
                    self._warning(
                        rindex,
                        self.PARAMS_DATA_COL,
                        f"Study type has been moved to the 'studyDesign' sheet, value ignored",
                    )
                elif field_name == self.PHASE_TITLE:
                    self._warning(
                        rindex,
                        self.PARAMS_DATA_COL,
                        f"Study phase has been moved to the 'studyDesign' sheet, value ignored",
                    )
                elif field_name == self.ACRONYM_TITLE:
                    self.acronym = self._set_title(
                        rindex, self.PARAMS_DATA_COL, "Study Acronym"
                    )
                elif field_name == self.RATIONALE_TITLE:
                    self.rationale = self.read_cell(rindex, self.PARAMS_DATA_COL)
                elif field_name == self.TA_TITLE:
                    self.therapeutic_areas = self.read_other_code_cell_mutiple(
                        rindex, self.PARAMS_DATA_COL
                    )
                elif field_name == self.TITLE_TITLE:
                    self._warning(
                        rindex,
                        self.PARAMS_DATA_COL,
                        f"Study title has been deprecated, use officialTitle or publicTitle instead",
                    )
                elif field_name == self.BRIEF_TITLE_TITLE:
                    self.brief_title = self._set_title(
                        rindex, self.PARAMS_DATA_COL, "Brief Study Title"
                    )
                elif field_name == self.OFFICAL_TITLE_TITLE:
                    self.official_title = self._set_title(
                        rindex, self.PARAMS_DATA_COL, "Official Study Title"
                    )
                elif field_name == self.PUBLIC_TITLE_TITLE:
                    self.public_title = self._set_title(
                        rindex, self.PARAMS_DATA_COL, "Public Study Title"
                    )
                elif field_name == self.SCIENTIFIC_TITLE_TITLE:
                    self.scientific_title = self._set_title(
                        rindex, self.PARAMS_DATA_COL, "Scientific Study Title"
                    )
                elif field_name == self.PROTOCOL_VERSION_TITLE:
                    self.protocol_version = self.read_cell(rindex, self.PARAMS_DATA_COL)
                elif field_name == self.PROTOCOL_STATUS_TITLE:
                    self.protocol_status = self.read_cdisc_klass_attribute_cell(
                        "StudyProtocolVersion",
                        "protocolStatus",
                        rindex,
                        self.PARAMS_DATA_COL,
                    )
                elif field_name == "":
                    main_part = False
                    dates_row = rindex + 2
                else:
                    self._warning(
                        rindex,
                        self.PARAMS_DATA_COL,
                        f"Unrecognized key '{field_name}', ignored",
                    )

            else:
                if rindex >= dates_row:
                    record = {}
                    for cindex in range(0, len(self.sheet.columns)):
                        field = fields[cindex]
                        if field == "category":
                            cell = self.read_cell(rindex, cindex)
                            if cell.lower() in self.date_categories:
                                category = cell.lower()
                            else:
                                categories = ", ".join(
                                    f'"{w}"' for w in self.date_categories
                                )
                                self._error(
                                    rindex,
                                    cindex,
                                    f"Date category not recognized, should be one of {categories}, defaults to '{self.date_categories[0]}'",
                                )
                                category = self.date_categories[0]
                        elif field == "type":
                            record[field] = self.read_cdisc_klass_attribute_cell(
                                "GovernanceDate", "type", rindex, cindex
                            )
                        elif field == "date":
                            record[field] = self.read_date_cell(rindex, cindex)
                        elif field == "scopes":
                            record[field] = self.read_geographic_scopes_cell(
                                rindex, cindex
                            )
                        else:
                            cell = self.read_cell(rindex, cindex)
                            record[field] = cell
                    try:
                        date = GovernanceDate(
                            id=self.globals.id_manager.build_id(GovernanceDate),
                            name=record["name"],
                            label=record["label"],
                            description=record["description"],
                            type=record["type"],
                            dateValue=record["date"],
                            geographicScopes=record["scopes"],
                        )
                        self.dates[category].append(date)
                        self.globals.cross_references.add(record["name"], date)
                    except Exception as e:
                        self._general_exception(
                            f"Failed to create GovernanceDate object", e
                        )

    def _set_title(self, rindex, cindex, title_type):
        try:
            text = self.read_cell(rindex, cindex)
            if text:
                code = CDISCCT(self.globals).code_for_attribute(
                    "StudyTitle", "type", title_type
                )
                title = StudyTitle(
                    id=self.globals.id_manager.build_id(StudyTitle),
                    text=text,
                    type=code,
                )
                self.titles.append(title)
                self.globals.cross_references.add(title.id, title)
                return title
            else:
                return None
        except Exception as e:
            self._exception(rindex, cindex, "Failed to create StudyTitle object", e)
