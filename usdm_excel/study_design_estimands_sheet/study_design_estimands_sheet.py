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
      current = None
      for index, row in self.sheet.iterrows():
        #e_xref = self.clean_cell(row, index, "xref") # Not needed as yet
        e_summary = self.clean_cell(row, index, "summaryMeasure")
        ap_description = self.clean_cell(row, index, "populationDescription")
        ice_name = self.clean_cell(row, index, "intercurrentEventName")
        ice_description = self.clean_cell(row, index, "intercurrentEventDescription")
        ice_strategy = self.clean_cell(row, index, "intercurrentEventStrategy")
        treatment_xref = self.clean_cell(row, index, "treatmentXref")
        #print("XREF1:", treatment_xref)
        treatment_id = cross_references.get(treatment_xref)
        #print("XREF2:", treatment_id)
        endpoint_xref = self.clean_cell(row, index, "endpointXref")
        #print("XREF3:", endpoint_xref)
        endpoint_id = cross_references.get(endpoint_xref)
        #print("XREF4:", endpoint_id)
        if not e_summary == "":
          ap = AnalysisPopulation(analysisPopulationId=self.id_manager.build_id(AnalysisPopulation), populationDescription=ap_description) 
          current = Estimand(estimandId=self.id_manager.build_id(Estimand), summaryMeasure=e_summary, analysisPopulation=ap, treatment=treatment_id, variableOfInterest=endpoint_id, intercurrentEvents=[])
          self.estimands.append(current)  
        ice = IntercurrentEvent(intercurrentEventId=self.id_manager.build_id(IntercurrentEvent), intercurrentEventName=ice_name, intercurrentEventDescription=ice_description, intercurrentEventStrategy=ice_strategy)
        current.intercurrentEvents.append(ice)
    except Exception as e:
      print("Oops!", e, "occurred.")
      traceback.print_exc()
