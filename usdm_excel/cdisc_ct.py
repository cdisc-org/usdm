from usdm_excel.id_manager import IdManager
from usdm.code import Code
import requests
import os
import yaml

class NoManager(Exception):
    pass

class CDISCCT():

  API_ROOT = 'https://api.library.cdisc.org/api'  

  def __init__(self):
    self.id_manager = None
    f = open('data/cdisc_ct_config.yml', 'r')
    self.cdisc_ct_config = yaml.load(f, Loader=yaml.FullLoader)
    self.api_key = os.getenv('CDISC_API_KEY')
    self.headers =  {"Content-Type":"application/json", "api-key": self.api_key}
    self._by_code_list = {}
    self._by_term = {}
    self._by_submission = {}
    self._by_pt = {}
    self._get_ct()

  @property
  def id_manager(self):
    return self._id_manager

  @id_manager.setter
  def id_manager(self, value: IdManager):
    self._id_manager = value

  def code(self, code, decode):
    if self._id_manager == None:
      raise NoManager 
    else: 
      return Code(codeId=self._id_manager.build_id(Code), code=code, codeSystem="http://www.cdisc.org", codeSystemVersion="2022-12-16", decode=decode)
  
  def submission(self, value):
    if value in self._by_submission:
      concept_id = self._by_submission[value]
      code_list = self._by_code_list[concept_id]
      return next((item for item in code_list if item["submissionValue"] == value), None)
    
  def preferred_term(self, value):
    if value in self._by_submission:
      concept_id = self._by_pt[value]
      code_list = self._by_code_list[concept_id]
      return next((item for item in code_list if item["preferredTerm"] == value), None)

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
        self._by_code_list[response['conceptId']] = response
        for item in response['terms']:
          self._check_in_and_add(self._by_term, item['conceptId'], response['conceptId'])
          self._check_in_and_add(self._by_submission, item['submissionValue'], response['conceptId'])
          self._check_in_and_add(self._by_pt, item['preferredTerm'], response['conceptId'])
      else:
        print("c_code", c_code, api_url, raw.status_code)

  def _url(self, relative_url):
    return "%s%s" % (self.__class__.API_ROOT, relative_url)

  def _check_in_and_add(self, collection, id, item):
    if not id in collection:
      collection[id] = []
    collection[id].append(item)

cdisc_ct = CDISCCT()