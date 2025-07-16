import os
import yaml
import requests
from usdm_excel.errors_and_logging.errors_and_logging import ErrorsAndLogging
from usdm_excel.cdisc_ct_library import CDISCCTLibrary
from usdm_excel.id_manager import IdManager

# from usdm_excel.cross_ref import CrossRef
from usdm_model.biomedical_concept import BiomedicalConcept
from usdm_model.biomedical_concept_property import BiomedicalConceptProperty
from usdm_model.response_code import ResponseCode
from usdm_model.code import Code
from usdm_model.alias_code import AliasCode


class CDISCBCLibrary:
    API_ROOT = "https://api.library.cdisc.org/api/cosmos/v2"

    def __init__(
        self,
        errors_and_logging: ErrorsAndLogging,
        ct_library: CDISCCTLibrary,
        id_manager: IdManager,
        # cross_references: CrossRef
    ):
        self._errors_and_logging = errors_and_logging
        self._ct_library = ct_library
        self._id_manager = id_manager
        # self._cross_references = cross_references
        self._api_key = os.getenv("CDISC_API_KEY")
        if not self._api_key:
            self._errors_and_logging.warning("Empty CDISC API key ...")
        self._headers = {"Content-Type": "application/json", "api-key": self._api_key}
        self._package_metadata = {}
        self._package_items = {}
        self._bc_responses = {}
        self._bcs = {}
        self._bcs_raw = {}
        self._bc_index = {}
        self._map = {}
        if self._bcs_exist():
            self._bcs = self._load_bcs()
        else:
            print("Rebuilding BCs ...")
            self._get_package_metadata()
            self._get_package_items()
            self._get_sdtm_bcs()
            self._get_generic_bcs()
            self._save_bcs(self._bcs_raw)
        self._bc_index = self._create_bc_index()

    def exists(self, name):
        return True if name.upper() in self._bc_index else False

    def catalogue(self) -> list:
        return list(self._bcs.keys())

    def usdm(self, name) -> BiomedicalConcept:
        bc = self._get_bc_data(name) if self.exists(name) else None
        if bc:
            bc_copy = bc.model_dump()
            self._set_ids(bc_copy)
            bc = BiomedicalConcept(**bc_copy)
        return bc

    def _set_ids(self, parent):
        if isinstance(parent, str) or isinstance(parent, bool) or (parent is None):
            return
        parent["id"] = self._id_manager.build_id(parent["instanceType"])
        for name, value in parent.items():
            if isinstance(value, list):
                for child in value:
                    self._set_ids(child)
            else:
                self._set_ids(value)

    def _load_bcs(self):
        results = {}
        data = self._read_bcs()
        for key, item in data.items():
            results[key] = BiomedicalConcept(**item)
        return results

    def _create_bc_index(self):
        results = {}
        for name, item in self._bcs.items():
            results[name] = name
            for synonym in item.synonyms:
                results[synonym.upper()] = name
        return results

    def _get_bc_data(self, name):
        return self._bcs[self._bc_index[name.upper()]]

    def _get_package_metadata(self):
        urls = {
            "generic": "/mdr/bc/packages",
            "sdtm": "/mdr/specializations/sdtm/packages",
        }
        for url_type, url in urls.items():
            try:
                api_url = self._url(url)
                self._errors_and_logging.info(f"CDISC BC Library: {url_type}: {url}")
                raw = requests.get(api_url, headers=self._headers)
                response = raw.json()
                print("#", end="", flush=True)
                self._package_metadata[url_type] = response["_links"]["packages"]
            except Exception as e:
                self._exception(
                    f"Exception '{e}', failed to retrieve CDISC BC package metadata from '{api_url}'",
                    e,
                )
        self._errors_and_logging.debug(f"PACKAGES: {self._package_metadata}")

    def _get_package_items(self) -> dict:
        for package_type in ["sdtm", "generic"]:
            self._package_items[package_type] = {}
            for package in self._package_metadata[package_type]:
                self._get_package(package, package_type)

    def _get_package(self, package, package_type):
        try:
            response_field = {
                "sdtm": "datasetSpecializations",
                "generic": "biomedicalConcepts",
            }
            api_url = self._url(package["href"]) if "href" in package else "not set"
            self._errors_and_logging.info(
                f"CDISC BC Library: {package_type}, {api_url}"
            )
            raw = requests.get(api_url, headers=self._headers)
            response = raw.json()
            print("#", end="", flush=True)
            for item in response["_links"][response_field[package_type]]:
                self._errors_and_logging.debug(f"ITEM: {item}")
                key = item["title"].upper()
                if package_type == "sdtm":
                    self._package_items[package_type][key] = item
                    # map[item['href']] = key
                elif package_type == "generic" and not key in self._package_items:
                    self._errors_and_logging.info(
                        f"GENERIC: Detected generic only BC {key}"
                    )
                    self._package_items[package_type][key] = item
                    self._map[item["href"]] = key
        except Exception as e:
            self._exception(
                f"Exception '{e}', failed to retrieve CDISC BC metadata from '{api_url}'",
                e,
            )
            return {}

    def _get_sdtm_bcs(self):
        # self._bcs, self._bcs_raw =
        for name, item in self._package_items["sdtm"].items():
            self._errors_and_logging.info(f"SDTM BC item '{name}'")
            print(".", end="", flush=True)
            sdtm, generic = self._get_from_url_all(name, item)
            if sdtm:
                bc = self._sdtm_bc_as_usdm(sdtm, generic)
                if bc:
                    if "variables" in sdtm:
                        for item in sdtm["variables"]:
                            property = self._sdtm_bc_property_as_usdm(item, generic)
                            if property:
                                bc.properties.append(property)
                    self._bcs_raw[name] = bc.model_dump()
                    self._bcs[name] = bc
                if generic:
                    href = generic["_links"]["self"]["href"]
                    if href in self._map:
                        self._map.pop(generic["_links"]["self"]["href"])
                    else:
                        self._errors_and_logging.error(
                            f"Missing reference when popping {href}"
                        )

    def _get_generic_bcs(self) -> BiomedicalConcept:
        for name, item in self._package_items["generic"].items():
            self._errors_and_logging.info(f"GENERIC BC item '{name}'")
            print(".", end="", flush=True)
            if self._process_genric_bc(name):
                response = self._get_from_url(item["href"])
                print("#", end="", flush=True)
                bc = self._generic_bc_as_usdm(response)
                if "dataElementConcepts" in response:
                    for item in response["dataElementConcepts"]:
                        property = self._generic_bc_property_as_usdm(item)
                        if property:
                            bc.properties.append(property)
                self._bcs_raw[name] = bc.model_dump()
                self._bcs[name] = bc

    def _generic_bc_as_usdm(self, api_bc) -> BiomedicalConcept:
        concept_code = self._cdisc_code(api_bc["conceptId"], api_bc["shortName"])
        synonyms = api_bc["synonyms"] if "synonyms" in api_bc else []
        return self._biomedical_concept_object(
            api_bc["shortName"],
            api_bc["shortName"],
            synonyms,
            api_bc["_links"]["self"]["href"],
            concept_code,
        )

    def _generic_bc_property_as_usdm(self, property) -> BiomedicalConceptProperty:
        concept_code = self._cdisc_code(property["conceptId"], property["shortName"])
        responses = []
        if "exampleSet" in property:
            for example in property["exampleSet"]:
                term = self._ct_library.preferred_term(example)
                if term != None:
                    code = self._cdisc_code(term["conceptId"], term["preferredTerm"])
                    code.id = "tbd"
                    responses.append(
                        ResponseCode(
                            id="tbd",
                            name=f"RC_{code.code}",
                            label="",
                            isEnabled=True,
                            code=code,
                        )
                    )
        return self._biomedical_concept_property_object(
            property["shortName"],
            property["shortName"],
            property["dataType"],
            responses,
            concept_code,
        )

    def _sdtm_bc_as_usdm(self, sdtm, generic) -> BiomedicalConcept:
        try:
            if self._process_sdtm_bc(sdtm["shortName"]):
                self._errors_and_logging.debug(f"BC: {sdtm}\n\n{generic}")
                role_variable = self._get_role_variable(sdtm)
                if role_variable:
                    if "assignedTerm" in role_variable:
                        if (
                            "conceptId" in role_variable["assignedTerm"]
                            and "value" in role_variable["assignedTerm"]
                        ):
                            concept_code = self._cdisc_code(
                                role_variable["assignedTerm"]["conceptId"],
                                role_variable["assignedTerm"]["value"],
                            )
                        else:
                            self._errors_and_logging.error(
                                f"Failed to set BC concept 1, {sdtm['shortName']}"
                            )
                            concept_code = self._cdisc_code(
                                "No Concept Code",
                                role_variable["assignedTerm"]["value"],
                            )
                    else:
                        self._errors_and_logging.error(
                            f"Failed to set BC concept 2, {sdtm['shortName']}"
                        )
                        concept_code = self._cdisc_code(
                            generic["conceptId"], generic["shortName"]
                        )
                else:
                    self._errors_and_logging.error(
                        f"Failed to set BC concept {sdtm['shortName']}"
                    )
                    concept_code = self._cdisc_code(
                        generic["conceptId"], generic["shortName"]
                    )
                synonyms = generic["synonyms"] if "synonyms" in generic else []
                synonyms.append(generic["shortName"])
                return self._biomedical_concept_object(
                    sdtm["shortName"],
                    sdtm["shortName"],
                    synonyms,
                    sdtm["_links"]["self"]["href"],
                    concept_code,
                )
            else:
                return None
        except Exception as e:
            self._exception(
                f"Exception '{e}', failed to build BC {sdtm['shortName']}", e
            )
            return None

    def _sdtm_bc_property_as_usdm(
        self, sdtm_property, generic
    ) -> BiomedicalConceptProperty:
        try:
            self._errors_and_logging.debug(
                f"NAME: {sdtm_property['name']}, {sdtm_property['name'][2:]}"
            )
            if self._process_property(sdtm_property["name"]):
                self._errors_and_logging.debug(f"PROPERTY: {sdtm_property}")
                if "dataElementConceptId" in sdtm_property:
                    generic_match = self._get_dec_match(
                        generic, sdtm_property["dataElementConceptId"]
                    )
                    if generic_match:
                        concept_code = self._cdisc_code(
                            generic_match["conceptId"], generic_match["shortName"]
                        )
                    else:
                        if (
                            "assignedTerm" in sdtm_property
                            and "conceptId" in sdtm_property["assignedTerm"]
                            and "value" in sdtm_property["assignedTerm"]
                        ):
                            concept_code = self._cdisc_code(
                                sdtm_property["dataElementConceptId"],
                                sdtm_property["name"],
                            )
                        else:
                            self._errors_and_logging.error(
                                f"Failed to set property concept 1, {sdtm_property}"
                            )
                            concept_code = self._cdisc_code(
                                sdtm_property["dataElementConceptId"],
                                sdtm_property["name"],
                            )
                else:
                    if "assignedTerm" in sdtm_property:
                        concept_code = self._cdisc_code(
                            sdtm_property["assignedTerm"]["conceptId"],
                            sdtm_property["assignedTerm"]["value"],
                        )
                    else:
                        self._errors_and_logging.error(
                            f"Failed to set property concept 2, {sdtm_property}"
                        )
                        concept_code = self._cdisc_code(
                            "No Concept Code", sdtm_property["name"]
                        )
                responses = []
                codes = []
                if "valueList" in sdtm_property:
                    codelist = (
                        sdtm_property["codelist"]["conceptId"]
                        if "codelist" in sdtm_property
                        else None
                    )
                    for value in sdtm_property["valueList"]:
                        term = self._ct_library.preferred_term(value, codelist)
                        if term:
                            code = self._cdisc_code(
                                term["conceptId"], term["preferredTerm"]
                            )
                            code.id = "tbd"
                            codes.append(code)
                        else:
                            term = self._ct_library.submission(value, codelist)
                            if term:
                                code = self._cdisc_code(
                                    term["conceptId"], term["preferredTerm"]
                                )
                                code.id = "tbd"
                                codes.append(code)
                            else:
                                cl = f", code list {sdtm_property['codelist']['conceptId'] if 'codelist' in sdtm_property else '<not defined>'}"
                                self._errors_and_logging.error(
                                    f"Failed to find submission or preferred term '{value}' {cl}"
                                )
                for code in codes:
                    response_code = ResponseCode(
                        id="tbd",
                        name=f"RC_{code.code}",
                        label="",
                        isEnabled=True,
                        code=code,
                    )
                    responses.append(response_code)
                datatype = (
                    sdtm_property["dataType"] if "dataType" in sdtm_property else ""
                )
                return self._biomedical_concept_property_object(
                    sdtm_property["name"],
                    sdtm_property["name"],
                    datatype,
                    responses,
                    concept_code,
                )
            else:
                return None
        except Exception as e:
            self._exception(
                f"Exception '{e}', failed to build property {sdtm_property}", e
            )
            return None

    def _biomedical_concept_object(
        self, name, label, synonyms, reference, code
    ) -> BiomedicalConcept:
        code.id = "tbd"
        alias_code = self._alias_code(code, [])
        alias_code.id = "tbd"
        return BiomedicalConcept(
            id="tbd",
            name=name,
            label=label,
            synonyms=synonyms,
            reference=reference,
            properties=[],
            code=alias_code,
        )

    def _biomedical_concept_property_object(
        self, name, label, datatype, responses, code
    ):
        code.id = "tbd"
        alias_code = self._alias_code(code, [])
        alias_code.id = "tbd"
        return BiomedicalConceptProperty(
            id="tbd",
            name=name,
            label=label,
            isRequired=True,
            isEnabled=True,
            datatype=datatype,
            responseCodes=responses,
            code=alias_code,
        )

    def _process_sdtm_bc(self, name):
        if name in [
            "Exclusion Criteria 01",
            "Inclusion Criteria 01",
            "Medical History Prespecified: Alzheimer's Disease",
            "Medical History Prespecified: Confusional Episodes",
            "Medical History Prespecified: Essential Tremor",
            "Medical History Prespecified: Extrapyramidal Features",
            "Medical History Prespecified: Facial Masking",
            "Medical History Prespecified: Rigidity Upper Extremity",
            "Medical History Prespecified: Sensitivity to Neuroleptics",
            "Medical History Prespecified: Visual Hallucinations",
            "TTS Acceptability Survey - Patch Acceptability",
            "TTS Acceptability Survey - Patch Appearance",
            "TTS Acceptability Survey - Patch Durability",
            "TTS Acceptability Survey - Patch Size",
            "Beer Use History",
            "Cigarette History",
            "Cigar History",
            "Coffee Use History",
            "Cola Use History",
            "Distilled Spirits Use History",
            "Pipe History",
            "Tea Use History",
            "Wine Use History",
        ]:
            return False
        return True

    def _process_genric_bc(self, name):
        return True if name.upper() in ["SUBJECT AGE", "RACE", "SEX"] else False

    def _process_property(self, name):
        if name[2:] in [
            "TEST",
            "STRESN",
            "STRESU",
            "STRESC",
            "CLASCD",
            "LOINC",
            "LOT",
            "CAT",
            "SCAT",
            "LLT",
            "LLTCD",
            "HLT",
            "HLTCD",
            "PTCD",
            "BODSYS",
            "BDSYCD",
            "SOC",
            "SOCCD",
            "RLDEV",
        ]:
            return False
        if name in ["EPOCH"]:
            return False
        return True

    def _get_role_variable(self, data):
        return next(
            (item for item in data["variables"] if item["role"] == "Topic"), None
        )

    def _get_dec_match(self, data, id):
        return next(
            (item for item in data["dataElementConcepts"] if item["conceptId"] == id),
            None,
        )

    def _get_from_url_all(self, name, details) -> dict:
        try:
            self._errors_and_logging.debug(f"DETAILS: {details}")
            sdtm_response = self._get_from_url(details["href"])
            generic = sdtm_response["_links"]["parentBiomedicalConcept"]
            generic_response = self._get_from_url(generic["href"])
            return sdtm_response, generic_response
        except Exception as e:
            self._exception(
                f"Exception '{e}', failed to retrieve CDISC BC metadata for {name} from '{details['href']}'",
                e,
            )
            return None, None

    def _get_from_url(self, url):
        api_url = self._url(url)
        self._errors_and_logging.info("CDISC BC Library: %s" % api_url)
        raw = requests.get(api_url, headers=self._headers)
        result = raw.json()
        return result

    def _url(self, relative_url) -> str:
        return "%s%s" % (self.__class__.API_ROOT, relative_url)

    def _save_bcs(self, data):
        try:
            with open(self._bcs_filename(), "w") as f:
                yaml.dump(data, f, indent=2, sort_keys=True)
        except Exception as e:
            self._exception(f"Exception '{e}', failed to save CDSIC BC file", e)

    def _read_bcs(self):
        try:
            if self._bcs_exist():
                with open(self._bcs_filename()) as f:
                    return yaml.load(f, Loader=yaml.FullLoader)
            else:
                self._errors_and_logging.error(
                    f"Failed to read CDSIC BC file, does not exist"
                )
                return None
        except Exception as e:
            self._exception(f"Exception '{e}', failed to read CDSIC CT file", e)

    def _bcs_exist(self):
        return os.path.isfile(self._bcs_filename())

    def _bcs_filename(self):
        return os.path.join(os.path.dirname(__file__), "data", f"cdisc_bcs.yaml")

    def _cdisc_code(self, code, decode):
        id = self._id_manager.build_id(Code)
        instance = Code(
            id=id,
            code=code,
            codeSystem=self._ct_library.system,
            codeSystemVersion=self._ct_library.version,
            decode=decode,
        )
        # self._cross_references.add(instance.id, instance)
        return instance

    def _alias_code(self, standard_code, aliases):
        return (
            AliasCode(
                id=self._id_manager.build_id(AliasCode),
                standardCode=standard_code,
                standardCodeAliases=aliases,
            )
            if standard_code
            else None
        )

    def _exception(self, message, e):
        self._errors_and_logging.exception(message, e)
