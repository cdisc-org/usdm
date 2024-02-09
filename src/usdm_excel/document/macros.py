import os
import base64
import traceback
import warnings
from bs4 import BeautifulSoup   
from .m11_template import M11Template
from .plain_template import PlainTemplate
from .elements import Elements
from usdm_excel.cross_ref import cross_references
from usdm_excel.base_sheet import BaseSheet

class Macros():

  def __init__(self, parent: BaseSheet, study):
    self.parent = parent
    self.study = study
    self.study_version = study.versions[0]
    self.study_design = self.study_version.studyDesigns[0]
    self.protocol_document_version = self.study.documentedBy.versions[0]
    self.elements = Elements(self.study)
    self.m11 = M11Template(self.study)
    self.plain = PlainTemplate(self.study)
    self.template_map = {'m11': self.m11, 'plain': self.plain}
  
  def resolve(self, content_text: str) -> str:
    soup = self._get_soup(content_text)
    for ref in soup(['usdm:macro']):
      try:
        attributes = ref.attrs
        method = f"_{attributes['id'].lower()}"
        if self._valid_method(method):
          result = getattr(self, method)(attributes, soup, ref)
        else:
          self.parent._general_error(f"Failed to resolve document macro '{attributes}', invalid method name {method}")
          ref.replace_with('Missing content: invalid method name')
      except Exception as e:
        self.parent._traceback(f"Failed to resolve document macro '{attributes}'\n{traceback.format_exc()}")
        self.parent._general_error(f"Exception '{e} while attempting to translate document macro '{attributes}'")
        ref.replace_with('Missing content: exception')
    return str(soup)

  def _xref(self, attributes, soup, ref) -> None:
    instance, attribute = cross_references.get_by_path(attributes['klass'], attributes['name'], attributes['attribute'])
    ref_tag = soup.new_tag("usdm:ref")
    ref_tag.attrs = {'klass': instance.__class__.__name__, 'id': instance.id, 'attribute': attribute}
    ref.replace_with(ref_tag)

  def _image(self, attributes, soup, ref) -> None:
    type = {attributes['type']}
    data = self._encode_image(attributes['file'])
    img_tag = soup.new_tag("img")
    img_tag.attrs['src'] = f"data:image/{type};base64,{data.decode('ascii')}"
    ref.replace_with(img_tag)

  def _element(self, attributes, soup, ref) -> None:
    method = attributes['name'].lower()
    if self.elements.valid_method(method):
      text = getattr(self.elements, method)()
      ref.replace_with(self._get_soup(text))
    else:
      self.parent._general_error(f"Failed to translate element method name '{method}' in '{attributes}', invalid method")
      ref.replace_with('Missing content: invalid method name')

  def _section(self, attributes, soup, ref) -> None:
    method = attributes['name'].lower()
    template = attributes['template'] if 'template' in attributes else 'plain' 
    instance = self._resolve_template(template)
    if instance.valid_method(method):
      text = getattr(instance, method)()
      ref.replace_with(self._get_soup(text))
    else:
      self.parent._general_error(f"Failed to translate section method name '{method}' in '{attributes}', invalid method")
      ref.replace_with('Missing content: invalid method name')       

  def _valid_method(self, name):
    return name in ['_xref', '_image', '_element', '_section']
  
  def _resolve_template(self, template) -> object:
    try:
      return self.template_map[template.lower()]
    except:
      self.parent._general_error(f"Failed to map template '{template}', using plain template")
      return self.plain

  def _encode_image(self, filename) -> bytes:
    with open(os.path.join(self.parent.dir_path, filename), "rb") as image_file:
      data = base64.b64encode(image_file.read())
    return data
  
  def _get_soup(self, text) -> str:
    try:
      #print(f"SOUP: {text}")
      with warnings.catch_warnings(record=True) as warning_list:
        result =  BeautifulSoup(text, 'html.parser')
      if warning_list:
        self.parent._general_warning(None, None, None, f"Warning raised within Soup package, processing '{text}'")
      return result
    except Exception as e:
      self.parent._traceback(f"Exception '{e}' raised parsing '{text}'\n{traceback.format_exc()}")
      self.parent._general_error(f"Exception raised parsing '{text}'. Ignoring value")
      return ""
    