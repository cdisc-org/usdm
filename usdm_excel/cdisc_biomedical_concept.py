import requests
import os
from usdm_excel.cdisc_ct import cdisc_ct

class CDISCBiomedicalConcepts():

  API_ROOT = 'https://api.library.cdisc.org/api'    
  
  def __init__(self):
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
      for item in response['dataElementConcepts']:
        if 'exampleSet' in item:
          for example in item['exampleSet']:
            print("S ", cdisc_ct.submission(example))
            print("PT", cdisc_ct.preferred_term(example))
      return response

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


