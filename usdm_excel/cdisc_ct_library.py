from usdm_excel.id_manager import IdManager
from usdm.code import Code
import requests
import os
import yaml

class CDISCCTLibrary():

  API_ROOT = 'https://api.library.cdisc.org/api'  
  HEADERS = { "Content-Type":"application/json", "api-key": os.getenv('CDISC_API_KEY') }
    
  def __init__(self):
    f = open('data/cdisc_ct_config.yml', 'r')
    self.cdisc_ct_config = yaml.load(f, Loader=yaml.FullLoader)
    #print("CONFIG:", self.cdisc_ct_config)
    self.version = self.cdisc_ct_config['version']
    self.system = "http://www.cdisc.org"
    #print("CONFIG:", self.version, self.system)
    self.api_key = os.getenv('CDISC_API_KEY')
    self._by_code_list = {}
    self._by_term = {}
    self._by_submission = {}
    self._by_pt = {}
    self._by_klass_attribute = {}
    self._get_ct()
    self._get_klass_attribute()

  def submission(self, value):
    if value in list(self._by_submission.keys()):
      #print("S1")
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

  def klass_and_attribute(self, klass, attribute, value):
    #print("K&A 1:", klass, attribute)
    try:
      concept_id = self._by_klass_attribute[klass][attribute]
      code_list = self._by_code_list[concept_id]
      #print("K&A 2:", code_list)
      #print("K&A 3:", value)
      for field in [ 'conceptId', 'preferredTerm', 'submissionValue']:
        result = next((item for item in code_list['terms'] if item[field].upper() == value.upper()), None)
        if result != None:
          #print("K&A 4:", result)
          return result
      #print("K&A 5:")
      return None
    except Exception as e: 
      #print("K&A 6:", e)
      return None
    
  def _get_ct(self):
    for item in self.cdisc_ct_config['required']:
      self._get_code_list(item)

  def _get_klass_attribute(self):
    for klass, info in self.cdisc_ct_config['klass'].items():
      #print("KLASS:", klass, info)
      if not klass in self._by_klass_attribute:
        self._by_klass_attribute[klass] = {}
      for attribute, cl in info.items():
        if not attribute in self._by_klass_attribute[klass]:
          self._by_klass_attribute[klass][attribute] = cl

  def _get_code_list(self, c_code):
    for package in self.cdisc_ct_config['packages']:
      package_full_name = "%sct-%s" % (package, self.version)
      api_url = self._url('/mdr/ct/packages/%s/codelists/%s' % (package_full_name, c_code))
      print("URL:", api_url)
      raw = requests.get(api_url, headers=self.__class__.HEADERS)
      if raw.status_code == 200:
        response = raw.json()
        #if c_code == "C188726":
        #  print(response)
        response.pop('_links', None)
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