from usdm_excel.id_manager import IdManager
from usdm.code import Code
import requests
import os
import yaml

class CDISCCTLibrary():

  API_ROOT = 'https://api.library.cdisc.org/api'  

  def __init__(self):
    f = open('data/cdisc_ct_config.yml', 'r')
    self.cdisc_ct_config = yaml.load(f, Loader=yaml.FullLoader)
    self.api_key = os.getenv('CDISC_API_KEY')
    self.headers =  {"Content-Type":"application/json", "api-key": self.api_key}
    self._by_code_list = {}
    self._by_term = {}
    self._by_submission = {}
    self._by_pt = {}
    self._get_ct()

  def submission(self, value):
    if value in list(self._by_submission.keys()):
      print("S1")
      concept_ids = self._by_submission[value]
      if len(concept_ids) == 0:
        return None
      elif len(concept_ids) == 1:
        code_list = self._by_code_list[concept_ids[0]]
        return next((item for item in code_list['terms'] if item["submissionValue"] == value), None)
      else:
        return None 
    
  def preferred_term(self, value):
    if value in list(self._by_pt.keys()):
      concept_ids = self._by_pt[value]
      if len(concept_ids) == 0:
        return None
      elif len(concept_ids) == 1:
        code_list = self._by_code_list[concept_ids[0]]
        return next((item for item in code_list['terms'] if item["preferredTerm"] == value), None)
      else:
        return None 

  def _get_ct(self):
    for item in self.cdisc_ct_config['required']:
      self._get_code_list(item)

  def _get_code_list(self, c_code):
    for package in self.cdisc_ct_config['packages']:
      api_url = self._url('/mdr/ct/packages/%s/codelists/%s' % (package, c_code))
      raw = requests.get(api_url, headers=self.headers)
      if raw.status_code == 200:
        response = raw.json()
        response.pop('_links', None)
#        if c_code == 'C99077':
#          print("Response:", response)
        self._by_code_list[response['conceptId']] = response
        for item in response['terms']:
          self._check_in_and_add(self._by_term, item['conceptId'], response['conceptId'])
          self._check_in_and_add(self._by_submission, item['submissionValue'], response['conceptId'])
          self._check_in_and_add(self._by_pt, item['preferredTerm'], response['conceptId'])
        return
    print("Failed to find:", c_code)

  def _url(self, relative_url):
    return "%s%s" % (self.__class__.API_ROOT, relative_url)

  def _check_in_and_add(self, collection, id, item):
    if not id in collection:
      collection[id] = []
    collection[id].append(item)

cdisc_ct_library = CDISCCTLibrary()