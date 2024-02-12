import os
import base64
import traceback
import docraptor
import warnings
from yattag import Doc
from bs4 import BeautifulSoup   
from usdm_excel.cross_ref import cross_references
from usdm_excel.base_sheet import BaseSheet
from usdm_excel.study_sheet.study_sheet import Study

class Document():

  class LogicError(Exception):
    pass

  def __init__(self, parent: BaseSheet, doc_title: str, study: Study, filepath: str):
    self.parent = parent
    self.filepath = filepath
    self.study = study
    self.study_version = study.versions[0]
    self.study_design = self.study_version.studyDesigns[0]
    self.protocol_document_version = self.study.documentedBy.versions[0]
    self.doc_title = doc_title
    self.chapters = []
    if self.protocol_document_version.id != self.study.versions[0].documentVersionId:
      self.parent._general_error(f"Failed to initialise NarrativeContent for document creation, ids did not match")
      raise self.LogicError(f"Failed to initialise NarrativeContent for document creation, ids did not match")

  def to_pdf(self, test=True):
    #print(f"PDF: Test set {test}")
    doc_api = docraptor.DocApi()
    doc_api.api_client.configuration.username = os.getenv('DOCRAPTOR_API_KEY')
    document_content = self.to_html()
    try:
      response = doc_api.create_doc({
        'test': test,  # test documents are free but watermarked
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
      self.parent._traceback(f"Failed to create PDF document {e.status} {e.reason} {e.body}\n{traceback.format_exc()}")
      self.parent._general_error(f"Something went wrong '{e.reason}' creating the PDF document")
    except Exception as e:
      self.parent._general_error(f"Exception '{e}' raised generating PDF content.\n{traceback.format_exc()}")
      self.parent._general_error(f"Exception '{e}' raised generating PDF content")

  def to_html(self):
    try:
      self.chapters = []
      root = self.protocol_document_version.contents[0]
      doc = Doc()
      doc.asis('<!DOCTYPE html>')
      for id in root.childIds:
        content = next((x for x in self.protocol_document_version.contents if x.id == id), None)
        if self._is_level_1_doc_section(content.sectionNumber):
          self.chapters.append(f'<a href="#section-{content.sectionNumber}"></a>')
      with doc.tag('html'):
        with doc.tag('head'):
          with doc.tag('meta', **{'charset': "utf-8"}):
            pass
          with doc.tag('meta', **{"name": "viewport", "content": "width=device-width", "initial-scale": "1"}):
            pass
          with doc.tag('style'):
            doc.asis(self._style())     
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
          doc.asis(self._title_page())    
          for id in root.childIds:
            content = next((x for x in self.protocol_document_version.contents if x.id == id), None)
            if content:
              self._content_to_html(content, doc)
      return doc.getvalue()
    except Exception as e:
      self.parent._traceback(f"Exception '{e}' raised generating HTML content.\n{traceback.format_exc()}")
      self.parent._general_error(f"Exception '{e}' raised generating HTML content")

  def _content_to_html(self, content, doc):
    #level = len(content.sectionNumber.split('.'))
    level = self._get_level(content.sectionNumber)
    klass = "page" if level == 1 else ""
    heading_id = f"section-{content.sectionNumber}"
    if (level == 1 and self._is_first_section(content.sectionNumber)):
      with doc.tag('div', klass=klass):
        doc.asis(self._table_of_contents())    
    with doc.tag('div', klass=klass):
      if (self._is_level_1_doc_section(content.sectionNumber)) or (level > 1):
        with doc.tag(f'h{level}', id=heading_id):
          doc.asis(f"{content.sectionNumber} {content.sectionTitle}")
      doc.asis(str(self._translate_references(content.text)))
      for id in content.childIds:
        content = next((x for x in self.protocol_document_version.contents if x.id == id), None)
        self._content_to_html(content, doc)

  def _get_level(self, section_number):
    if section_number.lower().startswith("appendix"):
      result = 1
    else:
      text = section_number[:-1] if section_number.endswith('.') else section_number
      result = len(text.split('.'))
    return result
      
  def _is_doc_section(self, section_number):
    try:
      sn = int(section_number)
      return True if sn > 0 else False
    except:
      return True

  def _is_level_1_doc_section(self, section_number):
    level = self._get_level(section_number)
    return level == 1 and self._is_doc_section(section_number)
  
  def _is_first_section(self, section_number):
    try:
      sn = int(section_number)
      return True if sn == 1 else False
    except:
      return False

  def _translate_references(self, content_text):
    soup = self._get_soup(content_text)
    for ref in soup(['usdm:ref']):
      try:
        attributes = ref.attrs
        instance = cross_references.get_by_id(attributes['klass'], attributes['id'])
        value = self._resolve_instance(instance, attributes['attribute'])
        translated_text = self._translate_references(value)
        ref.replace_with(translated_text)
      except Exception as e:
        self.parent._traceback(f"Failed to translate reference '{attributes}'\n{traceback.format_exc()}")
        self.parent._general_error(f"Exception '{e} while attempting to translate reference '{attributes}' while generating the HTML document")
        ref.replace_with('Missing content: exception')
    return self._get_soup(str(soup))

  def _resolve_instance(self, instance, attribute):
    dictionary = self._get_dictionary(instance)
    value = str(getattr(instance, attribute))
    soup = self._get_soup(value)
    for ref in soup(['usdm:tag']):
      try:
        attributes = ref.attrs
        if dictionary:
          value = dictionary.parameterMap[attributes['name']]
          ref.replace_with(self._get_soup(value))
        else:
          self.parent._general_error(f"Missing dictionary while attempting to resolve reference '{attributes}' while generating the HTML document")
          ref.replace_with('Missing content: missing dictionary')
      except Exception as e:
        self.parent._traceback(f"Failed to resolve reference '{attributes}'\n{traceback.format_exc()}")
        self.parent._general_error(f"Exception '{e} while attempting to resolve reference '{attributes}' while generating the HTML document")
        ref.replace_with('Missing content: exception')
    return str(soup)

  def _get_dictionary(self, instance):
    try:
      return cross_references.get_by_id('SyntaxTemplateDictionary', instance.dictionaryId)
    except:
      return None  
    
  def _table_of_contents(self):
    return f"""
      <div id="toc-page" class="page">
        <div id="table-of-contents">
          {''.join(self.chapters)}
        </div>
        <div align="center">
          <br/>
          <p class="usdm-warning">Note:</p>
          <p class="usdm-warning">The table of contents is auto generated upon PDF production and only includes first level sections.</p>
        </div>
        <div id="header-and-footer">
          <span id="page-number"></span>
        </div>
      </div>
    """

  def _title_page(self):
    return f"""
      <div id="title-page" class="page">
        <div class="container">
          <div class="row">
            <div class="col-md-8 offset-md-2 text-center">
              <h1>{self.doc_title}</h1>
            </div>
          </div>
          <div class="row mt-5">
            <div class="col-md-8 offset-md-2 text-center">
              <p class="usdm-warning">Note:</p>
              <p class="usdm-warning">This document is generated from content held within the Unified Studies Definitions Model. It is for test purposes only.</p>
            </div>
          </div>
        </div>
        <div id="header-and-footer">
          <span id="page-number"></span>
        </div>
      </div>
    """

  def _style(self):
    return """
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

      .usdm-warning {
        font-style: italic;
        color: red;
      }
    """
    
  def _get_soup(self, text):
    try:
      with warnings.catch_warnings(record=True) as warning_list:
        result =  BeautifulSoup(text, 'html.parser')
      if warning_list:
        self.parent._general_warning(f"Warning raised within Soup package, processing '{text}'")
      return result
    except Exception as e:
      self.parent._traceback(f"Exception '{e}' raised parsing '{text}'\n{traceback.format_exc()}")
      self.parent._general_error(f"Exception raised parsing '{text}'. Ignoring value")
      return ""
    