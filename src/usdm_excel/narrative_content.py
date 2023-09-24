import docraptor
from yattag import Doc
from bs4 import BeautifulSoup   
from usdm_excel.cross_ref import cross_references

class NarrativeContent():

  def __init__(self, doc_title, study_design):
    #print("NC INIT:")
    self.doc_title = doc_title
    self.study_design = study_design

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
    root = self.study_design.contents[0]
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
      content = next((x for x in self.study_design.contents if x.id == id), None)
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
          content = next((x for x in self.study_design.contents if x.id == id), None)
          #print(f"NC TH3: {id}={content.sectionNumber}")
          if content:
            self._content_to_html(content, doc)
    #print(doc.getvalue())
    return doc.getvalue()
  
  def _content_to_html(self, content, doc):
    level = len(content.sectionNumber.split('.'))
    klass = "page" if level == 1 else ""
    id = f"section-{content.sectionNumber}"
    with doc.tag('div', klass=klass):
      with doc.tag(f'h{level}', id=id):
        doc.asis(f"{content.sectionNumber}&nbsp{content.sectionTitle}")
      doc.asis(self._translate_references(content.text))
      for id in content.contentChildIds:
        content = next((x for x in self.study_design.contents if x.id == id), None)
        self._content_to_html(content, doc)

  def _translate_references(self, content_text):
    soup = BeautifulSoup(content_text, 'html.parser')
    for ref in soup(['usdm:ref']):
      attributes = ref.attrs
      try:
        #print(f"TR: Attributes={attributes}")
        if 'namexref' in attributes:
          instance = cross_references.get(attributes['klass'], attributes['namexref'])
          #print(f"TR: Name xref instance {instance}")
        else:
          instance = cross_references.get_by_id(attributes['klass'], attributes['id'])
          #print(f"TR: Id instance {instance}")
        try:
          translated_text = self._translate_references(getattr(instance, attributes['attribute']))
          #print(f"TR: text {translated_text}")
          ref.replace_with(translated_text)
        except:
          ref.replace_with("***** Failed to translate reference, attribute not found *****")
      except:
        ref.replace_with("***** Failed to translate reference, instance not foound *****")
    return str(soup)