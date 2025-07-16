import os
import yaml
import traceback
import requests
from usdm_excel.errors_and_logging.errors_and_logging import ErrorsAndLogging


class CDISCCTLibrary:
    API_ROOT = "https://api.library.cdisc.org/api"
    HEADERS = {
        "Content-Type": "application/json",
        "api-key": os.getenv("CDISC_API_KEY"),
    }

    def __init__(self, errors_and_logging: ErrorsAndLogging):
        self._errors_and_logging = errors_and_logging
        f = open(os.path.join(os.path.dirname(__file__), "data", "missing_ct.yaml"))
        self._missing_ct = yaml.load(f, Loader=yaml.FullLoader)
        f = open(
            os.path.join(os.path.dirname(__file__), "data", "cdisc_ct_config.yaml")
        )
        self._cdisc_ct_config = yaml.load(f, Loader=yaml.FullLoader)
        # Visible properties
        self.version = self._cdisc_ct_config["version"]
        self.system = "http://www.cdisc.org"
        # Private properties
        self._by_code_list = {}
        self._by_term = {}
        self._by_submission = {}
        self._by_pt = {}
        self._by_klass_attribute = {}
        if self._code_lists_exist():
            self._load_ct()
        else:
            self._get_ct()
            self._save_code_lists(self._by_code_list)
        self._get_missing_ct()
        self._get_klass_attribute()

    def submission(self, value, cl=None):
        if value in list(self._by_submission.keys()):
            concept_ids = self._by_submission[value]
            if len(concept_ids) == 0:
                return None
            elif len(concept_ids) == 1:
                code_list = self._by_code_list[concept_ids[0]]
                return next(
                    (
                        item
                        for item in code_list["terms"]
                        if item["submissionValue"] == value
                    ),
                    None,
                )
            else:
                if cl and cl in concept_ids:
                    code_list = self._by_code_list[cl]
                    return next(
                        (
                            item
                            for item in code_list["terms"]
                            if item["submissionValue"] == value
                        ),
                        None,
                    )
                else:
                    return None
        else:
            return None

    def preferred_term(self, value, cl=None):
        if value in list(self._by_pt.keys()):
            concept_ids = self._by_pt[value]
            if len(concept_ids) == 0:
                return None
            elif len(concept_ids) == 1:
                code_list = self._by_code_list[concept_ids[0]]
                return next(
                    (
                        item
                        for item in code_list["terms"]
                        if item["preferredTerm"] == value
                    ),
                    None,
                )
            else:
                if cl and cl in concept_ids:
                    code_list = self._by_code_list[cl]
                    return next(
                        (
                            item
                            for item in code_list["terms"]
                            if item["preferredTerm"] == value
                        ),
                        None,
                    )
                else:
                    return None
        else:
            return None

    def klass_and_attribute(self, klass, attribute, value):
        try:
            # if value == "Protocol Treatment Arm":
            #  print(f"Klass: {klass}, attribute: {attribute}, value: {value}")
            concept_id = self._by_klass_attribute[klass][attribute]
            # if value == "Protocol Treatment Arm":
            #  print(f"Concept: {concept_id}")
            code_list = self._by_code_list[concept_id]
            # if value == "Protocol Treatment Arm":
            #  print(f"Concept: {code_list}")
            return self._get_item(code_list, value)
        except Exception as e:
            self._errors_and_logging.exception(
                f"Failed to find '{value}' for klass '{klass}' attribute '{attribute}'",
                e,
            )
            return None

    def unit(self, value):
        try:
            code_list = self._by_code_list["C71620"]
            return self._get_item(code_list, value)
        except Exception as e:
            self._errors_and_logging.exception(f"Failed to find unit '{value}'")
            return None

    def _get_item(self, code_list, value):
        try:
            for field in ["conceptId", "preferredTerm", "submissionValue"]:
                # if value == "Protocol Treatment Arm":
                #  print(f"GET: {field}")
                result = next(
                    (
                        item
                        for item in code_list["terms"]
                        if item[field].upper() == value.upper()
                    ),
                    None,
                )
                if result:
                    return result
            return None
        except Exception as e:
            self._errors_and_logging.exception(
                f"Failed to find CDSIC CT for '{value}' in code ist '{code_list}'", e
            )
            return None

    def _get_ct(self):
        for item in self._cdisc_ct_config["required"]:
            self._get_code_list(item)

    def _load_ct(self):
        self._by_code_list = self._read_code_lists()
        for c_code, entry in self._by_code_list.items():
            for item in entry["terms"]:
                self._check_in_and_add(self._by_term, item["conceptId"], c_code)
                self._check_in_and_add(
                    self._by_submission, item["submissionValue"], c_code
                )
                self._check_in_and_add(self._by_pt, item["preferredTerm"], c_code)

    def _get_missing_ct(self):
        for response in self._missing_ct:
            self._by_code_list[response["conceptId"]] = response
            for item in response["terms"]:
                self._check_in_and_add(
                    self._by_term, item["conceptId"], response["conceptId"]
                )
                self._check_in_and_add(
                    self._by_submission, item["submissionValue"], response["conceptId"]
                )
                self._check_in_and_add(
                    self._by_pt, item["preferredTerm"], response["conceptId"]
                )

    def _get_klass_attribute(self):
        for klass, info in self._cdisc_ct_config["klass"].items():
            if not klass in self._by_klass_attribute:
                self._by_klass_attribute[klass] = {}
            for attribute, cl in info.items():
                if not attribute in self._by_klass_attribute[klass]:
                    self._by_klass_attribute[klass][attribute] = cl

    def _get_code_list(self, c_code):
        for package in self._cdisc_ct_config["packages"]:
            package_full_name = "%sct-%s" % (package, self.version)
            api_url = self._url(
                "/mdr/ct/packages/%s/codelists/%s" % (package_full_name, c_code)
            )
            self._errors_and_logging.info(f"CDISC CT Library: {api_url}")
            raw = requests.get(api_url, headers=self.__class__.HEADERS)
            if raw.status_code == 200:
                response = raw.json()
                response.pop("_links", None)
                self._by_code_list[response["conceptId"]] = response
                for item in response["terms"]:
                    self._check_in_and_add(
                        self._by_term, item["conceptId"], response["conceptId"]
                    )
                    self._check_in_and_add(
                        self._by_submission,
                        item["submissionValue"],
                        response["conceptId"],
                    )
                    self._check_in_and_add(
                        self._by_pt, item["preferredTerm"], response["conceptId"]
                    )
                return
        # If none found in all of the packages, then log error.
        self._errors_and_logging.error(
            f"Failed to find CDSIC CT for C code '{c_code}'"
        )

    def _url(self, relative_url):
        return f"{self.__class__.API_ROOT}{relative_url}"

    def _check_in_and_add(self, collection, id, item):
        if not id in collection:
            collection[id] = []
        collection[id].append(item)

    def _save_code_lists(self, data):
        try:
            if not self._code_lists_exist():
                with open(self._ct_filename(), "w") as f:
                    yaml.dump(data, f, indent=2, sort_keys=True)
        except Exception as e:
            self._errors_and_logging.exception("Failed to save CDSIC CT file", e)

    def _read_code_lists(self):
        try:
            if self._code_lists_exist():
                with open(self._ct_filename()) as f:
                    return yaml.safe_load(f)
            else:
                self._errors_and_logging.error(
                    f"Failed to read CDSIC CT file, does not exist"
                )
                return None
        except Exception as e:
            self._errors_and_logging.exception("Failed to read CDSIC CT file", e)

    def _code_lists_exist(self):
        return os.path.isfile(self._ct_filename())

    def _ct_filename(self):
        return os.path.join(
            os.path.dirname(__file__),
            "data",
            f"cdisc_ct_{self._cdisc_ct_config['version']}.yaml",
        )
