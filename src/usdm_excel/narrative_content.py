from yattag import Doc
from bs4 import BeautifulSoup   
from usdm_excel.cross_ref import cross_references
from usdm_excel.logger import logging
import docraptor
import re

class NarrativeContent():

  class LogicError(Exception):
    pass

  def __init__(self, doc_title, study):
    self.study = study
    self.study_version = study.versions[0]
    self.study_design = self.study_version.studyDesigns[0]
    self.protocol_document_version = self.study.documentedBy.versions[0]
    self.doc_title = doc_title
    if self.protocol_document_version.id != self.study.versions[0].documentVersionId:
      logging.error(f"Failed to initialise NarrativeContent for document creation, ids did not match")
      raise self.LogicError(f"Failed to initialise NarrativeContent for document creation, ids did not match")

  def to_pdf(self):
    doc_api = docraptor.DocApi()
    doc_api.api_client.configuration.username = 'YOUR_API_KEY_HERE'

    document_content = self.to_html()
    try:
      response = doc_api.create_doc({
        'test': True,  # test documents are free but watermarked
        'document_type': 'pdf',
        'document_content': document_content,
        # 'document_url': 'https://docraptor.com/examples/invoice.html',
        # 'javascript': True,
        # 'prince_options': # {
        #    'media': 'print', # @media 'screen' or 'print' CSS
        #    'baseurl': 'https://yoursite.com', # the base URL for any relative URLs
        # },
      })
      binary_formatted_response = bytearray(response)
      return binary_formatted_response
    except docraptor.rest.ApiException as error:
      pass
      #print(error.status)
      #print(error.reason)
      #print(error.body)

  def to_html(self):
    root = self.protocol_document_version.contents[0]
    doc = Doc()
    doc.asis('<!DOCTYPE html>')
    style = """
      /* Create a running element */
      #header-and-footer {
        position: running(header-and-footer);
        text-align: right;
      }

      /* Add that running element to the top and bottom of every page */
      @page {
        @top {
          content: element(header-and-footer);
        }
        @bottom {
          content: element(header-and-footer);
        }
      }

      /* Add a page number */
      #page-number {
        content: "Page " counter(page);
      }

      /* Create a title page with a full-bleed background and no header */
      #title-page {
        page: title-page;
      }

      @page title-page {
        @top {
          content: "";
        }
      }

      #title-page h1 {
        padding: 200px 0 40px 0;
        font-size: 30px;
      }

      /* Dynamically create a table of contents with leaders */
      #table-of-contents a {
        content: target-content(attr(href)) leader('.') target-counter(attr(href), page);
        color: #000000;
        text-decoration: none;
        display: block;
        padding-top: 5px;
      }

      /* Float the footnote to a footnotes area on the page */
      .footnote {
        float: footnote;
        font-size: small;
      }

      .page {
        page-break-after: always;
      }

      body {
        counter-reset: chapter;
        font-family: 'Times New Roman';
        color: #000000;
      }
    </style>
    <link href='https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;800&display=swap' rel='stylesheet'>
    """
    chapters = []
    for id in root.contentChildIds:
      content = next((x for x in self.protocol_document_version.contents if x.id == id), None)
      level = len(content.sectionNumber.split('.'))
      if level == 1:
        chapters.append(f'<a href="#section-{content.sectionNumber}"></a>')
    front_sheet = f"""
      <div id="title-page" class="page">
        <h1>{self.doc_title}</h1>
        <div id="header-and-footer">
          <span id="page-number"></span>
        </div>
      </div>
      <div id="toc-page" class="page">
        <div id="table-of-contents">
          {''.join(chapters)}
        </div>
        <div id="header-and-footer">
          <span id="page-number"></span>
        </div>
      </div>
    """
    with doc.tag('html'):
      with doc.tag('head'):
        with doc.tag('style'):
          doc.asis(style)      
      with doc.tag('body'):
        doc.asis(front_sheet)    
        for id in root.contentChildIds:
          content = next((x for x in self.protocol_document_version.contents if x.id == id), None)
          if content:
            self._content_to_html(content, doc)
    return doc.getvalue()
  
  def _content_to_html(self, content, doc):
    level = len(content.sectionNumber.split('.'))
    klass = "page" if level == 1 else ""
    id = f"section-{content.sectionNumber}"
    with doc.tag('div', klass=klass):
      with doc.tag(f'h{level}', id=id):
        doc.asis(f"{content.sectionNumber}&nbsp{content.sectionTitle}")
      if self._standard_section(content.text):
        #print(f"STD1 {content.text}")
        name = self._standard_section_name(content.text)
        #print(f"STD2 {name}")
        content.text = self._generate_standard_section(name)
        #print(f"STD3 {content.text}")
      doc.asis(self._translate_references(content.text))
      for id in content.contentChildIds:
        content = next((x for x in self.protocol_document_version.contents if x.id == id), None)
        self._content_to_html(content, doc)

  def _translate_references(self, content_text):
    soup = BeautifulSoup(content_text, 'html.parser')
    for ref in soup(['usdm:ref']):
      #print(f"TRA: {ref}")
      attributes = ref.attrs
      #print(f"TRB: {attributes}")
      try:
        if 'namexref' in attributes:
          instance = cross_references.get(attributes['klass'], attributes['namexref'])
        else:
          instance = cross_references.get_by_id(attributes['klass'], attributes['id'])
        try:
          #print(f"TR1: {instance.id}")
          value = getattr(instance, attributes['attribute'])
          #print(f"TR2: {value}")
          translated_text = self._translate_references(value)
          #print(f"TR3: {translated_text}")
          ref.replace_with(translated_text)
        except:
          ref.replace_with("***** Failed to translate reference, attribute not found *****")
      except:
        ref.replace_with("***** Failed to translate reference, instance not found *****")
    return str(soup)
  
  def _standard_section(self, text):
    soup = BeautifulSoup(text, 'html.parser')
    for section in soup(['usdm:section']):
      return True
    return False
  
  def _standard_section_name(self, text):  
    soup = BeautifulSoup(text, 'html.parser')
    for section in soup(['usdm:section']):
      attributes = section.attrs
      if 'name' in attributes:
        return attributes['name'].upper()
      else:
        return None
    return None

  def _generate_standard_section(self, name):
    #print(f"GSS: {name}")   
    if name == "M11-TITLE-PAGE":
      return self._generate_m11_title_page()
    elif name == "M11-INCLUSION":
      return self._generate_m11_criteria("C25532")
    elif name == "M11-EXCLUSION":
      return self._generate_m11_criteria("C25370")
    elif name == "M11-OBJECTIVE-ENDPOINTS":
      return self._generate_m11_objective_endpoints()
    else:
      return f"Unrecognized standard content name {name}"

  def _generate_m11_title_page(self):
    #print(f"M11 TP:")
    doc = Doc()
    with doc.tag('table'):
      self._generate_m11_title_page_entry(doc, 'Sponsor Confidentiality Statement:', '', 'Enter Sponsor Confidentiality Statement')
      self._generate_m11_title_page_entry(doc, 'Full Title:', f'<usdm:ref klass="StudyProtocolDocumentVersion" id="{self.protocol_document_version.id}" attribute="officialTitle"/>', 'Enter Full Title')
      self._generate_m11_title_page_entry(doc, 'Trial Acronym:', f'<usdm:ref klass="StudyVersion" id="{self.study_version.id}" attribute="studyAcronym"/>', 'Enter trial Acronym')
      self._generate_m11_title_page_entry(doc, 'Protocol Identifier:', f'<usdm:ref klass="StudyIdentifier" id="{self._study_identifier().id}" attribute="studyIdentifier"/>', 'Enter Protocol Identifier')
      self._generate_m11_title_page_entry(doc, 'Original Protocol:', '', 'Original protocol')
      self._generate_m11_title_page_entry(doc, 'Version Number:', f'<usdm:ref klass="StudyVersion" id="{self.study_version.id}" attribute="studyVersion"/>', 'Enter Version Number')
      self._generate_m11_title_page_entry(doc, 'Version Date:', '', 'Enter Version Date')
      self._generate_m11_title_page_entry(doc, 'Amendment Identifier:', f'<usdm:ref klass="StudyAmendment" id="{self._amendment().id}" attribute="number"/>', 'Amendment Identifier')
      self._generate_m11_title_page_entry(doc, 'Amendment Scope:', '', 'Amendment Scope')
      self._generate_m11_title_page_entry(doc, 'Compound Codes(s):', '', 'Enter Compound Code(s)')
      self._generate_m11_title_page_entry(doc, 'Compound Name(s):', '')
      self._generate_m11_title_page_entry(doc, 'Trial Phase:', f'<usdm:ref klass="Code" id="{self.study_version.studyPhase.standardCode.id}" attribute="decode"/>', 'Trial Phase')
      self._generate_m11_title_page_entry(doc, 'Short Title:', f'<usdm:ref klass="StudyProtocolDocumentVersion" id="{self.protocol_document_version.id}" attribute="briefTitle"/>', 'Enter Trial Short Title')
      self._generate_m11_title_page_entry(doc, 'Sponsor Name and Address:', f'<usdm:ref klass="Organization" id="{self._organization().id}" attribute="name"/><br/><usdm:ref klass="Address" id="{self._organization_address().id}" attribute="text"/>', 'Enter Sponsor Name, Enter Sponsor Legal Address')
      self._generate_m11_title_page_entry(doc, 'Regulatory Agency Identifier Number(s):', '', 'EU CT Number, IDE Number, FDA IND Number, JRCT Number, NCT Number, NMPA IND Number, WHO/UTN Number, Other Regulatory Agency Identifier Number')
      self._generate_m11_title_page_entry(doc, 'Spondor Approval Date:', '', 'Enter Approval Date or state location where information can be found')

      # Enter Nonproprietary Name(s)
      # Enter Proprietary Name(s)
      # Globally/Locally/Cohort
      # Primary Reason for Amendment
      # Region Identifier
      # Secondary Reason for Amendment

    result = doc.getvalue()
    #print(f"DOC: {result}")
    return result
  
  def _generate_m11_criteria(self, type):
    #print(f"M11 TP:")
    heading = { 
      'C25532': "Patients may be included in the study only if they meet <strong>all</strong> the following criteria:",
      'C25370': "Patients may be excluded in the study for <strong>any</strong> of the following reasons:",
    }
    doc = Doc()
    with doc.tag('p'):
      doc.asis(heading[type])  
    with doc.tag('table'):
      for criterion in self._criteria(type):
        self._generate_m11_critieria_entry(doc, criterion['identifier'], criterion['text'])
    return doc.getvalue()

  def _generate_m11_objective_endpoints(self):
    #print(f"M11 TP:")
    doc = Doc()
    with doc.tag('table'):
      for item in self._objective_endpoints():
        self._generate_m11_objective_endpoints_entry(doc, item['objective'], item['endpoints'])
    return doc.getvalue()

  def _generate_m11_critieria_entry(self, doc, number, entry):
    with doc.tag('tr'):
      with doc.tag('td', style="vertical-align: top; text-align: left"):
        with doc.tag('p'):
          doc.asis(number)  
      with doc.tag('td', style="vertical-align: top; text-align: left"):
        with doc.tag('p'):
          doc.asis(entry)

  def _generate_m11_objective_endpoints_entry(self, doc, objective, endpoints):
    with doc.tag('tr'):
      with doc.tag('td', style="vertical-align: top; text-align: left"):
        with doc.tag('p'):
          doc.asis(objective)  
      with doc.tag('td', style="vertical-align: top; text-align: left"):
        for endpoint in endpoints:
          with doc.tag('p'):
            doc.asis(endpoint)

  def _generate_m11_title_page_entry(self, doc, title, entry, m11_reference=''):
    with doc.tag('tr'):
      with doc.tag('th', style="vertical-align: top; text-align: left"):
        with doc.tag('p'):
          doc.asis(title)  
        with doc.tag('p', style="vertical-align: top; text-align: left; color: #2AAA8A; font-size: 12px"):
          with doc.tag('i'):
            m11_reference = "Not set" if not m11_reference else m11_reference
            doc.text(f"M11: {m11_reference}")  
        with doc.tag('p', style="vertical-align: top; text-align: left; color: #FA8072; font-size: 12px"):
          with doc.tag('i'):
            doc.text(f"USDM: {', '.join(self._list_references(entry))}")  
      with doc.tag('td', style="vertical-align: top; text-align: left"):
        with doc.tag('p'):
          doc.asis(entry)

  def _study_identifier(self):
    identifiers = self.study_version.studyIdentifiers
    for identifier in identifiers:
      if identifier.studyIdentifierScope.type.code == 'C70793':
        return identifier
    return None
  
  def _organization(self):
    identifier = self._study_identifier()
    return identifier.studyIdentifierScope
  
  def _organization_address(self):
    organization = self._organization()
    return organization.organizationLegalAddress
  
  def _amendment(self):
    amendments = self.study_version.amendments
    return amendments[-1]
    
  def _criteria(self, type):
    results = []
    items = [c for c in self.study_design.studyEligibilityCritieria if c.category.code == type ]
    items.sort(key=lambda d: d.identifier)
    for item in items:
      result = {'identifier': item.identifier, 'text': item.text}
      dictionary = cross_references.get_by_id('SyntaxTemplateDictionary', item.dictionaryId)
      if dictionary:
        result['text'] = self._substitute_tags(result['text'], dictionary)
      results.append(result)
    return results

  def _objective_endpoints(self):
    results = []
    for item in self.study_design.studyObjectives:
      result = {'objective': item.text, 'endpoints': []}
      dictionary = cross_references.get_by_id('SyntaxTemplateDictionary', item.dictionaryId)
      if dictionary:
        result['objective'] = self._substitute_tags(result['objective'], dictionary)
      for endpoint in item.objectiveEndpoints:
        dictionary = cross_references.get_by_id('SyntaxTemplateDictionary', endpoint.dictionaryId)
        ep_text = endpoint.text
        if dictionary:
          ep_text = self._substitute_tags(ep_text, dictionary)
        result['endpoints'].append(ep_text)
      results.append(result)
    return results

  def _substitute_tags(self, text, dictionary):
      tags = re.findall(r'\[([^]]*)\]', text)
      for tag in tags:
        if tag in dictionary.parameterMap:
          map = dictionary.parameterMap[tag]
          text = text.replace(f"[{tag}]", f'<usdm:ref klass="{map["klass"]}" id="{map["id"]}" attribute="{map["attribute"]}"/>')
      return text

  def _list_references(self, content_text):
    references = []
    soup = BeautifulSoup(content_text, 'html.parser')
    for ref in soup(['usdm:ref']):
      attributes = ref.attrs
      references.append(f"'class': {attributes['klass']}, 'attribute': {attributes['attribute']}")
    return references