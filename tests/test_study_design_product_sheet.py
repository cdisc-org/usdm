import pandas as pd
from usdm_excel.study_design_intervention_sheet.study_design_product_sheet import StudyDesignProductSheet
from usdm_excel.base_sheet import BaseSheet
from usdm_model.code import Code

def test_create_1(mocker, globals):
  ids = ['Id_1', 'Id_2', 'Id_3', 'Id_4', 'Id_5', 'Id_6', 'Id_7', 'Id_8', 'Id_9', 'Id_10', 'Id_11', 'Id_12', 'Id_13', 'Id_14']
  expected = ( 
    '{"id": "Id_4", "name": "60 mg Study Drug", "label": "label 1", "description": "description 1", "pharmacologicClass": '
      '{"id": "Id_3", "code": "A", "codeSystem": "FDA", "codeSystemVersion": "", "decode": "B", "instanceType": "Code"}, '
    '"administrableDoseForm": '
      '{"id": "Id_2", '
        '"standardCode": {"id": "Id_1", "code": "C42998", "codeSystem": "http://www.cdisc.org", "codeSystemVersion": "2023-12-15", "decode": "Tablet Dosage Form", "instanceType": "Code"}, '
        '"standardCodeAliases": [], '
        '"instanceType": "AliasCode"}, '
      '"properties": [], "identifiers": [], '
      '"ingredients": '
        '[{"id": "Id_7", "role": '
          '{"id": "Id_6", "code": "100000072072", "codeSystem": "HL7", "codeSystemVersion": "", "decode": "Active", "instanceType": "Code"}, '
        '"substance": '
          '{"id": "Id_5", "name": "Ingredient C", "label": "label 2", "description": "description 2", "codes": [], '
          '"strengths": '
            '[{"id": "Id_14", "name": "60 mg", "label": "", "description": "", '
            '"denominator": '
              '{"id": "Id_13", "value": 1.0, '
              '"unit": '
                '{"id": "Id_12", '
                '"standardCode": '
                  '{"id": "Id_11", "code": "C48542", "codeSystem": "http://www.cdisc.org", "codeSystemVersion": "2023-12-15", "decode": "Tablet Dosing Unit", "instanceType": "Code"}, '
                '"standardCodeAliases": [], "instanceType": "AliasCode"}, '
              '"instanceType": "Quantity"}, '
            '"numerator": {"id": "Id_10", "value": 60.0, '
              '"unit": {"id": "Id_9", '
                '"standardCode": {"id": "Id_8", "code": "C28253", "codeSystem": "http://www.cdisc.org", "codeSystemVersion": "2023-12-15", "decode": "Milligram", "instanceType": "Code"}, '
                '"standardCodeAliases": [], "instanceType": "AliasCode"}, '
              '"instanceType": "Quantity"}, '
            '"instanceType": "Strength"}], '
          '"referenceSubstance": null, "instanceType": "Substance"}, '
        '"instanceType": "Ingredient"}], "notes": [], '
      '"instanceType": "AdministrableProduct"}'
  )
  data = {
    'name': ['60 mg Study Drug'],
    'description': ['description 1'],
    'label': ['label 1'],
    'pharmacologicClass': ['FDA: A=B'],
    'administrableDoseForm': ['TABLET'],
    'ingredientRole': ['HL7:   100000072072=Active'],
    'substanceName': ['Ingredient C'],
    'substanceDescription': ['description 2'],
    'substanceLabel': ['label 2'],
    'substanceCode': [''],
    'strengthName': ['60 mg'],
    'strengthDescription': [''],
    'strengthLabel': [''],
    'strengthNumerator': ['60 mg'],
    'strengthDenominator': ['1 TABLET'],
    'referenceSubstanceName': [''],
    'referenceSubstanceDescription': [''],
    'referenceSubstanceLabel': [''],
    'referenceSubstanceCode': [''],
    'referenceSubstanceStrengthName': [''],
    'referenceSubstanceStrengthDescription': [''],
    'referenceSubstanceStrengthLabel': [''],
    'referenceSubstanceStrengthNumerator': [''],
    'referenceSubstanceStrengthDenominator': ['']
  }  
  sheet = _setup_sheet(mocker, globals, data, ids)
  assert str(sheet.items[0].to_json()) == expected

def test_create_2(mocker, globals):
  ids = [
     'Id_1',  'Id_2',  'Id_3',  'Id_4',  'Id_5',  'Id_6',  'Id_7',  'Id_8',  'Id_9', 'Id_10', 
    'Id_11', 'Id_12', 'Id_13', 'Id_14', 'Id_15', 'Id_16', 'Id_17', 'Id_18', 'Id_19', 'Id_20',
    'Id_21', 'Id_22', 'Id_23', 'Id_24', 'Id_25', 'Id_26', 'Id_27', 'Id_28', 'Id_29', 'Id_30'
  ]
  data = {
    'name': ['60 mg Study Drug', ''],
    'description': ['description 1', ''],
    'label': ['label 1', ''],
    'pharmacologicClass': ['FDA: A=B', ''],
    'administrableDoseForm': ['TABLET', ''],
    'ingredientRole': ['HL7:   100000072072=Active', 'HL7:   100000072072=Active'],
    'substanceName': ['Ingredient C', 'Ingredient D'],
    'substanceDescription': ['description 2', 'description 3'],
    'substanceLabel': ['label 2', 'label 3'],
    'substanceCode': ['', ''],
    'strengthName': ['60 mg', '120 mg'],
    'strengthDescription': ['', ''],
    'strengthLabel': ['', ''],
    'strengthNumerator': ['60 mg', '120 mg'],
    'strengthDenominator': ['1 TABLET', '1 TABLET'],
    'referenceSubstanceName': ['', ''],
    'referenceSubstanceDescription': ['', ''],
    'referenceSubstanceLabel': ['', ''],
    'referenceSubstanceCode': ['', ''],
    'referenceSubstanceStrengthName': ['', ''],
    'referenceSubstanceStrengthDescription': ['', ''],
    'referenceSubstanceStrengthLabel': ['', ''],
    'referenceSubstanceStrengthNumerator': ['', ''],
    'referenceSubstanceStrengthDenominator': ['', '']
  }  
  sheet = _setup_sheet(mocker, globals, data, ids)
  assert sheet.items[0].ingredients[0].substance.name == 'Ingredient C'
  assert sheet.items[0].ingredients[1].substance.name == 'Ingredient D'

def test_create_3(mocker, globals):
  ids = [
     'Id_1',  'Id_2',  'Id_3',  'Id_4',  'Id_5',  'Id_6',  'Id_7',  'Id_8',  'Id_9', 'Id_10', 
    'Id_11', 'Id_12', 'Id_13', 'Id_14', 'Id_15', 'Id_16', 'Id_17', 'Id_18', 'Id_19', 'Id_20',
    'Id_21', 'Id_22', 'Id_23', 'Id_24', 'Id_25', 'Id_26', 'Id_27', 'Id_28', 'Id_29', 'Id_30',
    'Id_31', 'Id_32', 'Id_33', 'Id_34', 'Id_35', 'Id_36', 'Id_37', 'Id_38', 'Id_39', 'Id_40',
  ]
  data = {
    'name': ['60 mg Study Drug', ''],
    'description': ['description 1', ''],
    'label': ['label 1', ''],
    'pharmacologicClass': ['FDA: A=B', ''],
    'administrableDoseForm': ['TABLET', ''],
    'ingredientRole': ['HL7:   100000072072=Active', 'HL7:   100000072072=Active'],
    'substanceName': ['Ingredient C', 'Ingredient D'],
    'substanceDescription': ['description 2', 'description 3'],
    'substanceLabel': ['label 2', 'label 3'],
    'substanceCode': ['', ''],
    'strengthName': ['60 mg', '120 mg'],
    'strengthDescription': ['', ''],
    'strengthLabel': ['', ''],
    'strengthNumerator': ['60 mg', '120 mg'],
    'strengthDenominator': ['1 TABLET', '1 TABLET'],
    'referenceSubstanceName': ['', 'albuterol base'],
    'referenceSubstanceDescription': ['', 'Reference description'],
    'referenceSubstanceLabel': ['', 'Reference label'],
    'referenceSubstanceCode': ['', ''],
    'referenceSubstanceStrengthName': ['', '90 μg'],
    'referenceSubstanceStrengthDescription': ['', 'Ref strength description'],
    'referenceSubstanceStrengthLabel': ['', 'Ref strength label'],
    'referenceSubstanceStrengthNumerator': ['', '90	ug'],
    'referenceSubstanceStrengthDenominator': ['', '1	INHALATION']
  }  
  sheet = _setup_sheet(mocker, globals, data, ids)
  assert sheet.items[0].ingredients[0].substance.referenceSubstance == None
  assert sheet.items[0].ingredients[1].substance.referenceSubstance.name == 'albuterol base'
  assert sheet.items[0].ingredients[1].substance.referenceSubstance.strengths[0].name == '90 μg'

def test_missign_column_error(mocker, globals):
  ids = ['Id_1', 'Id_2', 'Id_3', 'Id_4', 'Id_5', 'Id_6', 'Id_7', 'Id_8', 'Id_9', 'Id_10', 'Id_11', 'Id_12', 'Id_13', 'Id_14']
  data = {
    'name': ['60 mg Study Drug'],
    'description': ['description 1'],
    'label': ['label 1'],
    'administrableDoseForm': ['TABLET'],
    'ingredientRole': ['HL7:   100000072072=Active'],
    'substanceName': ['Ingredient C'],
    'substanceDescription': ['description 2'],
    'substanceLabel': ['label 2'],
    'substanceCode': [''],
    'strengthName': ['60 mg'],
    'strengthDescription': [''],
    'strengthLabel': [''],
    'strengthNumerator': ['60 mg'],
    'strengthDenominator': ['1 TABLET'],
    'referenceSubstanceName': [''],
    'referenceSubstanceDescription': [''],
    'referenceSubstanceLabel': [''],
    'referenceSubstanceCode': [''],
    'referenceSubstanceStrengthName': [''],
    'referenceSubstanceStrengthDescription': [''],
    'referenceSubstanceStrengthLabel': [''],
    'referenceSubstanceStrengthNumerator': [''],
    'referenceSubstanceStrengthDenominator': ['']
  }  
  mock_error = mocker.patch("usdm_excel.errors_and_logging.errors.Errors.add")
  sheet = _setup_sheet(mocker, globals, data, ids)
  assert mock_error.call_count == 1
  mock_error.assert_has_calls([mocker.call('studyDesignProducts', None, None, "Exception. Error [Failed to detect column(s) 'pharmacologicClass' in sheet] while reading sheet 'studyDesignProducts'. See log for additional details.", 40)])

def _setup_sheet(mocker, globals, data, ids):
  globals.cross_references.clear()
  mock_present = mocker.patch("usdm_excel.base_sheet.BaseSheet._sheet_present")
  mock_present.side_effect=[True]
  mock_id = mocker.patch("usdm_excel.id_manager.IdManager.build_id")
  mock_id.side_effect=ids
  mocked_open = mocker.mock_open(read_data="File")
  mocker.patch("builtins.open", mocked_open)
  mock_read = mocker.patch("pandas.read_excel")
  mock_read.return_value = pd.DataFrame.from_dict(data)
  return StudyDesignProductSheet("", globals)
