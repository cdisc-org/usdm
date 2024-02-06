import re
import os
import base64
import traceback
import docraptor
import warnings
from yattag import Doc
from bs4 import BeautifulSoup   
from usdm_excel.cross_ref import cross_references
from usdm_excel.logger import logging
from usdm_excel.errors.errors import error_manager

class NarrativeContent():

  class LogicError(Exception):
    pass

  def __init__(self, doc_title, study, filepath):
    #warnings.filterwarnings("error")
    self.filepath = filepath
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
    doc_api.api_client.configuration.username = os.getenv('DOCRAPTOR_API_KEY')

    document_content = self.to_html()
    try:
      response = doc_api.create_doc({
        'test': True,  # test documents are free but watermarked
        #'test': False,  # Non-watermarked documents, but limited number allowed.
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
    except docraptor.rest.ApiException as e:
      logging.error(f"Failed to create PDF document {e.status} {e.reason} {e.body}\n{traceback.format_exc()}")
      error_manager.add(None, None, None, f"Something went wrong '{e.reason}' creating the PDF document")
    except Exception as e:
      logging.error(f"Exception '{e}' raised generating PDF content.\n{traceback.format_exc()}")
      error_manager.add(None, None, None, f"Exception '{e}' raised generating PDF content")

  def to_html(self):
    try:
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
      """
      chapters = []
      for id in root.childIds:
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
          with doc.tag('meta', **{'charset': "utf-8"}):
            pass
          with doc.tag('meta', **{"name": "viewport", "content": "width=device-width", "initial-scale": "1"}):
            pass
          with doc.tag('style'):
            doc.asis(style)     
          attributes = {
            'href': "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;800&display=swap",
            'rel': "stylesheet"
          }
          with doc.tag('link', **attributes):
            pass
          attributes = {
            'href': "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
            'rel': "stylesheet",
            'integrity': "sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN",
            'crossorigin': "anonymous"
          }
          with doc.tag('link', **attributes):
            pass
        with doc.tag('body'):
          doc.asis(front_sheet)    
          for id in root.childIds:
            content = next((x for x in self.protocol_document_version.contents if x.id == id), None)
            if content:
              self._content_to_html(content, doc)
      return doc.getvalue()
    except Exception as e:
      logging.error(f"Exception '{e}' raised generating HTML content.\n{traceback.format_exc()}")
      error_manager.add(None, None, None, f"Exception '{e}' raised generating HTML content")

  def _content_to_html(self, content, doc):
    level = len(content.sectionNumber.split('.'))
    klass = "page" if level == 1 else ""
    heading_id = f"section-{content.sectionNumber}"
    with doc.tag('div', klass=klass):
      if (level == 1 and int(content.sectionNumber) > 0) or (level > 1):
        with doc.tag(f'h{level}', id=heading_id):
          doc.asis(f"{content.sectionNumber}&nbsp{content.sectionTitle}")
      if self._standard_section(content.text):
        name = self._standard_section_name(content.text)
        content.text = self._generate_standard_section(name)
      doc.asis(self._translate_references(content.text))
      for id in content.childIds:
        content = next((x for x in self.protocol_document_version.contents if x.id == id), None)
        self._content_to_html(content, doc)

  def _translate_references(self, content_text):
    soup = self._get_soup(content_text)
    for ref in soup(['usdm:ref']):
      try:
        attributes = ref.attrs
        if 'namexref' in attributes:
          instance, attribute = cross_references.get_by_path(attributes['klass'], attributes['namexref'], attributes['attribute'])
          value = str(getattr(instance, attribute))
          translated_text = self._translate_references(value)
          ref.replace_with(translated_text)
        elif 'image' in attributes:
          type = {attributes['type']}
          data = self._encode_image(attributes['image'])
          img_tag = soup.new_tag("img")
          img_tag.attrs['src'] = f"data:image/{type};base64,{data.decode('ascii')}"
          ref.replace_with(img_tag)
        elif 'element' in attributes:
          method = f"_{attributes['element']}"
          if self._valid_method(method):
            value = getattr(self, method)()
            if value:
              translated_text = self._translate_references(value)
              ref.replace_with(translated_text)
            else:
              error_manager.add(None, None, None, f"Failed to translate element method name '{method}' in '{attributes}' while generating the HTML document, no value")
              ref.replace_with('Missing content: no value')
          else:
            error_manager.add(None, None, None, f"Failed to translate element method name '{method}' in '{attributes}' while generating the HTML document, invalid method")
            ref.replace_with('Missing content: invalid method name')
        elif 'id' in attributes:
          instance = cross_references.get_by_id(attributes['klass'], attributes['id'])
          value = str(getattr(instance, attributes['attribute']))
          translated_text = self._translate_references(value)
          ref.replace_with(translated_text)
        else:
          error_manager.add(None, None, None, f"Failed to translate reference '{attributes}' while generating the HTML document, invalid attribute name")
          ref.replace_with('Missing content: invalid attribute name')
      except Exception as e:
        logging.error(f"Failed to translate reference '{attributes}'\n{traceback.format_exc()}")
        error_manager.add(None, None, None, f"Exception '{e} while attempting to translate reference '{attributes}' while generating the HTML document")
        ref.replace_with('Missing content: exception')
    return str(soup)

  def _encode_image(self, filename):
    with open(os.path.join(self.filepath, filename), "rb") as image_file:
      data = base64.b64encode(image_file.read())
    return data
  
  def _valid_method(self, name):
    return name in [
      '_study_phase',
      '_study_short_title',
      '_study_full_title',
      '_study_acronym',
      '_study_rationale',
      '_study_version',
      '_study_identifier',
      '_study_regulatory_identifiers',
      '_study_date',
      '_approval_date',
      '_organization_name_and_address',
      '_amendment',
      '_amendment_scopes',
      '_no_value_for_test'
    ]
  
  def _standard_section(self, text):
    soup = self._get_soup(text)
    for section in soup(['usdm:section']):
      return True
    return False
  
  def _standard_section_name(self, text):  
    soup = self._get_soup(text)
    for section in soup(['usdm:section']):
      attributes = section.attrs
      if 'name' in attributes:
        return attributes['name'].upper()
      else:
        return None
    return None

  def _get_soup(self, text):
    try:
      #print(f"SOUP: {text}")
      with warnings.catch_warnings(record=True) as warning_list:
        result =  BeautifulSoup(text, 'html.parser')
      if warning_list:
        error_manager.add(None, None, None, f"Warning raised within Soup package, processing '{text}'", level=error_manager.WARNING)
      return result
    except:
      logging.error(f"Exception raised parsing '{text}'\n{traceback.format_exc()}")
      error_manager.add(None, None, None, f"Exception raised raised parsing '{text}'. Ignoring value")
      return ""
    
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
      self._generate_m11_title_page_entry(doc, 'Full Title:', f'{self._study_full_title()}', 'Enter Full Title')
      self._generate_m11_title_page_entry(doc, 'Trial Acronym:', f'{self._study_acronym()}', 'Enter trial Acronym')
      self._generate_m11_title_page_entry(doc, 'Protocol Identifier:', f'{self._study_identifier()}', 'Enter Protocol Identifier')
      self._generate_m11_title_page_entry(doc, 'Original Protocol:', '', 'Original protocol')
      self._generate_m11_title_page_entry(doc, 'Version Number:', f'{self._study_version()}', 'Enter Version Number')
      self._generate_m11_title_page_entry(doc, 'Version Date:', f'{self._study_date()}', 'Enter Version Date')
      self._generate_m11_title_page_entry(doc, 'Amendment Identifier:', f'{self._amendment()}', 'Amendment Identifier')
      self._generate_m11_title_page_entry(doc, 'Amendment Scope:', f'{self._amendment_scopes()}', 'Amendment Scope')
      self._generate_m11_title_page_entry(doc, 'Compound Codes(s):', '', 'Enter Compound Code(s)')
      self._generate_m11_title_page_entry(doc, 'Compound Name(s):', '', 'Enter Nonproprietary Name(s), Enter Proprietary Name(s)')
      self._generate_m11_title_page_entry(doc, 'Trial Phase:', f'{self._study_phase()}', 'Trial Phase')
      self._generate_m11_title_page_entry(doc, 'Short Title:', f'{self._study_short_title()}', 'Enter Trial Short Title')
      self._generate_m11_title_page_entry(doc, 'Sponsor Name and Address:', f'{self._organization_name_and_address()}', 'Enter Sponsor Name, Enter Sponsor Legal Address')
      self._generate_m11_title_page_entry(doc, 'Regulatory Agency Identifier Number(s):', f'{self._study_regulatory_identifiers()}', 'EU CT Number, IDE Number, FDA IND Number, JRCT Number, NCT Number, NMPA IND Number, WHO/UTN Number, Other Regulatory Agency Identifier Number')
      self._generate_m11_title_page_entry(doc, 'Spondor Approval Date:', f'{self._approval_date()}', 'Enter Approval Date or state location where information can be found')

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
      with doc.tag('td', style="vertical-align: top; text-align: left"):
        with doc.tag('p'):
          doc.asis(entry)
    with doc.tag('tr', bgcolor="#F2F4F4"):
      with doc.tag('td', colspan="2", style="vertical-align: top; text-align: left; font-size: 12px"):
        #with doc.tag('span', style="vertical-align: top; text-align: left; font-size: 12px"):
        with doc.tag('i'):
          with doc.tag('span', style="color: #2AAA8A"):
            m11_reference = "Not set" if not m11_reference else m11_reference
            doc.text(f"M11: {m11_reference}")  
          with doc.tag('br'):
            pass
          with doc.tag('span', style="color: #FA8072"):
            doc.text(f"USDM: {', '.join(self._list_references(entry))}")  

  def _sponsor_identifier(self):
    identifiers = self.study_version.studyIdentifiers
    for identifier in identifiers:
      if identifier.studyIdentifierScope.organizationType.code == 'C70793':
        return identifier
    return None
  
  def _study_phase(self):
    phase = self.study_version.studyPhase.standardCode
    results = [{'instance': phase, 'klass': 'Code', 'attribute': 'decode', 'path': 'StudyVersion/@studyPhase/@standardCode/@decode'}]
    return self._set_of_references(results)

  def _study_short_title(self):
    title = self._get_title('Brief Study Title')
    results = [{'instance': title, 'klass': 'StudyTitle', 'attribute': 'text', 'path': 'StudyVersion/@titles/StudyTitle/@text'}]
    return self._set_of_references(results)

  def _study_full_title(self):
    title = self._get_title('Official Study Title')
    results = [{'instance': title, 'klass': 'StudyTitle', 'attribute': 'text', 'path': 'StudyVersion/@titles/StudyTitle/@text'}]
    return self._set_of_references(results)

  def _study_acronym(self):
    title = self._get_title('Study Acronym')
    results = [{'instance': title, 'klass': 'StudyTitle', 'attribute': 'text', 'path': 'StudyVersion/@titles/StudyTitle/@text'}]
    return self._set_of_references(results)

  def _study_rationale(self):
    results = [{'instance': self.study_version, 'klass': 'StudyVersion', 'attribute': 'rationale', 'path': 'StudyVersion/@rationale'}]
    return self._set_of_references(results)

  def _study_version(self):
    results = [{'instance': self.study_version, 'klass': 'StudyVersion', 'attribute': 'versionIdentifier', 'path': 'StudyVersion/@versionIdentifier'}]
    return self._set_of_references(results)

  def _study_identifier(self):
    identifier = self._sponsor_identifier()
    results = [{'instance': identifier, 'klass': 'StudyIdentifier', 'attribute': 'studyIdentifier', 'path': 'StudyIdentifier[Organization/@type/@code=C70793]/@studyIdentifier'}]
    return self._set_of_references(results)

  def _study_regulatory_identifiers(self):
    results = []
    identifiers = self.study_version.studyIdentifiers
    for identifier in identifiers:
      if identifier.studyIdentifierScope.organizationType.code == 'C188863' or identifier.studyIdentifierScope.organizationType.code == 'C93453':
        item = {'instance': identifier, 'klass': 'StudyIdentifier', 'attribute': 'studyIdentifier', 'path': 'StudyIdentifier[Organization/@type/@code=C188863|C93453]/@studyIdentifier'}
        results.append(item)
    return self._set_of_references(results)

  def _study_date(self):
    dates = self.protocol_document_version.dateValues
    for date in dates:
      if date.type.code == 'C99903x1':
        results = [{'instance': date, 'klass': 'GovernanceDate', 'attribute': 'dateValue', 'path': 'StudyProtocolDocumentVersion/GovernanceDate[@type/@code=C99903x1]/@dateValue'}]
        return self._set_of_references(results)
    return []
  
  def _approval_date(self):
    dates = self.study_version.dateValues
    for date in dates:
      if date.type.code == 'C132352':
        results = [{'instance': date, 'klass': 'GovernanceDate', 'attribute': 'dateValue', 'path': 'StudyVersion/GovernanceDate[@type/@code=C132352]/@dateValue'}]
        return self._set_of_references(results)
    return []

  def _organization_name_and_address(self):
    identifier = self._sponsor_identifier()
    results = [
      {'instance': identifier.studyIdentifierScope, 'klass': 'Organization', 'attribute': 'name', 'path': 'StudyIdentifier[Organization/@type/@code=C70793]/Organization/@name'},
      {'instance': identifier.studyIdentifierScope.legalAddress, 'klass': 'Address', 'attribute': 'text', 'path': 'StudyIdentifier[Organization/@type/@code=C70793]/Organization/Address/@text'},
    ]
    return self._set_of_references(results)

  def _amendment(self):
    amendments = self.study_version.amendments
    results = [{'instance': amendments[-1], 'klass': 'StudyAmendment', 'attribute': 'number', 'path': 'StudyVersion/StudyAmendment/@number'}]
    return self._set_of_references(results)

  def _amendment_scopes(self):
    results = []
    amendment = self.study_version.amendments[-1]
    for item in amendment.enrollments:
      if item.type.code == "C68846":
        results = [{'instance': item.type, 'klass': 'Code', 'attribute': 'decode', 'path': 'StudyVersion/StudyAmendment/SubjectEnrollment[@type/@code=C68846]/Code/@decode'}]
        return self._set_of_references(results)
      else:
        entry = {'instance': item.code.standardCode, 'klass': 'Code', 'attribute': 'decode', 'path': 'StudyVersion/StudyAmendment/SubjectEnrollment/@code/@standardCode/@decode'}
        results.append(entry)
    return self._set_of_references(results)

  def _no_value_for_test(self):
    return []

  def _criteria(self, type):
    results = []
    items = [c for c in self.study_design.population.criteria if c.category.code == type ]
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
    for item in self.study_design.objectives:
      result = {'objective': item.text, 'endpoints': []}
      dictionary = cross_references.get_by_id('SyntaxTemplateDictionary', item.dictionaryId)
      if dictionary:
        result['objective'] = self._substitute_tags(result['objective'], dictionary)
      for endpoint in item.endpoints:
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
      if 'path' in attributes:
        path = f"{attributes['path']}"
      else:
        path = f"{attributes['klass']}/@{attributes['attribute']}"
      if path not in references:
        references.append(path)
    return references if references else ['No mapping path']
  
  def _set_of_references(self, items):
    if items:
      return ", ".join([f'<usdm:ref klass="{item["klass"]}" id="{item["instance"].id}" attribute="{item["attribute"]}" path="{item["path"]}"/>' for item in items])
    else:
      return ""

  def _get_title(self, title_type):
    for title in self.study_version.titles:
      if title.type.decode == title_type:
        return title
    return None
