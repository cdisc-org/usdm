# CDISC / Transcelerate DDF USDM Package

This package provides an implementation of the Digital Data Flow (DDF) CDISC / TransCelerate Unified Study Definitions Model (USDM). Two main parts are provided:

- Within the `usdm_model` directory are a set of classes reflecting the USDM model as transported using the DDF USDM API 
- Within the `usdm_excel` directory is a class, `USDMExcel`, that can be used to import an entire study definition from an excel file and build the equivalent json as defined by the API

# Warning

This package was, originally, not intended for public use and, consequently, only informal testing has been performed on the package to date. Formal testing has just begun. Use this at your own risk.

# Setup

Setup is via pip

`pip install usdm`

The package requires a single environment variable `CDISC_API_KEY` that should be set to your CDISC library API key. This is used to access CDISC CT and BC definitions in the CDISC library.

See below for a simple example program.

# USDM Model

Not further information as yet.

# Excel Import

## Example Program

The following code imports an Excel file (in the appropriate structure) and processes it. The data are then exported to a file in JSON API format. *Note: The logging is not needed.*

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

The content of each sheet is described below. Example workbooks can be found in the [CDISC Reference Architecture repo](https://github.com/cdisc-org/DDF-RA/tree/sprint-11/Deliverables/IG/examples). *Note: the link above points to the sprint 11 branch. This will be merged into the main branch prior to public review.*

#### CDISC Terminology

For those cells where CDISC codes are used the user can enter either the CDISC C Code, for example `C15602`, the CDISC submission value, for example `PHASE III TRIAL`, or the preferred term, for example `Phase III Trial`

#### External Terminology

For those cells where external CT is referenced the user can enter code in the form `<code system>: <code> = <decode>`. For example `SPONSOR: A = decode 1, SPONSOR: B = decode 2`.

### Identifiers and Cross References

Some content defined within the sheets contain unique identifiers such that the content can be cross referenced in other sheets. This is done so as to link content or expand definitions. Identifiers are simple strings that need to be unique within the workbook. There is a single definition and one or more cross references.

### Study Sheet

#### Sheet Name

`study`

#### Sheet Contents

The study sheet consists of two parts, the upper section for those single values and then a section for the potentially repeating protocol version informaion

For the single values, the keyword is in column A while the value is in column B. The order of the fields cannot be changed.

| Row | Row Name | Description | Format and Values |
| :--- | :--- | :--- | :--- |
| 1 | studyTitle | The study title | Text string |
| 2 | studyVersion | String version | Text string |
| 3 | studyType | The study type | CDISC code reference |
| 4 | studyPhase | The study phase | CDISC code reference |
| 5 | studyAcronym | The study acronym | Text string |
| 6 | studyRationale | the study rationale | Text string |
| 7 | businessTherapeuticAreas | The set of business therapuetic area codes | External CT code format. Likely filled with sponsor terms |

A header row in row 9 followed by repeating rows from row 10, containing a protocol version definition: 

| Column | Column Name | Description | Format and Values |
| :--- | :--- | :--- | :--- |
| A | briefTitle | The brief title | Text string | 
| B | officialTitle	 | The officiall title | Text string| 
| C | publicTitle	 | The public title | Text string| 
| D | scientificTitle	 | The scientific title | Text string| 
| E | protocolVersion	 | The version of the protocol | Text string | 
| F | protocolAmendment	 |The version amendment | Text string | 
| G | protocolEffectiveDate	 | Effective date of the protocol | Date field, dd/mm/yyyy | 
| H | protocolStatus | The status | CDISC code reference | 

### Study Identifiers	Sheet
	
#### Sheet Name

`studyIdentifiers`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing a study identifier: 

| Column | Column Name | Description | Format and Values |
| :--- | :--- | :--- | :--- |
| A | organisationIdentifierScheme | The scheme for the organisation identifier. | Example would be 'DUNS' |
| B | organisationIdentifier | Organisation identifier | Text string |
| C | organisationName | Organisation name | Text string |
| D | organisationType | Organisation type | CDISC code reference |
| E | studyIdentifier | The identifier for the study | Text string |
| F | organisationAddress | The organisation address | Formated using a pipe delimited - allows for commas in items within the address - form, i.e. `line|city|district|state|postal_code|<country code>`. All fields are text strings except for `<country code>`. `<country code>` is either a two or three character ISO-3166 country code. |

### Study Design sheet

#### Sheet Name

`studyDesign`

#### Sheet Contents

The study design sheet consists of two parts, the upper section for those single values and then a section for the arms and epochs.

For the single values, the keyword is in column A while the value is in column B. The order of the fields cannot be changed.

| Row | Row Name | Description | Format and Values |
| :--- | :--- | :--- | :--- |
| 1 | studyDesignName | Study design name | Text string |
| 2 | studyDesignDescription | Study design description | Text string |
| 3 | therapeuticAreas | Set of therapeutic area codes | Set of external CT references, comma separated |
| 4 | studyDesignRationale | Study design rationale | Text string |
| 5 | studyDesignBlindingScheme | Code for the blinding scheme | CDISC code reference |
| 6 | trialIntentTypes | Codes for the trial intent types | Comma separated CDISC code references |
| 7 | trialTypes | Code for the trial type | CDISC code reference|
| 8 | interventionModel | | CDISC code reference |
| 9 | mainTimeline | Name of main timeline sheet | This must be present |
| 10 | otherTimelines | Names of other timeline sheeText string | Commma separated list of sheet names. Can be empty |

For the arms and epochs, a simple table is required. The table starts in row 12 and can consists of a header row and 1 or more arm rows. 

The header row consists of a cell that is ignored followed by 1 or more cells containing the epoch names.

The arm rows consist of the arm name in the first column followed by a cells for each epoch containing one or more references to study design elements defined in the studyDesignElements sheet.

### Timeline sheets

#### Sheet Name

As defined within the study design sheet, see above.

#### Sheet Contents

Not currently described

### Study Design Indications and Interventions Sheet
	
#### Sheet Name

`studyDesignII`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing an indication or intervention: 

| Column | Column Name | Description | Format and Values |
| :--- | :--- | :--- | :--- |
| A | Identifier | The identifier | Text string | 
| B | type | The type, either `IND` for indication or `INT` for intervention | Text string |
| C | description | A Text string description for the indication or intervvention | Text string |
| D | codes | The set of indication or intervention codes | A set of external CT codes, comma separated |	

### Study Design Populations sheet

#### Sheet Name

`studyDesignPopulations`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing a population definition: 

| Column | Column Name | Description | Format and Values |
| :--- | :--- | :--- | :--- |
| A | populationDescription	| Description of the population | Text string | 
| B | plannedNumberOfParticipants	| Number of participants | Integer | 
| C | plannedMinimumAgeOfParticipants	| Min age | Text string | 
| D | plannedMaximumAgeOfParticipants	| Mas Age | Text string |
| E | plannedSexOfParticipants | Sex of participants | CDISC code reference | 

### Study Design Objectives and Endpoints sheet

#### Sheet Name

`studyDesignOE`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing objective and endpoint definitions. Note that columns D through G can repeat for the same content in columns A to C. For additional endpoint rows leave columns A to C blank.

| Column | Column Name | Description | Format and Values |
| :--- | :--- | :--- | :--- |
| A | objectiveXref	| Identifier | Text string |
| B | objectiveDescription	| Description | Text string |
| C | objectiveLevel	| Objective level | CDISC code reference |
| D | endpointXref	| Identifier | Text string. Note columns D to G can repeat for each endpoiint for an objective |
| E | endpointDescription	| Description | Text string |
| F | endpointPurposeDescription	| | |
| G | endpointLevel| Level | CDISC code reference |

### Study Design Estimands sheet

#### Sheet Name

`studyDesignEstimands`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing estimand definitions. Note that column H can repeat for the same content in columns A through G.

| Column | Column Name | Description | Format and Values |
| :--- | :--- | :--- | :--- |
| A | xref	| Identifier | Text string |
| B | summaryMeasure	| The summary measure | Text string |
| C | populationDescription	| Description | Text string |
| D | intercurrentEventName	| Name | Text string |
| E | intercurrentEventDescription | Description | Text string |
| F | treatmentXref	| Treatment cross reference | Cross reference to a treatment |
| G | endpointXref	| Endpoint cross reference | Cross reference to an endpont |
| H | intercurrentEventstrategy| Strategy | Text string. This column can be repeated fo reach intercurrent event rerquired for the Estimand |

### Study Design Procedures sheet

#### Sheet Name

`studyDesignProcedures`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing procedure definitions.

| Column | Column Name | Description | Format and Values |
| :--- | :--- | :--- | :--- |
| A | xref | Identifier | Text string |
| B | procedureType	| Type | Text string |
| C | procedureCode	| Code reference | External CT reference  |
| D | procedureIsConditional | Conditional flag | Boolean |
| E | procedureIsConditionalReason | Reason | Text string |

### Study Design Encounters sheet

#### Sheet Name

`studyDesignEncounters`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing encounter definitions.

| Column | Column Name | Description | Format and Values |
| :--- | :--- | :--- | :--- |
| A | xref	| Identifier | Text string |
| B | encounterName	| Name | Text string |
| C | encounterDescription	| Description | Text string |
| D | encounterType	| The type | CDISC code reference |
| E | encounterEnvironmentalSetting	| Encounter environment | CDISC code reference |
| F | encounterContactModes	| Contact modes | CDISC code reference |
| G | transitionStartRule	| Start rule | Text string |
| H | transitionEndRule| End Rule | Text string |

### Study Design Elements sheet

#### Sheet Name

`studyDesignElements`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing element definitions.

| Column | Column Name | Description | Format and Values |
| :--- | :--- | :--- | :--- |
| A | xref | Identifier | Text string |	
| B | studyElementName | Name | Text string |	
| C | studyElementDescription | Description | Text string |	
| D | transitionStartRule | Start rule | Text string |	
| E | transitionEndRule | End rule | Text string |

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
- Better handlingof content in timeline sheet (remove need for '-' characters)