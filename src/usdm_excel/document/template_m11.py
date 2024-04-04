import re
from yattag import Doc
#from .elements import Elements
from .template_base import TemplateBase
#from usdm_excel.cross_ref import cross_references
from usdm_excel.base_sheet import BaseSheet

class TemplateM11(TemplateBase):

  def __init__(self, parent: BaseSheet, study):
    super().__init__(parent, study)

  def title_page(self):
    doc = Doc()
    with doc.tag('table'):
      self._title_page_entry(doc, 'Sponsor Confidentiality Statement:', '')
      self._title_page_entry(doc, 'Full Title:', f'{self.elements.study_full_title()}')
      self._title_page_entry(doc, 'Trial Acronym:', f'{self.elements.study_acronym()}')
      self._title_page_entry(doc, 'Protocol Identifier:', f'{self.elements.study_identifier()}')
      self._title_page_entry(doc, 'Original Protocol:', '')
      self._title_page_entry(doc, 'Version Number:', f'{self.elements.study_version_identifier()}')
      self._title_page_entry(doc, 'Version Date:', f'{self.elements.study_date()}')
      self._title_page_entry(doc, 'Amendment Identifier:', f'{self.elements.amendment()}')
      self._title_page_entry(doc, 'Amendment Scope:', f'{self.elements.amendment_scopes()}')
      self._title_page_entry(doc, 'Compound Codes(s):', '')
      self._title_page_entry(doc, 'Compound Name(s):', '')
      self._title_page_entry(doc, 'Trial Phase:', f'{self.elements.study_phase()}')
      self._title_page_entry(doc, 'Short Title:', f'{self.elements.study_short_title()}')
      self._title_page_entry(doc, 'Sponsor Name and Address:', f'{self.elements.organization_name_and_address()}')
      self._title_page_entry(doc, 'Regulatory Agency Identifier Number(s):', f'{self.elements.study_regulatory_identifiers()}')
      self._title_page_entry(doc, 'Spondor Approval Date:', f'{self.elements.approval_date()}')

      # Enter Nonproprietary Name(s)
      # Enter Proprietary Name(s)
      # Globally/Locally/Cohort
      # Primary Reason for Amendment
      # Region Identifier
      # Secondary Reason for Amendment

    result = doc.getvalue()
    #print(f"DOC: {result}")
    return result

  def inclusion(self):  
    return self._criteria("C25532")
  
  def exclusion(self):  
    return self._criteria("C25370")

  def objective_endpoints(self):
    #print(f"M11 TP:")
    doc = Doc()
    with doc.tag('table'):
      for item in self._objective_endpoints_list():
        self._objective_endpoints_entry(doc, item['objective'], item['endpoints'])
    return doc.getvalue()

  def _criteria(self, type):
    #print(f"M11 TP:")
    heading = { 
      'C25532': "Patients may be included in the study only if they meet <strong>all</strong> the following criteria:",
      'C25370': "Patients may be excluded in the study for <strong>any</strong> of the following reasons:",
    }
    doc = Doc()
    with doc.tag('p'):
      doc.asis(heading[type])  
    with doc.tag('table'):
      for criterion in self._criteria_list(type):
        self._critieria_entry(doc, criterion['identifier'], criterion['text'])
    return doc.getvalue()

  def _critieria_entry(self, doc, number, entry):
    with doc.tag('tr'):
      with doc.tag('td', style="vertical-align: top; text-align: left"):
        with doc.tag('p'):
          doc.asis(number)  
      with doc.tag('td', style="vertical-align: top; text-align: left"):
        with doc.tag('p'):
          doc.asis(entry)

  def _objective_endpoints_entry(self, doc, objective, endpoints):
    with doc.tag('tr'):
      with doc.tag('td', style="vertical-align: top; text-align: left"):
        with doc.tag('p'):
          doc.asis(objective)  
      with doc.tag('td', style="vertical-align: top; text-align: left"):
        for endpoint in endpoints:
          with doc.tag('p'):
            doc.asis(endpoint)

  def _title_page_entry(self, doc, title, entry):
    with doc.tag('tr'):
      with doc.tag('th', style="vertical-align: top; text-align: left"):
        with doc.tag('p'):
          doc.asis(title)  
      with doc.tag('td', style="vertical-align: top; text-align: left"):
        with doc.tag('p'):
          doc.asis(entry)

  def _criteria_list(self, type):
    results = []
    items = [c for c in self.study_design.population.criteria if c.category.code == type ]
    items.sort(key=lambda d: d.identifier)
    for item in items:
      result = {'identifier': item.identifier, 'text': self._reference(item, 'text')}
      results.append(result)
    return results

  def _objective_endpoints_list(self):
    results = []
    for item in self.study_design.objectives:
      result = {'objective': self._reference(item, 'text'), 'endpoints': []}
      for endpoint in item.endpoints:
        result['endpoints'].append(self._reference(endpoint, 'text'))
      results.append(result)
    return results
  