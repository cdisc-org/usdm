from .activity import Activity
from .code import *
from .encounter import *
from .endpoint import *
from .estimand import *
from .indication import *
from .intercurrent_event import *
from .investigational_intervention import *
from .objective import *
from .organisation import *
from .analysis_population import *
from .study_design_population import *
from .procedure import *
from .transition_rule import *
from .study_arm import *
from .study_cell import *
from .study_data import *
from .study_design import *
from .study_element import *
from .study_epoch import *
from .study_identifier import *
from .study_protocol_version import *
from .study import *
from .workflow import *
from .workflow_item import *

class Klass():

  def get(name):
    return globals()[name]
