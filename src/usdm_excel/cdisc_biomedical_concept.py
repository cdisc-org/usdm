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
    if self._bc_items_exist():
      self.package_metadata = {} # Not needed other than to read items
      self.package_items = self._read_bc_items()
    else:
      self.package_metadata = self._get_package_metadata()
      self.package_items = self._get_package_items()
      self._save_bc_items(self.package_items)
    if self._bcs_exist():
      self._bc_responses = self._read_bcs()
    else:  
      self._bc_responses = {}

  def exists(self, name):
    name_uc = name.upper() # Avoid case mismatches
    if name_uc in self.package_items:
      return self.package_items[name_uc]
    else:
      return None

  def catalogue(self) -> list:
    return list(self.package_items.keys())
  
  def synonyms(self, name) -> list:
    metadata = self.exists(name)
    if not metadata:
      return []
    else:
      bc = self.usdm(name)
      return bc.bcSynonyms

  def to_cdisc_json(self, name) -> dict:
    metadata = self.exists(name)
    if not metadata:
      return {}
    else:
      return self._get_bc(metadata['href'])

  def to_usdm_json(self, name) -> dict:
    metadata = self.exists(name)
    if not metadata:
      return {}
    else:
      bc = self.usdm(name)
      return bc.to_json()

  def usdm(self, name) -> BiomedicalConcept:
    metadata = self.exists(name)
    if not metadata:
      return None
    else:
      response = self._get_bc(metadata['href'])
      #print(f"BC: {response}")
      bc = self._bc_as_usdm(response)
      if 'variables' in response:
        for item in response['variables']:
          codes = []
          if 'exampleSet' in item:
            for example in item['exampleSet']:
              term = cdisc_ct_library.preferred_term(example)
              if term != None:
                codes.append(CDISCCT().code(term['conceptId'], term['preferredTerm']))
          bc.properties.append(self._bc_property_as_usdm(item, codes))
      return bc

  def _get_package_metadata(self) -> dict:
    #api_url = self._url('/mdr/bc/packages')
    api_url = self._url('/mdr/specializations/sdtm/packages')
    package_logger.info("CDISC BC Library: %s" % api_url)
    try:
      raw = requests.get(api_url, headers=self.headers)
      response = raw.json()
      #print(f"PACKAGE: {response}")
      packages = response['_links']['packages']
      return packages
    except Exception as e:
      package_logger.error(f"Exception '{e}', failed to retrieve CDISC BC package metadata from '{api_url}'")
      package_logger.debug(f"{e}\n{traceback.format_exc()}")
      return {}

  def _get_package_items(self) -> dict:
    results = {}
    try:
      for package in self.package_metadata:
        api_url = self._url(package['href']) 
        package_logger.info("CDISC BC Library: %s" % api_url)
        raw = requests.get(api_url, headers=self.headers)
        response = raw.json()
        #print(f"ITEMS: {response}")
        for item in response['_links']['datasetSpecializations']:
          results[item['title'].upper()] = item
      return results
    except Exception as e:
      package_logger.error(f"Exception '{e}', failed to retrieve CDISC BC metadata from '{api_url}'")
      package_logger.debug(f"{e}\n{traceback.format_exc()}")
      return {}

  def _url(self, relative_url) -> str:
    return "%s%s" % (self.__class__.API_ROOT, relative_url)

  def _bc_as_usdm(self, api_bc) -> BiomedicalConcept:
    role_variable = self._get_role_variable(api_bc)
    code = NCIt().code(role_variable['assignedTerm']['conceptId'], role_variable['assignedTerm']['value'])
    synonyms = api_bc['synonyms'] if 'synonyms' in api_bc else []
    return BiomedicalConcept(
      id=id_manager.build_id(BiomedicalConcept),
      name=api_bc['shortName'],
      label=api_bc['shortName'],
      synonyms=synonyms,
      reference=api_bc['_links']['self']['href'],
      properties=[],
      code=Alias().code(code, [])
    )

  def _bc_property_as_usdm(self, property, codes) -> BiomedicalConceptProperty:
    print(f"PROPERTY: {property}")
    if 'dataElementConceptId' in property:
      concept_code = NCIt().code(property['dataElementConceptId'], property['name'])
    else:
      concept_code = NCIt().code(property['assignedTerm']['conceptId'], property['assignedTerm']['value'])
    concept_aliases = []
    responses = []
    for code in codes:
      responses.append(ResponseCode(id=id_manager.build_id(ResponseCode), isEnabled=True, code=code))
    return BiomedicalConceptProperty(
      id=id_manager.build_id(BiomedicalConceptProperty),
      name=property['name'],
      label=property['name'],
      isRequired=True,
      isEnabled=True,
      datatype=property['dataType'] if 'dataType' in property else '',
      responseCodes=responses,
      code=Alias().code(concept_code, concept_aliases)
    )

  def _get_role_variable(self, api_bc):
    return next((item for item in api_bc['variables'] if item["role"] == "Topic"), None)


  def _get_bc(self, url):
    if url in self._bc_responses:
      return self._bc_responses[url]
    else:
      api_url = self._url(url)
      raw = requests.get(api_url, headers=self.headers)
      result = raw.json()
      self._bc_responses[url] = result
      self._save_bcs(self._bc_responses)
      return result

  def _save_bc_items(self, data):
    try:
      if not self._bc_items_exist():
        with open(self._bc_items_filename(), 'w') as f:
          yaml.dump(data, f, indent=2, sort_keys=True)
    except Exception as e:
      package_logger.error(f"Exception '{e}', failed to save CDSIC BC items file")
      package_logger.debug(f"{e}\n{traceback.format_exc()}")

  def _read_bc_items(self):
    try:
      if self._bc_items_exist():
        with open(self._bc_items_filename()) as f:
          return yaml.load(f, Loader=yaml.FullLoader)
      else:
        package_logger.error(f"Failed to read CDSIC BC items file, does not exist")
        return None
    except Exception as e:
      package_logger.error(f"Exception '{e}', failed to read CDSIC BC items file")
      package_logger.debug(f"{e}\n{traceback.format_exc()}")

  def _bc_items_exist(self):
    return os.path.isfile(self._bc_items_filename()) 

  def _bc_items_filename(self):
    return os.path.join(os.path.dirname(__file__), 'data', f"cdisc_bc_items.yaml")

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