import os
import base64
import traceback
import logging
from document.template_m11 import TemplateM11
from document.template_plain import TemplatePlain
from document.elements import Elements
from usdm_db.cross_reference import CrossReference
from document.utility import get_soup, log_exception
from usdm_model.study import Study 
from usdm_db.errors.errors import Errors

class Macros():

  def __init__(self, study: Study, errors: Errors, cross_ref: CrossReference):
    self._logger = logging.getLogger(__name__)
    self._errors = errors
    self._cross_ref = cross_ref
    self.study = study
    self.study_version = study.versions[0]
    self.study_design = self.study_version.studyDesigns[0]
    self.protocol_document_version = self.study.documentedBy.versions[0]
    self.elements = Elements(self.study, self._errors)
    self.m11 = TemplateM11(self.study)
    self.plain = TemplatePlain(self.study)
    self.template_map = {'m11': self.m11, 'plain': self.plain}
  
  def resolve(self, content_text: str) -> str:
    soup = get_soup(content_text, self.parent)
    for ref in soup(['usdm:macro']):
      try:
        attributes = ref.attrs
        method = f"_{attributes['id'].lower()}"
        if self._valid_method(method):
          result = getattr(self, method)(attributes, soup, ref)
        else:
          self._errors.add(f"Failed to resolve document macro '{attributes}', invalid method name {method}")
          ref.replace_with('Missing content: invalid method name')
      except Exception as e:
        log_exception(self._logger, f"Failed to resolve document macro '{attributes}'", e)
        self._errors.add(f"Exception '{e} while attempting to translate document macro '{attributes}'")
        ref.replace_with('Missing content: exception')
    return str(soup)

  def _xref(self, attributes, soup, ref) -> None:
    instance, attribute = self._cross_ref.get_by_path(attributes['klass'], attributes['name'], attributes['attribute'])
    ref_tag = soup.new_tag("usdm:ref")
    ref_tag.attrs = {'klass': instance.__class__.__name__, 'id': instance.id, 'attribute': attribute}
    ref.replace_with(ref_tag)

  def _image(self, attributes, soup, ref) -> None:
    type = {attributes['type']}
    data = self._encode_image(attributes['file'])
    if data:
      img_tag = soup.new_tag("img")
      img_tag.attrs['src'] = f"data:image/{type};base64,{data.decode('ascii')}"
      ref.replace_with(img_tag)
    else:
      self._note({'text': f"Failed to insert image '{attributes['file']}', ignoring!"}, soup, ref)

  def _element(self, attributes, soup, ref) -> None:
    method = attributes['name'].lower()
    if self.elements.valid_method(method):
      text = getattr(self.elements, method)()
      ref.replace_with(get_soup(text, self.parent))
    else:
      self._errors.add(f"Failed to translate element method name '{method}' in '{attributes}', invalid method")
      ref.replace_with('Missing content: invalid method name')

  def _section(self, attributes, soup, ref) -> None:
    method = attributes['name'].lower()
    template = attributes['template'] if 'template' in attributes else 'plain' 
    instance = self._resolve_template(template)
    if instance.valid_method(method):
      text = getattr(instance, method)()
      ref.replace_with(get_soup(text, self.parent))
    else:
      self._errors.add(f"Failed to translate section method name '{method}' in '{attributes}', invalid method")
      ref.replace_with('Missing content: invalid method name')       

  def _note(self, attributes, soup, ref) -> None:
    text = f"""
      <div class="col-md-8 offset-md-2 text-center">
        <p class="usdm-warning">Note:</p>
        <p class="usdm-warning">{attributes['text']}</p>
      </div>
    """
    ref.replace_with(get_soup(text, self.parent))

  def _valid_method(self, name):
    return name in ['_xref', '_image', '_element', '_section', '_note']
  
  def _resolve_template(self, template) -> object:
    try:
      return self.template_map[template.lower()]
    except:
      self._errors.add(f"Failed to resolve template '{template}', using plain template")
      return self.plain

  def _encode_image(self, filename) -> bytes:
    try:
      with open(os.path.join(self.parent.dir_path, filename), "rb") as image_file:
        data = base64.b64encode(image_file.read())
      return data
    except:
      self._errors.add(f"Failed to open image file '{filename}', ignored")
      return None
      