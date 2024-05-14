import os
import base64
from usdm_excel.document.template_m11 import TemplateM11
from usdm_excel.document.template_plain import TemplatePlain
from usdm_excel.document.elements import Elements
from usdm_excel.base_sheet import BaseSheet
from usdm_model.study import Study
from usdm_model.activity import Activity
from usdm_model.biomedical_concept import BiomedicalConcept
from usdm_model.biomedical_concept_surrogate import BiomedicalConceptSurrogate
from usdm_excel.document.utility import get_soup

class Macros():

  def __init__(self, parent: BaseSheet, study: Study):
    self.parent = parent
    self.study = study
    self.study_version = study.versions[0]
    self.study_design = self.study_version.studyDesigns[0]
    self.protocol_document_version = self.study.documentedBy.versions[0]
    self.elements = Elements(parent, self.study)
    self.m11 = TemplateM11(parent, self.study)
    self.plain = TemplatePlain(parent, self.study)
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
          self.parent._general_error(f"Failed to resolve document macro '{attributes}', invalid method name {method}")
          ref.replace_with('Missing content: invalid method name')
      except Exception as e:
        self.parent._general_exception(f"Failed to resolve document macro '{attributes}'", e)
        ref.replace_with('Missing content: exception')
    return str(soup)

  def _xref(self, attributes, soup, ref) -> None:
    instance, attribute = self.parent.globals.cross_references.get_by_path(attributes['klass'], attributes['name'], attributes['attribute'])
    ref_tag = soup.new_tag("usdm:ref")
    ref_tag.attrs = {'klass': instance.__class__.__name__, 'id': instance.id, 'attribute': attribute}
    ref.replace_with(ref_tag)
      
  def _bc(self, attributes, soup, ref) -> None:
    bc_name = attributes['name'].upper().strip()
    activity_name = attributes['activity'].strip()
    activity = self.parent.globals.cross_references.get(Activity, activity_name)
    if activity:
      bc = None
      for collection in [{'klass': BiomedicalConcept, 'ids': activity.biomedicalConceptIds, 'synonyms': True}, 
                         {'klass': BiomedicalConceptSurrogate, 'ids': activity.bcSurrogateIds, 'synonyms': False}]:
        for id in collection['ids']:
          next_bc = self.parent.globals.cross_references.get_by_id(collection['klass'], id)
          if next_bc:
            if bc_name == next_bc.name.upper() or bc_name in [x.upper() for x in next_bc.synonyms]:
              bc = next_bc
              break
      if bc:      
        ref_tag = soup.new_tag("usdm:ref")
        ref_tag.attrs = {'klass': bc.__class__.__name__, 'id': bc.id, 'attribute': 'label'}
        ref.replace_with(ref_tag)
      else:
        self.parent._general_error(f"Failed to find BC name '{bc_name}' in activity '{activity_name}'")
        ref.replace_with('Missing BC: failed to find BC in activity')
    else:
      self.parent._general_error(f"Failed to find  activity '{activity_name}'")
      ref.replace_with('Missing activity: failed to find activity')

  def _image(self, attributes, soup, ref) -> None:
    type = attributes['type']
    data = self._encode_image(attributes['file'])
    if data:
      img_tag = soup.new_tag("img")
      img_tag.attrs['src'] = f"data:image/{type};base64,{data.decode('ascii')}"
      img_tag.attrs['alt'] = "Alt text"
      ref.replace_with(img_tag)
    else:
      self._note({'text': f"Failed to insert image '{attributes['file']}', ignoring!"}, soup, ref)

  def _element(self, attributes, soup, ref) -> None:
    method = attributes['name'].lower()
    if self.elements.valid_method(method):
      text = getattr(self.elements, method)()
      ref.replace_with(get_soup(text, self.parent))
    else:
      self.parent._general_error(f"Failed to translate element method name '{method}' in '{attributes}', invalid method")
      ref.replace_with('Missing content: invalid method name')

  def _section(self, attributes, soup, ref) -> None:
    method = attributes['name'].lower()
    template = attributes['template'] if 'template' in attributes else 'plain' 
    instance = self._resolve_template(template)
    if instance.valid_method(method):
      text = getattr(instance, method)(attributes)
      ref.replace_with(get_soup(text, self.parent))
    else:
      self.parent._general_error(f"Failed to translate section method name '{method}' in '{attributes}', invalid method")
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
    return name in ['_xref', '_image', '_element', '_section', '_note', '_bc']
  
  def _resolve_template(self, template) -> object:
    try:
      return self.template_map[template.lower()]
    except:
      self.parent._general_error(f"Failed to map template '{template}', using plain template")
      return self.plain

  def _encode_image(self, filename) -> bytes:
    try:
      with open(os.path.join(self.parent.dir_path, filename), "rb") as image_file:
        data = base64.b64encode(image_file.read())
      return data
    except:
      self.parent._general_error(f"Failed to open image file '{filename}', ignored")
      return None
      