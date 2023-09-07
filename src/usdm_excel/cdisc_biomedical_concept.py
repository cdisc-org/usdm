import requests
import os
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

class CDISCBiomedicalConcepts():

  API_ROOT = 'https://api.library.cdisc.org/api/cosmos/v2'    
  
  def __init__(self):
    self.api_key = os.getenv('CDISC_API_KEY')
    self.headers =  {"Content-Type":"application/json", "api-key": self.api_key}
    self.package_metadata = self._get_package_metadata()
    self.package_items = self._get_package_items()
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
      bc = self._bc_as_usdm(response)
      if 'dataElementConcepts' in response:
        for item in response['dataElementConcepts']:
          codes = []
          if 'exampleSet' in item:
            for example in item['exampleSet']:
              term = cdisc_ct_library.preferred_term(example)
              if term != None:
                codes.append(CDISCCT().code(term['conceptId'], term['preferredTerm']))
          bc.bcProperties.append(self._bc_property_as_usdm(item, codes))
      return bc

  def _get_package_metadata(self) -> dict:
    api_url = self._url('/mdr/bc/packages')
    package_logger.info("CDISC BC Library: %s" % api_url)
    try:
      raw = requests.get(api_url, headers=self.headers)
      response = raw.json()
      packages = response['_links']['packages']
      return packages
    except:
      package_logger.info("CDISC BC Library FAILED: %s" % api_url)
      return {}

  def _get_package_items(self) -> dict:
    results = {}
    try:
      for package in self.package_metadata:
        api_url = self._url(package['href']) 
        package_logger.info("CDISC BC Library: %s" % api_url)
        raw = requests.get(api_url, headers=self.headers)
        response = raw.json()
        for item in response['_links']['biomedicalConcepts']:
          results[item['title'].upper()] = item
      return results
    except:
      results = {}

  def _url(self, relative_url) -> str:
    return "%s%s" % (self.__class__.API_ROOT, relative_url)

  def _bc_as_usdm(self, api_bc) -> BiomedicalConcept:
    code = NCIt().code(api_bc['conceptId'], api_bc['shortName'])
    synonyms = api_bc['synonyms'] if 'synonyms' in api_bc else []
    return BiomedicalConcept(
      id=id_manager.build_id(BiomedicalConcept),
      name=api_bc['shortName'],
      label=api_bc['shortName'],
      bcSynonyms=synonyms,
      bcReference=api_bc['_links']['self']['href'],
      bcProperties=[],
      code=Alias().code(code, [])
    )

  def _bc_property_as_usdm(self, property, codes) -> BiomedicalConceptProperty:
    concept_code = NCIt().code(property['conceptId'], property['shortName'])
    concept_aliases = []
    responses = []
    for code in codes:
      responses.append(ResponseCode(id=id_manager.build_id(ResponseCode), responseCodeEnabled=True, code=code))
    return BiomedicalConceptProperty(
      id=id_manager.build_id(BiomedicalConceptProperty),
      name=property['shortName'],
      label=property['shortName'],
      bcPropertyRequired=True,
      bcPropertyEnabled=True,
      bcPropertyDatatype=property['dataType'],
      bcPropertyResponseCodes=responses,
      code=Alias().code(concept_code, concept_aliases)
    )

  def _get_bc(self, url):
    if url in self._bc_responses:
      return self._bc_responses[url]
    else:
      api_url = self._url(url)
      raw = requests.get(api_url, headers=self.headers)
      result = raw.json()
      self._bc_responses[url] = result
      return result

cdisc_bc_library = CDISCBiomedicalConcepts()