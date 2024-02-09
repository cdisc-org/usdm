import os
import sys
import base64
import traceback
import docraptor
import warnings
from yattag import Doc
from bs4 import BeautifulSoup   
from usdm_excel.cross_ref import cross_references
from usdm_excel.logger import logging
from usdm_excel.errors.errors import error_manager
from usdm_excel.document.m11_template import M11Template
from usdm_excel.document.plain_template import PlainTemplate
from usdm_excel.document.elements import Elements

class NarrativeContent():

  class LogicError(Exception):
    pass

  def __init__(self, doc_title, study, filepath):
    self.filepath = filepath
    self.study = study
    self.study_version = study.versions[0]
    self.study_design = self.study_version.studyDesigns[0]
    self.protocol_document_version = self.study.documentedBy.versions[0]
    self.doc_title = doc_title
    self.elements = Elements(self.study)
    self.m11 = M11Template(self.study)
    self.plain = PlainTemplate(self.study)
    self.template_map = {'m11': self.m11, 'plain': self.plain}
    self.chapters = []
    if self.protocol_document_version.id != self.study.versions[0].documentVersionId:
      logging.error(f"Failed to initialise NarrativeContent for document creation, ids did not match")
      raise self.LogicError(f"Failed to initialise NarrativeContent for document creation, ids did not match")

  def to_pdf(self, test=True):
    print(f"PDF: Test set {test}")
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
      logging.error(f"Failed to create PDF document {e.status} {e.reason} {e.body}\n{traceback.format_exc()}")
      error_manager.add(None, None, None, f"Something went wrong '{e.reason}' creating the PDF document")
    except Exception as e:
      logging.error(f"Exception '{e}' raised generating PDF content.\n{traceback.format_exc()}")
      error_manager.add(None, None, None, f"Exception '{e}' raised generating PDF content")

  def to_html(self):
    try:
      self.chapters = []
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
      for id in root.childIds:
        content = next((x for x in self.protocol_document_version.contents if x.id == id), None)
        level = len(content.sectionNumber.split('.'))
        if level == 1:
          self.chapters.append(f'<a href="#section-{content.sectionNumber}"></a>')
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
          # doc.asis(front_sheet)    
          for id in root.childIds:
            content = next((x for x in self.protocol_document_version.contents if x.id == id), None)
            if content:
              self._content_to_html(content, doc)
      return doc.getvalue()
    except Exception as e:
      logging.error(f"Exception '{e}' raised generating HTML content.\n{traceback.format_exc()}")
      error_manager.add(None, None, None, f"Exception '{e}' raised generating HTML content")

  def _content_to_html(self, content, doc):
    #level = len(content.sectionNumber.split('.'))
    level = self._get_level(content.sectionNumber)
    klass = "page" if level == 1 else ""
    heading_id = f"section-{content.sectionNumber}"
    with doc.tag('div', klass=klass):
      if (level == 1 and self._is_doc_section(content.sectionNumber)) or (level > 1):
        with doc.tag(f'h{level}', id=heading_id):
          doc.asis(f"{content.sectionNumber} {content.sectionTitle}")
      doc.asis(str(self._translate_references(content.text)))
      for id in content.childIds:
        content = next((x for x in self.protocol_document_version.contents if x.id == id), None)
        self._content_to_html(content, doc)

  def _get_level(self, section_number):
    #print(f"LEVEL1: {section_number}")
    if section_number.lower().startswith("appendix"):
      result = 1
    else:
      text = section_number[:-1] if section_number.endswith('.') else section_number
      result = len(text.split('.'))
    #print(f"LEVEL2: {result}")
    return result
      
  def _is_doc_section(self, section_number):
    try:
      sn = int(section_number)
      return True if sn > 0 else False
    except:
      return True
    
  def _translate_references(self, content_text):
    soup = self._get_soup(content_text)
    for ref in soup(['usdm:ref']):
      self._usdm_reference(soup, ref)
    return self._get_soup(str(soup))

  def _usdm_reference(self, soup, ref):
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
        method = attributes['element'].lower()
        if self.elements.valid_method(method):
          value = getattr(self.elements, method)()
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
      elif 'section' in attributes:
        method = attributes['section'].lower()
        template = attributes['template'] if 'template' in attributes else 'plain' 
        instance = self._resolve_template(template)
        if instance.valid_method(method):
          text = getattr(instance, method)()
          #print(f"\n\n\nTEXT1: {text}")
          translated_text = self._translate_references(text)
          #print(f"TEXT2: {translated_text}")
          ref.replace_with(translated_text)
        else:
          error_manager.add(None, None, None, f"Failed to translate section method name '{method}' in '{attributes}' while generating the HTML document, invalid method")
          ref.replace_with('Missing content: invalid method name')       
      elif 'table_of_contents' in attributes:
        toc = f"""
          <div id="toc-page" class="page">
            <div id="table-of-contents">
              {''.join(self.chapters)}
            </div>
            <div id="header-and-footer">
              <span id="page-number"></span>
            </div>
          </div>
        """
        ref.replace_with(self._get_soup(toc))
      elif 'title_page' in attributes:
        tp = f"""
          <div id="title-page" class="page">
            <div class="container">
              <div class="row">
                <div class="col-md-8 offset-md-2 text-center">
                  <h1>{self.doc_title}</h1>
                </div>
              </div>
              <div class="row mt-5">
                <div class="col-md-8 offset-md-2 text-center">
                  <p><b>This document is generated from content held within the Unified Studies Definitions Model. It is for test purposes only.</b></p>
                </div>
              </div>
            </div>
            <div id="header-and-footer">
              <span id="page-number"></span>
            </div>
          </div>
        """
        ref.replace_with(self._get_soup(tp))
      else:
        error_manager.add(None, None, None, f"Failed to translate reference '{attributes}' while generating the HTML document, invalid attribute name")
        ref.replace_with('Missing content: invalid attribute name')
    except Exception as e:
      logging.error(f"Failed to translate reference '{attributes}'\n{traceback.format_exc()}")
      error_manager.add(None, None, None, f"Exception '{e} while attempting to translate reference '{attributes}' while generating the HTML document")
      ref.replace_with('Missing content: exception')
  
  def _resolve_template(self, template):
    try:
      return self.template_map[template.lower()]
    except:
      error_manager.add(None, None, None, f"Failed to map template '{template}', using plain template")
      return self.plain

  def _encode_image(self, filename):
    with open(os.path.join(self.filepath, filename), "rb") as image_file:
      data = base64.b64encode(image_file.read())
    return data
  
  def _get_soup(self, text):
    try:
      #print(f"SOUP: {text}")
      with warnings.catch_warnings(record=True) as warning_list:
        result =  BeautifulSoup(text, 'html.parser')
      if warning_list:
        error_manager.add(None, None, None, f"Warning raised within Soup package, processing '{text}'", level=error_manager.WARNING)
      return result
    except Exception as e:
      logging.error(f"Exception '{e}' raised parsing '{text}'\n{traceback.format_exc()}")
      error_manager.add(None, None, None, f"Exception raised parsing '{text}'. Ignoring value")
      return ""
    