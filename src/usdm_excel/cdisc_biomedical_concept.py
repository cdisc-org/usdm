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
  
  # def synonyms(self, name) -> list:
  #   metadata = self.exists(name)
  #   if not metadata:
  #     return []
  #   else:
  #     # ToDo, needs a tweak
  #     bc = self.usdm(name)
  #     return bc.bcSynonyms

  # # Not sure used anymore?
  # def to_cdisc_json(self, name) -> dict:
  #   metadata = self.exists(name)
  #   if not metadata:
  #     return {}
  #   else:
  #     sdtm_response, generic_response = self._get_from_url_both(metadata['href'])
  #     return sdtm_response

  # def to_usdm_json(self, name) -> dict:
  #   metadata = self.exists(name)
  #   return metadata if metadata else {}
  #     return {}
  #   else:
  #     bc = self.usdm(name)
  #     return bc.to_json()

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
      package_logger.error(f"Exception '{e}', failed to retrieve CDISC BC package metadata from '{api_url}'")
      package_logger.debug(f"{e}\n{traceback.format_exc()}")
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
      package_logger.error(f"Exception '{e}', failed to retrieve CDISC BC metadata from '{api_url}'")
      package_logger.debug(f"{e}\n{traceback.format_exc()}")
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
      package_logger.debug(f"BC: {sdtm}\n\n{generic}")
      role_variable = self._get_role_variable(sdtm)
      code = NCIt().code(role_variable['assignedTerm']['conceptId'], role_variable['assignedTerm']['value'])
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
    except Exception as e:
      package_logger.error(f"Exception '{e}', failed to build BC \n'{sdtm}'\n\n{generic}")
      package_logger.debug(f"{e}\n{traceback.format_exc()}")
      return None

  def _bc_property_as_usdm(self, sdtm_property, generic) -> BiomedicalConceptProperty:
    try:
      if sdtm_property['name'][2:-1] not in ['TEST', 'STRESN', 'STRESU']:
        package_logger.debug(f"PROPERTY: {sdtm_property}")
        if 'dataElementConceptId' in sdtm_property:
          generic_match = self._get_dec_match(generic, sdtm_property['dataElementConceptId'])
          concept_code = NCIt().code(generic_match['conceptId'], generic_match['shortName'])
        else:
          concept_code = NCIt().code(sdtm_property['assignedTerm']['conceptId'], sdtm_property['assignedTerm']['value'])
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
                package_logger.error(f"Failed to find submission 7 preferred term '{value}'")
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
      package_logger.error(f"Exception '{e}', failed to build property '{sdtm_property}'")
      package_logger.debug(f"{e}\n{traceback.format_exc()}")
      return None

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
      package_logger.error(f"Exception '{e}', failed to retrieve CDISC BC metadata from '{item['href']}'")
      package_logger.debug(f"{e}\n{traceback.format_exc()}")
      return None, None

  def _get_from_url(self, url):
    # if url in self._bc_responses:
    #   return self._bc_responses[url]
    # else:
    api_url = self._url(url)
    raw = requests.get(api_url, headers=self.headers)
    result = raw.json()
    #self._bc_responses[url] = result
    #self._save_bcs(self._bc_responses)
    return result

  def _url(self, relative_url) -> str:
    return "%s%s" % (self.__class__.API_ROOT, relative_url)

  # def _save_bc_items(self, data):
  #   try:
  #     if not self._bc_items_exist():
  #       with open(self._bc_items_filename(), 'w') as f:
  #         yaml.dump(data, f, indent=2, sort_keys=True)
  #   except Exception as e:
  #     package_logger.error(f"Exception '{e}', failed to save CDSIC BC items file")
  #     package_logger.debug(f"{e}\n{traceback.format_exc()}")

  # def _read_bc_items(self):
  #   try:
  #     if self._bc_items_exist():
  #       with open(self._bc_items_filename()) as f:
  #         return yaml.load(f, Loader=yaml.FullLoader)
  #     else:
  #       package_logger.error(f"Failed to read CDSIC BC items file, does not exist")
  #       return None
  #   except Exception as e:
  #     package_logger.error(f"Exception '{e}', failed to read CDSIC BC items file")
  #     package_logger.debug(f"{e}\n{traceback.format_exc()}")

  # def _bc_items_exist(self):
  #   return os.path.isfile(self._bc_items_filename()) 

  # def _bc_items_filename(self):
  #   return os.path.join(os.path.dirname(__file__), 'data', f"cdisc_bc_items.yaml")

  def _save_bcs(self, data):
    try:
      with open(self._bcs_filename(), 'w') as f:
        yaml.dump(data, f, indent=2, sort_keys=True)
    except Exception as e:
      package_logger.error(f"Exception '{e}', failed to save CDSIC BC file")
      package_logger.debug(f"{e}\n{traceback.format_exc()}")

  def _read_bcs(self):
    try:
      if self._bcs_exist():
        with open(self._bcs_filename()) as f:
          return yaml.load(f, Loader=yaml.FullLoader)
      else:
        package_logger.error(f"Failed to read CDSIC BC file, does not exist")
        return None
    except Exception as e:
      package_logger.error(f"Exception '{e}', failed to read CDSIC CT file")
      package_logger.debug(f"{e}\n{traceback.format_exc()}")

  def _bcs_exist(self):
    return os.path.isfile(self._bcs_filename()) 

  def _bcs_filename(self):
    return os.path.join(os.path.dirname(__file__), 'data', f"cdisc_bcs.yaml")

cdisc_bc_library = CDISCBiomedicalConcepts()