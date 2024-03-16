from usdm_excel.cdisc_ct import CDISCCT
from usdm_excel.cdisc_ct_library import cdisc_ct_library
from usdm_excel.ncit import NCIt
from usdm_excel.id_manager import id_manager
from usdm_excel.alias import Alias
from usdm_model.biomedical_concept import BiomedicalConcept
from usdm_model.biomedical_concept_property import BiomedicalConceptProperty
from usdm_model.response_code import ResponseCode
from usdm_model.alias_code import AliasCode
from usdm_excel.logger import package_logger

import os
import yaml
import requests
import traceback

class CDISCBiomedicalConcepts():

  API_ROOT = 'https://api.library.cdisc.org/api/cosmos/v2'    
  
  def __init__(self):
    self.api_key = os.getenv('CDISC_API_KEY')
    self.headers =  {"Content-Type":"application/json", "api-key": self.api_key}
    self._package_metadata = {}
    self._package_items = {}
    self._bc_responses = {}
    self._bcs = {}
    self._bcs_raw = {}
    self._bc_index = {}
    if self._bcs_exist():
      self._bcs = self._load_bcs()
    else:
      self._package_metadata = self._get_package_metadata()
      self._package_items = self._get_package_items()
      self._bcs, self._bcs_raw = self._get_bcs()
      self._save_bcs(self._bcs_raw)
    self._bc_index = self._create_bc_index()

  def exists(self, name):
    return True if name.upper() in self._bc_index else False

  def catalogue(self) -> list:
    return list(self._bcs.keys())
  
  def usdm(self, name) -> BiomedicalConcept:
    return self._get_bc_data(name) if self.exists(name) else None

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
  
  def _get_package_metadata(self) -> dict:
    try:
      api_url = self._url('/mdr/specializations/sdtm/packages')
      package_logger.info("CDISC BC Library: %s" % api_url)
      raw = requests.get(api_url, headers=self.headers)
      response = raw.json()
      packages = response['_links']['packages']
    except Exception as e:
      self._exception(f"Exception '{e}', failed to retrieve CDISC BC package metadata from '{api_url}'", e)
      packages = {}
    package_logger.debug(f"PACKAGES: {packages}")
    return packages
        
  def _get_package_items(self) -> dict:
    results = {}
    try:
      #for package in self._package_metadata:
        package = self._package_metadata[-1]
        api_url = self._url(package['href']) 
        package_logger.info("CDISC BC Library: %s" % api_url)
        raw = requests.get(api_url, headers=self.headers)
        response = raw.json()
        package_logger.debug(f"ITEMS: {response}")
        for item in response['_links']['datasetSpecializations']:
          key = item['title'].upper()
          results[key] = item
        return results
    except Exception as e:
      self._exception(f"Exception '{e}', failed to retrieve CDISC BC metadata from '{api_url}'", e)
      return {}

  def _get_bcs(self):
    results = {}
    raw_results = {}
    for name, item in self._package_items.items():
      sdtm, generic = self._get_from_url_all(name)
      if sdtm:
        bc = self._bc_as_usdm(sdtm, generic)
        if bc:
          if 'variables' in sdtm:
            for item in sdtm['variables']:
                property = self._bc_property_as_usdm(item, generic)
                if property:
                  bc.properties.append(property)
          raw_results[name] = bc.model_dump()
          results[name] = bc
    return results, raw_results
  
  def _bc_as_usdm(self, sdtm, generic) -> BiomedicalConcept:
    try:
      if self._process_bc(sdtm['shortName']):
        package_logger.debug(f"BC: {sdtm}\n\n{generic}")
        role_variable = self._get_role_variable(sdtm)
        if role_variable:
          if 'assignedTerm' in role_variable:
            print(f"ASSIGNED TERM: {role_variable['assignedTerm']}")
            if 'conceptId' in role_variable['assignedTerm'] and 'value' in role_variable['assignedTerm']:
              code = NCIt().code(role_variable['assignedTerm']['conceptId'], role_variable['assignedTerm']['value'])
            else:
              code = NCIt().code('No Concept Code', role_variable['assignedTerm']['value'])
          else:
            code = NCIt().code(generic['conceptId'], generic['shortName'])
        else:
          package_logger.error(f"Failed to set BC concept {sdtm}\n\n{generic}")
          code = NCIt().code(generic['conceptId'], generic['shortName'])
        synonyms = generic['synonyms'] if 'synonyms' in generic else []
        synonyms.append(generic['shortName'])
        return BiomedicalConcept(
          id=id_manager.build_id(BiomedicalConcept),
          name=sdtm['shortName'],
          label=sdtm['shortName'],
          synonyms=synonyms,
          reference=sdtm['_links']['self']['href'],
          properties=[],
          code=Alias().code(code, [])
        )
      else:
        return None
    except Exception as e:
      self._exception(f"Exception '{e}', failed to build BC \n{sdtm['shortName']}", e)
      return None

  def _bc_property_as_usdm(self, sdtm_property, generic) -> BiomedicalConceptProperty:
    try:
      package_logger.info(f"NAME: {sdtm_property['name']}, {sdtm_property['name'][2:]}")
      if self._process_property(sdtm_property['name']):
        package_logger.debug(f"PROPERTY: {sdtm_property}")
        if 'dataElementConceptId' in sdtm_property:
          generic_match = self._get_dec_match(generic, sdtm_property['dataElementConceptId'])
          if generic_match:
            concept_code = NCIt().code(generic_match['conceptId'], generic_match['shortName'])
          else:
            #package_logger.error(f"Failed to set property concept {sdtm_property}\n\n{generic}")
            concept_code = NCIt().code(sdtm_property['dataElementConceptId'], sdtm_property['name'])
        else:
          if 'assignedTerm' in sdtm_property:
            concept_code = NCIt().code(sdtm_property['assignedTerm']['conceptId'], sdtm_property['assignedTerm']['value'])
          else:
            concept_code = None
        concept_aliases = []
        responses = []
        codes = []
        if 'valueList' in sdtm_property:
          for value in sdtm_property['valueList']:
            term = cdisc_ct_library.preferred_term(value)
            if term:
              codes.append(CDISCCT().code(term['conceptId'], term['preferredTerm']))
            else:
              term = cdisc_ct_library.submission(value)
              if term:
                codes.append(CDISCCT().code(term['conceptId'], term['preferredTerm']))
              else:
                cl = f", code list {sdtm_property['codelist']['conceptId'] if 'codelist' in sdtm_property else '<not defined>'}"
                package_logger.error(f"Failed to find submission or preferred term '{value}' {cl}")
        for code in codes:
         responses.append(ResponseCode(id=id_manager.build_id(ResponseCode), isEnabled=True, code=code))
        return BiomedicalConceptProperty(
          id=id_manager.build_id(BiomedicalConceptProperty),
          name=sdtm_property['name'],
          label=sdtm_property['name'],
          isRequired=True,
          isEnabled=True,
          datatype=sdtm_property['dataType'] if 'dataType' in sdtm_property else '',
          responseCodes=responses,
          code=Alias().code(concept_code, concept_aliases)
        )
      else:
        return None
    except Exception as e:
      self._exception(f"Exception '{e}', failed to build property {sdtm_property}", e)
      return None

  def _process_bc(self, name):
    if name in [
      'Exclusion Criteria 01', 'Inclusion Criteria 01', "Medical History Prespecified: Alzheimer's Disease", "Medical History Prespecified: Confusional Episodes", 
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
      "Wine Use History"
    ]:
      return False
    return True
  
  def _process_property(self, name):
    if name[2:] in ['TEST', 'STRESN', 'STRESU', 'STRESC', 'CLASCD', 'LOINC', 'LOT', 'CAT', 'SCAT']:
      return False
    if name in ['EPOCH']:
      return False
    return True
 
  def _get_role_variable(self, data):
    return next((item for item in data['variables'] if item["role"] == "Topic"), None)

  def _get_dec_match(self, data, id):
    return next((item for item in data['dataElementConcepts'] if item["conceptId"] == id), None)

  def _get_from_url_all(self, name) -> dict:
    try:
      item = self._package_items[name]
      package_logger.debug(f"{item}")
      sdtm_response = self._get_from_url(item['href'])
      generic = sdtm_response["_links"]["parentBiomedicalConcept"]
      generic_response = self._get_from_url(generic['href'])
      return sdtm_response, generic_response
    except Exception as e:
      self._exception(f"Exception '{e}', failed to retrieve CDISC BC metadata from '{item['href']}'", e)
      return None, None

  def _get_from_url(self, url):
    api_url = self._url(url)
    raw = requests.get(api_url, headers=self.headers)
    result = raw.json()
    return result

  def _url(self, relative_url) -> str:
    return "%s%s" % (self.__class__.API_ROOT, relative_url)

  def _save_bcs(self, data):
    try:
      with open(self._bcs_filename(), 'w') as f:
        yaml.dump(data, f, indent=2, sort_keys=True)
    except Exception as e:
      self._exception(f"Exception '{e}', failed to save CDSIC BC file", e)

  def _read_bcs(self):
    try:
      if self._bcs_exist():
        with open(self._bcs_filename()) as f:
          return yaml.load(f, Loader=yaml.FullLoader)
      else:
        package_logger.error(f"Failed to read CDSIC BC file, does not exist")
        return None
    except Exception as e:
      self._exception(f"Exception '{e}', failed to read CDSIC CT file", e)

  def _bcs_exist(self):
    return os.path.isfile(self._bcs_filename()) 

  def _bcs_filename(self):
    return os.path.join(os.path.dirname(__file__), 'data', f"cdisc_bcs.yaml")

  def _exception(self, message, e):
    package_logger.error(message)
    package_logger.error(f"{e}\n{traceback.format_exc()}")

cdisc_bc_library = CDISCBiomedicalConcepts()