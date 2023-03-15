import requests
import os
from usdm_excel.cdisc_ct import cdisc_ct
from usdm_excel.ncit import NCIt
from usdm_excel.id_manager import IdManager
from usdm_excel.alias import Alias
from usdm.biomedical_concept import BiomedicalConcept
from usdm.biomedical_concept_property import BiomedicalConceptProperty
from usdm.response_code import ResponseCode
from usdm.alias_code import AliasCode

class CDISCBiomedicalConcepts():

  API_ROOT = 'https://api.library.cdisc.org/api'    
  
  def __init__(self, id_manager: IdManager):
    self.id_manager = id_manager
    self.api_key = os.getenv('CDISC_API_KEY')
    self.headers =  {"Content-Type":"application/json", "api-key": self.api_key}
    self.package_metadata = self._get_package_metadata()
    self.package_items = self._get_package_items()

  def exists(self, name):
    if name in self.package_items:
      return self.package_items[name]
    else:
      return None

  def catalogue(self):
    return list(self.package_items.keys())
  
  def usdm(self, name):
    metadata = self.exists(name)
    if not metadata:
      return None
    else:
      api_url = self._url(metadata['href'])
      raw = requests.get(api_url, headers=self.headers)
      response = raw.json()
      bc = self._bc_as_usdm(response)
      for item in response['dataElementConcepts']:
        codes = []
        if 'exampleSet' in item:
          for example in item['exampleSet']:
            term = cdisc_ct.preferred_term(example)
            codes.append(cdisc_ct.code(term['conceptId'], term['preferredTerm']))
        bc.bcProperties.append(self._bc_property_as_uasdm(item, codes))
      return bc

  def _get_package_metadata(self):
    api_url = self._url('/mdr/bc/packages')
    raw = requests.get(api_url, headers=self.headers)
    response = raw.json()
    packages = response['_links']['packages']
    return packages

  def _get_package_items(self):
    results = {}
    for package in self.package_metadata:
      api_url = self._url(package['href'])
      raw = requests.get(api_url, headers=self.headers)
      response = raw.json()
      for item in response['_links']['biomedicalConcepts']:
        results[item['title']] = item
    return results
    
  def _url(self, relative_url):
    return "%s%s" % (self.__class__.API_ROOT, relative_url)

  def _bc_as_usdm(self, api_bc):
    code = NCIt(self.id_manager).code(api_bc['conceptId'], api_bc['shortName'])
    aliases = []
    return BiomedicalConcept(
      biomedicalConceptId=self.id_manager.build_id(BiomedicalConcept),
      bcName=api_bc['shortName'],
      bcSynonyms=api_bc['synonym'],
      bcReference=api_bc['_links']['self']['href'],
      bcProperties=[],
      bcConceptCode=Alias(self.id_manager).code(code, aliases)
    )

  def _bc_property_as_uasdm(self, property, codes):
    code = NCIt(self.id_manager).code(property['conceptId'], property['shortName'])
    aliases = []
    responses = []
    for code in codes:
      responses.append(ResponseCode(responseCodeId=self.id_manager.build_id(ResponseCode), responseCodeEnabled=True, code=code))
    return BiomedicalConceptProperty(
      bcPropertyId=self.id_manager.build_id(BiomedicalConceptProperty),
      bcPropertyName=property['shortName'],
      bcPropertyRequired=True,
      bcPropertyEnabled=True,
      bcPropertyDatatype=property['dataType'],
      bcPropertyResponseCodes=responses,
      bcPropertyConceptCode=Alias(self.id_manager).code(code, aliases)
    )
