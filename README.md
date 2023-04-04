# USDM CDISC / Transcelerate DDF USDM

This package provides an implementation of the Digital Data Flow (DDF) CDISC / TransCelerate Unified Study Definitions Model (USDM). Two main parts are provided:

- Within the `usdm_model` directory are a set of classes reflecting the USDM model as transported using the DDF USDM API 
- Within the `usdm_excel` directory is a class, `USDMExcel`, that can be used to import an entire study definition from an excel file and build the equivalent json as defined by the API

# Warning

When originally written, this package was not intended for public use and, consequently, only informal testing has been performed on the package. 

Formal testing has just begun. Use this at your own risk.

# Setup

Setup is via pip

`pip install usdm`

The package requires a single environment variable `CDISC_API_KEY` that should be set to your CDISC library API key. This is used to access CDISC CT and BC definitions.

See below for a simple example program.

# USDM Model

Not further information as yet.

# Excel Import

## Example Program

The following code imports an Excel file (in the appropriate structure) and processes it. The data are then exported to a file in JSON API format.

Note: The logging is not needed.
```
import logging
log = logging.basicConfig(level=logging.INFO)

import json
from usdm_excel import USDMExcel

excel = USDMExcel("source_data/simple_1.xlsx")
with open('source_data/simple_1.json', 'w', encoding='utf-8') as f:
  f.write(json.dumps(json.loads(excel.to_json()), indent=2))
```

## Format of Workbook

### General

#### Sheets

The workbook consists of several sheets each with a dedicated purpose.

- Study sheet
- Study Identifiers sheet
- Study Design sheet
- one or more Timeline sheets
- Study Design Indications and Interventions sheet
- Study Design Populations sheet
- Study Design Objectives and Endpoints sheet
- Study Design Estimands sheet
- Study Design Procedures sheet
- Study Design Encounters sheet
- Study Design Elements sheet
- Configuration sheet

The content of each sheet is described below

#### CDISC Terminology

For those cells  where CDISC codes are used the user can enter either the CDISC C Code, for example `C15602`, the CDISC submission value, for example `PHASE III TRIAL`, or the preferred term, for example `Phase III Trial`

### Study Sheet

#### Sheet Name

`study`

#### Sheet Contents

The study sheet consists of two parts, the upper section for those single values and then a section for the potentially repeating protocol version informaion

For the single values, the keyword is in column A while the value is in column B. The order of the fields cannot be changed.

| Row Name | Description | Format and Values |
| :--- | :--- | :--- |
| studyTitle | The study title | Simple text string |
| studyVersion | String version | Simple text string |
| studyType | CDISC code | String. Either the C Code, the submission value or the preferred term for the term desired. |
| studyPhase | CDISC code | String. Either the C Code, the submission value or the preferred term for the term desired.  |
| studyAcronym | The study acronym | |
| studyRationale | the study rationale | |
| businessTherapeuticAreas | The set of business therapuetic area codes | Each code is of the form `<code system>: <code> = <decode>`. For example `SPONSOR: A = decode 1, SPONSOR: B = decode 2`. Likely filled with sponsor terms |

For each Study Protocol Version a row containing:

| Column Name | Description | Format and Values |
| :--- | :--- | :--- |
| briefTitle | The brief title | Simple text string | 
| officialTitle	 | The officiall title | Simple text string| 
| publicTitle	 | The public title | Simple text string| 
| scientificTitle	 | The scientific title | Simple text string| 
| protocolVersion	 | The version of the protocol | Simple text string | 
| protocolAmendment	 |The version amendment | Simple text string | 
| protocolEffectiveDate	 | Effective date of the protocol | Date field, dd/mm/yyyy | 
| protocolStatus | | String. Either the C Code, the submission value or the preferred term for the term desired.  | 

### Study Identifiers	Sheet
	
#### Sheet Name

`study`

#### Sheet Contents

| Column Name | Description | Format and Values |
| :--- | :--- | :--- |
| organisationIdentifierScheme | The scheme for the organisation identifier.  | Example would be 'DUNS' |
| organisationIdentifier | Organisation identifier | A text string |
| organisationName | Organisation name | A text string |
| organisationType | Organisation type | Set to either `registry`, `sponsor` or `regulatory` |
| studyIdentifier | The identifier for the study | A text string |
| organisationAddress | The organisation address | Formated using a pipe delimited - allows for commas in items within the address - form, i.e. `line|city|district|state|postal_code|<country code>`. All fields are free text except for `<country code>`. `<country code>` is either a two or three character ISO-3166 country code. |

- Study Design sheet
- one or more Timeline sheets

### Study Design Indications and Interventions Sheet
	
#### Sheet Name

`studyDesignII`

#### Sheet Contents

| Column Name | Description | Format and Values |
| :--- | :--- | :--- |
| type | The type, either IND for indication or INT for intervention ||
| description | A free text description for the indication or intervvention ||
| codes | A set of codes, comma separated | Each code is of the form `<code system>: <code> = <decode>`. For example `SNOMED: 12345678 = decode, ICD-10: code = decode` |	

### Study Design Populations sheet

#### Sheet Name

`studyDesignPopulations`

#### Sheet Contents

### Study Design Objectives and Endpoints sheet

#### Sheet Name

`studyDesignOE`

#### Sheet Contents

### Study Design Estimands sheet

#### Sheet Name

`studyDesignEstimands`

#### Sheet Contents

### Study Design Procedures sheet

#### Sheet Name

`studyDesignProcedures`

#### Sheet Contents

### Study Design Encounters sheet

#### Sheet Name

`studyDesignEncounters`

#### Sheet Contents

### Study Design Elements sheet

#### Sheet Name

`studyDesignElements`

#### Sheet Contents

### Configuration Sheet

#### Sheet Name

`configuration`

#### Sheet Contents

A set of rows consisting of configuration parameters. The first column is the type of configuration parameter while the second is the value. The values for specific parameters may vary in their format

| Parameter | Description | Format and Values |
| :--- | :--- | :--- |
| CT Version | Allows for the version of a specific external CT to be set. Multiple rows can be included to set the versions for several CTs | Of the form CT name = Version value, For example `SNOMED = 21st June 2012`|

### Content Not Suported As Yet

It is intended to support all of the content in the USDM. The following features are not yet supported:

- Full Arm definitions
- Full Epoch definitions