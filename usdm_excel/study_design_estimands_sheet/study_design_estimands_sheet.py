from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
import traceback
import pandas as pd
from usdm.intercurrent_event import IntercurrentEvent
from usdm.analysis_population import AnalysisPopulation
from usdm.estimand import Estimand
from usdm_excel.cdisc_ct_library import cdisc_ct_library
from usdm_excel.cdisc_ct import CDISCCT

class StudyDesignEstimandsSheet(BaseSheet):

  def __init__(self, file_path, id_manager):
    try:
      super().__init__(pd.read_excel(open(file_path, 'rb'), sheet_name='studyDesignEstimands'), id_manager)
      self.estimands = []
      for index, row in self.sheet.iterrows():
        #e_xref = self.clean_cell(row, index, "xref") # Not needed as yet
        e_summary = self.clean_cell(row, index, "summaryMeasure")
        ap_description = self.clean_cell(row, index, "populationDescription")
        ice_name = self.clean_cell(row, index, "intercurrentEventName")
        ice_description = self.clean_cell(row, index, "intercurrentEventDescription")
        ice_strategy = self.clean_cell(row, index, "intercurrentEventStrategy")
        treatment_xref = self.clean_cell(row, index, "treatmentXref")
        treament_id = cross_references.get(treatment_xref)
        endpoint_xref = self.clean_cell(row, index, "endpointXref")
        endpoint_id = cross_references.get(endpoint_xref)
  
        ice = IntercurrentEvent(intercurrentEventId=self.id_manager.build_id(IntercurrentEvent), intercurrentEventName=ice_name, intercurrentEventDescription=ice_description, intercurrentEventStrategy=ice_strategy)
        ap = AnalysisPopulation(analysisPopulationId=self.id_manager.build_id(AnalysisPopulation), populationDescription=ap_description) 
        est = Estimand(estimandId=self.id_manager.build_id(Estimand), summaryMeasure=e_summary, analysisPopulation=ap, treatment=treament_id, variableOfInterest=endpoint_id, intercurrentEvents=[ice])
        self.estimands.append(est)
    except Exception as e:
      print("Oops!", e, "occurred.")
      traceback.print_exc()
