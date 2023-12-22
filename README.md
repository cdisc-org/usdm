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

### Example

An example spreadsheet in maintained within the [document directory](https://github.com/data4knowledge/usdm/tree/main/docs).

### Sheets

The workbook consists of several sheets each with a dedicated purpose. All sheets must be present except for those marked optional.

- Study sheet
- Study Identifiers sheet
- Study Amendments sheet
- Study Design sheet
- One or more Timeline sheets
- Study Design Timing sheet
- Study Design Activities sheet (optional)
- Study Design Indications sheet
- Study Design Interventions sheet
- Study Design Populations sheet
- Study Design Objectives and Endpoints sheet
- Study Design Eligibility Criteria sheet
- Study Design Estimands sheet
- Study Design Procedures sheet
- Study Design Encounters sheet
- Study Design Elements sheet
- Study Design Content sheet
- Study Design Sites sheet
- Dictionaries Sheet
- Configuration sheet

The content of each sheet is described below. 

### CDISC Terminology

For those cells where CDISC codes are used the user can enter either the CDISC C Code, for example `C15602`, the CDISC submission value, for example `PHASE III TRIAL`, or the preferred term, for example `Phase III Trial`

### Multiple Values

Some cells allow for multiple values. These are all comma separated. If users wish to include a comma within such strings then the string can be enclosed in quotes. For example `123, "123,456", 789`.

### External Terminology

For those cells where external CT is referenced the user can enter code in the form `<code system>: <code> = <decode>`. For example `SPONSOR: A = decode 1, SPONSOR: B = decode 2`. Where multiple codes are needed then the values are separated by commas.

### Boolean Values

For boolean fields the following can be used to indicate a `true` value `'Y', 'YES', 'T', 'TRUE', '1'` or the lower case equivalents.

### Address Values

An address is of the form: ```line,district,city,state,postal_code,<country code>```. All fields are text strings except for `<country code>`. `<country code>` is either a two or three character ISO-3166 country code. Note that `|` can be used in place of the commas for backward compatibility.

### Identifiers and Cross References

Some content defined within the sheets contain unique identifiers such that the content can be cross referenced in other sheets. This is done so as to link content or expand definitions. Identifiers are simple strings that need to be unique within the workbook. There is a single definition and one or more cross references.

See the [infographic](https://github.com/data4knowledge/usdm/blob/main/docs/sheets.png) for further information.

### Timing Values

A number of fields specify timing values, either single relative values or ranges. These can be entered as
a *Timing Value* of ```<value> <unit>``` or a *Timing Range* of ```<lower>..<upper> <unit>```. The unit can be entered as follows:

- Years: 'Y', 'YRS', 'YR', 'YEARS', 'YEAR'
- Months: 'MTHS', 'MTH', 'MONTHS', 'MONTH'
- Weeks: 'W', 'WKS', 'WK', 'WEEKS', 'WEEK'
- Days: 'D', 'DYS', 'DY', 'DAYS', 'DAY'
- Hours: 'H', 'HRS', 'HR', 'HOURS', 'HOUR'
- Minutes: 'M', 'MINS', 'MIN', 'MINUTES', 'MINUTE'
- Seconds: 'S', 'SECS', 'SEC', 'SECONDS', 'SECOND'

So ```3 Y```, ```3 YRS```, ```3 YR```, ```3 YEARS```, ```3 YEAR``` are all equivalent. Only a single value and unit should be entered, i.e. combination values are not supported.

### Templated Text

Some entries can include "tags" that allow the text to reference structured content from elsewhere in the model. An example is an activity name. These sections of text are formatted as `[tag_name]` within the text. The `tag_name` refers to an entry within a dictionary (see the dictionaries sheet)

An example of Templated Text is `Subjects shall be between [min_age] and [max_age]` where the min and max ages will be inserted using the dictionary entries that refer to particular attribute values from within the structured parts of the model.

### Sheet Descriptions

The sheet descriptions detail the fields found within each sheet and the details of the data required. Note:

- Some fields have multiple names due to model changes and a desire to preserve backwards compatibility. Any of the choices documented can be used. 
- Some columns are optional and thus can be included or omitted. Again this is to preserve backwards compatibility. A default value is specified if the column is not included.

### Study Sheet

#### Sheet Name

`study`

#### Sheet Contents

The study sheet consists of two parts, the upper section for those single values and then a section for the potentially repeating protocol version informaion

For the single values, the keyword is in column A while the value is in column B. 

| Row | Row Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| 1 | studyTitle | The study title | Text string |
| 2 | studyVersion | String version | Text string |
| 3 | studyType or type | The study type | CDISC code reference |
| 4 | studyPhase | The study phase | CDISC code reference |
| 5 | studyAcronym | The study acronym | Text string |
| 6 | studyRationale | the study rationale | Text string |
| 7 | businessTherapeuticAreas | The set of business therapuetic area codes | External CT code format. Likely filled with sponsor terms |
| 8 | briefTitle | The brief title | Text string | 
| 9 | officialTitle	 | The officiall title | Text string| 
| 10 | publicTitle	 | The public title | Text string| 
| 11 | scientificTitle	 | The scientific title | Text string| 
| 12 | protocolVersion	 | The version of the protocol | Text string | 
| 13 | protocolStatus | The status | CDISC code reference | 

A header row in row 16 followed by repeating rows from row 17, containing a series of dates: 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | category | The date category | Either `study_version` or `protocol_document` for a date that applies to the study version or the document | 
| B | name | A name for the date | text string | 
| C | description	| A date description | Text string, can be blank | 
| D | label	| A date label | Text string| 
| E | type | the type of date | CDISC code reference | 
| F | date| The date | Date field, dd/mm/yyyy | 
| H | scopes | The geographic scopes for the date | Geographic scoped, see below |

The geographic is of the form: `Global`, `Region: <region>` or , `Country: <country>`. Regions and Countries are taken from the ISO3166 value set. Examples are `Global` or `Region: Europe, Country: USA`. Where multiple codes are needed then the values are separated by commas. Note, if a global entry is specified then no other values are required and will be ignored. 

### Study Identifiers	Sheet
	
#### Sheet Name

`studyIdentifiers`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, each containing a study identifier: 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | organisationIdentifierScheme | The scheme for the organisation identifier. | Example would be 'DUNS' |
| B | organisationIdentifier | Organisation identifier | Text string |
| C | organisationName or name | Organisation name | Text string |
| D (optional) | label | Display label | Text string, can be empty. Default value is '' |
| E | organisationType or type | Organisation type | CDISC code reference |
| F | studyIdentifier | The identifier for the study | Text string |
| G | organisationAddress | The organisation address | Address |


### Study Amendments	Sheet
	
#### Sheet Name

`studyAmendments`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing a study amendment: 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | number | The amendment number | Integer |
| B | summary | The amendment summary | Text string |
| C | substantialImpact | True or false value  indicating if the amendment is substantial | Boolean |
| D | primaryReason | Primary reason for the amendment | CDISC code reference |
| E | secondaryReasons | Secondary reasons for amendment. Multiple values can be supplied separated by a comma | CDISC code reference |
| F | enrollment | The current state of subject enrollment, either global, regional or country | Geographic scoped, see below |

The enrollment data is of the form: `Global: <enrollment>`, `Region: <region>=<enrollment>` or , `Country: <country>=<enrollment>`. 
The enrollment is either a percentage or an absolute value. Regions and Countries are taken from the ISO3166 value set. Examples are `Global: 65%` or `Region: Europe=15, Country: USA=20%`. Where multiple codes are needed then the values are separated by commas. Note, if a global entry is specified then no other values are required and will be ignored.

The primary and secondary reasons should be set to one (primary) or one or more (secondary) values from the following reasons:

- Regulatory Agency Request To Amend
- New Regulatory Guidance
- IRB/IEC Feedback
- New Safety Information Available
- Manufacturing Change
- IMP Addition
- Change In Strategy
- Change In Standard Of Care
- New Data Available (Other Than Safety Data)
- Investigator/Site Feedback
- Recruitment Difficulty
- Inconsistency And/Or Error In The Protocol
- Protocol Design Error
- Other
- Not Applicable

### Study Design sheet

#### Sheet Name

`studyDesign`

#### Sheet Contents

The study design sheet consists of two parts, the upper section for those single values and then a section for the arms and epochs.

For the single values, the keyword is in column A while the value is in column B. Some rows can repeat

| Row Name | Purpose | Format and Values | Repeat |
| :--- | :--- | :--- | :--- |
| studyDesignName or name | Study design name | Text string | No | 
| studyDesignDescription or description | Study design description | Text string | No |
| label | Study design label. Default value is '' | Text string | No |
| therapeuticAreas | Set of therapeutic area codes | Set of external CT references, comma separated | No |
| studyDesignRationale | Study design rationale | Text string | No |
| studyDesignBlindingScheme | Code for the blinding scheme | CDISC code reference | No |
| trialIntentTypes | Codes for the trial intent types | Comma separated CDISC code references | No |
| trialTypes | Code for the trial type | CDISC code reference| No |
| interventionModel | | CDISC code reference | No |
| masking | A masking role | Takes form of Role=description where the role is a CDISC Code Reference | Yes |
| characteristics | Set of characteristics | Set of CDISC code references | No |
| mainTimeline | Name of main timeline sheet | This must be present | No |
| otherTimelines | Names of other timeline sheeText string | Commma separated list of sheet names. Can be empty | No |

For the arms and epochs, a simple table is required. The table starts in row 12 and can consists of a header row and 1 or more arm rows. 

The header row consists of a cell in column A that is ignored followed by 1 or more cells (columns) containing the epoch names. Each epoch name should have a corresponding entry in the Study Design Epochs sheet, see below.

The arm rows consist of the arm name in the first column followed by a cells for each epoch containing one or more references to study design elements defined in the studyDesignElements sheet. Each arm name should have a corresponding entry in the Study Design Arms sheet, see bwlow.

### Study Design Arms sheet

#### Sheet Name

`studyDesignArms`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing the details of a study arm: 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | studyArmName or name | Identifier | Text string. Should match an arm name in the Study Design sheet | 
| B | studyArmDescription or description | Description | Text string, can be empty |
| C (optional) | label | Display label | Text string, can be empty. Default value is '' |
| D | studyArmType or type | The arm type| CDISC code reference |
| E | studyArmDataOriginDescription or dataOriginDescription	| The description of the data origin for the arm | Text string |
| F | studyArmDataOriginType or dataOriginType | The type of arm data origin | CDISC code reference|

### Study Design Epochs sheet

#### Sheet Name

`studyDesignEpochs`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing the details of a study epoch: 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | studyEpochName or name | The epoch name | Text string. Should match an epoch name in the Study Design sheet | 
| B | studyEpochDescription or description | Description | Text string, can be empty |
| C (optional) | label | Display label | Text string, can be empty. Default value is '' |
| D | studyEpochType or type | The epoch type| CDISC code reference |

### V1 Timeline sheets

#### Sheet Name

As defined within the study design sheet, see above.

#### Sheet Contents

##### General

This is a complicated sheet. It is, in essence, an enhanced SoA. There are several sections within the sheet:

- The name, description and condition located top right
- The remainder of the sheet is the SoA with:
  - The timing set in the top rows, the "timepoints"
  - The activities down the left hand side
  - The link between activities and "timepoints", the classic 'X'

##### Name, Description, Condition

The name description and condition are located in columns A and B, rows 1 and 2. It is a vertical name value pair configuration

| Row | Row Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| 1 | Name | The timeline name | Text string |
| 2 | Description | Timeline description | Text string |
| 3 | Condition | Timeline entry condition | Text string |

##### Timing

The timing seciton consists of multiple columns starting in column D. As many columns as needed can be created. A title block is held in Column C. The section consists of eight rows in rows 1 to 8 as follows:

| Row | Row Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| 1 | Epoch | The name of the epoch within which the timepoint falls. Note the cells in this row can be merged to link an epoch with many timepoints | Text string  |
| 2 | Cycle | The cycle in which the "timepoint" exists. Can be empty or set to '-' (empty) | Text string |
| 3 | First Cycle Start | The time at which the cycle starts. Should be specified. Empty if not part of a cycle | Text string |
| 4 | Cycle Period | The cycle period. Shoudl be specified. Empty if not part of a cycle | Text string |
| 5 | Cycle End Rule | The cycle end rule. Can be empty. Empty if not part of a cycle | Text string |
| 6 | Timing | "Timepoint" timing.  | A timing string, see below |
| 7 | Encounter xref | Cross reference to the encounter in which the timepoint belongs. Can be empty | Text string |
| 8 | Window | Timing window. Can be empty | A *Timing Range* |

The timepont timing takes the form defined as follows (using pseudo BNF). 

```
<entry> ::= <type> [<count>] : [<relative timing>]
<type> ::= N | P| A | C
<count> ::= any positive integer (will default to 1)
<relative timing> ::= A single Timing Value
```
N = Next, P = Previous, A = Anchor and C = Cycle Start. The count when used with N or P indicates a relative to the Nth next or previous timepoint. When not specificed it defaults to 1.

`P2: +14 Days` indicates the timepoiint is relative to the 2nd previous timepoint by 14 days. A plus or minus sign can be entered but will be ignored as times are absolute.
`N1: 1 Day` is equivalent to `N: 1 Day` and indicates the timepoiint is relative to the next timepoint by 1 day.
`A:` is an anchor

##### Activity

The activity section consists of three columns, A to C, starting in row 10, row 9 being a title row. As many rows as needed can be added.

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | Parent Activity | Parent Activity. Not used currently | Set to '-' |
| B | Child Activity | Child activity name | Text string |
| C | BC/Procedure/Timeline | A set of BCs, procedures or timelines. Comma separated or the form detailed below | :--- |

The BC, procedure, timeline format is defined as follows (using pseudo BNF):

```
<entries> ::= <entry> | <entries> <entry>
<entry> ::= <type> : <name> | empty
<type> ::= PR | BC | TL
<name> ::= <name of item>
```

`BC: Age, BC: Sec, PR:Informed Consent Form, TL:Exercise` indicates the activity consists of the bcs Age and Sex, a procedure for the informed consent and a timeline specified in the Exercise sheet.

##### Link

The link section consists of a set of cells into which an upper case 'X' can be placed to link a timepoint with an activity. Otherwise the cell will be ignored. A '-' can be used to fill in cells but "empty".

### V2 Timeline sheets

#### Sheet Name

As defined within the study design sheet, see above.

#### Sheet Contents

##### General

This is a complicated sheet. It is, in essence, an enhanced SoA. There are several sections within the sheet:

- The name, description and condition located top right
- The remainder of the sheet is the SoA with:
  - The timing set in the top rows, the "timepoints"
  - The activities down the left hand side
  - The link between activities and "timepoints", the classic 'X'

##### Name, Description, Condition

The name description and condition are located in columns A and B, rows 1 and 2. It is a vertical name value pair configuration

| Row | Row Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| 1 | Name | The timeline name | Text string |
| 2 | Description | Timeline description | Text string |
| 3 | Condition | Timeline entry condition | Text string |

##### Timing

The timing seciton consists of multiple columns starting in column D. As many columns as needed can be created. A title block is held in Column C. The section consists of eight rows in rows 1 to 8 as follows:

| Row | Row Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| 1 | name | Identifier | Text string |
| 2 | description | Description | Text string, can be empty |
| 3 | label | Display label | Text string, can be empty |
| 4 | type | Timepoint type | `Activity` or `Decision` |
| 5 | default | Timepoint Link | The name (as per row 1) of the next activity in the sequence, the default connection |
| 6 | condition | Timepoint Links | The names (as per row 1) of the activities to link to for one or more conditions (command separated list) |
| 7 | epoch | Name of the epoch within which the timepoint falls | Text string  |
| 8 | encounter | Name of the encounter in which the timepoint belongs| Text string. Can be empty |

##### Activity

The activity section consists of three columns, A to C, starting in row 10, row 9 being a title row. As many rows as needed can be added.

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | Parent Activity | Parent Activity. Not used currently | Set to '-' |
| B | Child Activity | Child activity name | Text string |
| C | BC/Procedure/Timeline | A set of BCs, procedures or timelines. Comma separated or the form detailed below | :--- |

The BC, procedure, timeline format is defined as follows (using pseudo BNF):

```
<entries> ::= <entry> | <entries> <entry>
<entry> ::= <type> : <name> | empty
<type> ::= PR | BC | TL
<name> ::= <name of item>
```

`BC: Age, BC: Sec, PR:Informed Consent Form, TL:Exercise` indicates the activity consists of the bcs Age and Sex, a procedure for the informed consent and a timeline specified in the Exercise sheet.

##### Link

The link section consists of a set of cells into which an upper case 'X' can be placed to link a timepoint with an activity. Otherwise the cell will be ignored. 

### Study Design Timing sheet

#### Sheet Name

`studyDesignTiming`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing encounter definitions.

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | name	| Name | Text string |
| B | description | Description | Text string, can be empty |
| C | label | Display label | Text string, can be empty |
| D | type | The type of timing | Either `Before`, `After` or `Fixed` |
| E | from | Timeing point ref | The name of a timing point from a timeline sheet |
| E | to | Timeing point ref | The name of a timing point from a timeline sheet |
| E | timingValue | Timing | The relative value for a `Before`, `After` timing value or an absolute time for `Fixed` |
| E | toFrom | Timing precision | Either `S2S`, `S2E`, `E2S`, `E2E` to set the precise timing for a `Before`, `After` timing value |
| E | window | Timing window | A timing range |

### Study Design Activities sheet

#### Sheet Name

`studyDesignActivities`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing encounter definitions.

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | activityName or name	| Name | Text string |
| B | activityDescription or description| Description | Text string, can be empty |
| C (optional) | label | Display label | Text string, can be empty. Default value is '' |
| D | activityIsConditional | Conditional flag | Boolean |
| E | activityIsConditionalReason | Reason | Text string |

Note that this sheet is optional. If the sheet is not provided the activities will be created from those defined in the timeline sheets. These activities will have the name and description set to the name used in the timeline sheet and no condition will be set.

If the sheet is provided but there is no definition in the sheet for an activity referenced in a timeline sheet then the name and description will be set to the name used in the timeline sheet and no condition will be set.

### Study Design Indications Sheet
	
#### Sheet Name

`studyDesignIndications`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing an indication or intervention: 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | name | The name | Text string | 
| B | description | Description | Text string, can be empty |
| C | label | Display label | Text string, can be empty |
| D | codes | The set of indication or intervention codes | A set of external CT codes, comma separated |	


### Study Design Interventions Sheet
	
#### Sheet Name

`studyDesignInterventions`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing an intervention. Note that columns J through S can repeat for the same content in columns A to I. For additional administrations rows leave columns A to I blank.


| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | name | Name | Text string | 
| B | description | Description | Text string, can be empty |
| C | label | Display label | Text string, can be empty |
| D | codes | The set of intervention codes | A set of external CT codes, comma separated |	
| E | role | The role th eintervanetion plays |	A single M11 code |
| F | type | The intervention type | |
| G | pharmacologicalClass | The pharmalogical class | A single external CT code |
| H | productDesignation | The product designation| A single M11 code |
| I | minimumResponseDuration | The minimum response duration | |
| J | administrationName | Name | Text string | 
| K | administrationDescription | Description | Text string, can be empty |
| L | administrationLabel | Display label | Text string, can be empty |
| M | administrationRoute | Route of administration | CDISC code reference |
| N | administrationDose | Dose quantity | Quantity |
| O | administrationFrequency | Administration freqeunce | CDISC code reference |
| P | administrationDurationDescription | Description | Text string, can be empty |
| Q | administrationDurationWillVary | Duration will vary flag | Boolean |
| R | administrationDurationWillVaryReason | Duration will vary reason | Text string |
| S | administrationDurationQuantity| administration quantity | Quantity |


### Study Design Populations sheet

#### Sheet Name

`studyDesignPopulations`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2 containing population or sub-population definitions. Note that not every entry in columns E through I need to be filled in, just enough to define  either the whole population of the sub-populations. Sub-population need not be specificed.

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | level	| Level of entry | Set to either `MAIN` for the main population entry. All other values equate to a cohort (sub population) entry | 
| B | name	| Identifier | Text string | 
| C | description| Description | Text string, can be empty | 
| D | label | Display label | Text string, can be empty |
| E | plannedCompletionNumber	| Number of participants to complete the study | Integer | 
| F | plannedEnrollmentNumber	| Number of participants to be enrolled | Integer | 
| G | plannedAge	| Age range of participants | Range |
| H | plannedSexOfParticipants | Sex of participants | CDISC code reference |
| I | includesHealthSubjects | Healthy subjects flag | Boolean |

### Study Design Objectives and Endpoints sheet

#### Sheet Name

`studyDesignOE`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing objective and endpoint definitions. Note that columns D through G can repeat for the same content in columns A to C. For additional endpoint rows leave columns A to C blank.

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | objectiveXref	or objectiveName | Identifier | Text string |
| B | objectiveDescription	| Description | Text string, can be empty |
| C (optional) | objectiveLabel | Display label | Text string, can be empty. Default value is '' |
| D | objectiveText	| The objective | Templated text |
| E | objectiveLevel	| Objective level | CDISC code reference |
| F | objectiveDictionary| Dictionary cross reference | The dictionary from which the templated text tags are taken. If no tags are used can be empty |
| G | endpointXref or endpointName	| Identifier | Text string. Note columns G to M can repeat for each endpoiint for an objective |
| H | endpointDescription	| Description | Text string, can be empty |
| I (optional) | endpointLabel | Display label | Text string, can be empty. Default value is '' |
| J | endpointText	| The objective | Templated text |
| K | endpointPurpose	| | |
| L | endpointLevel | Level | CDISC code reference |
| M | endpointDictionary| Dictionary cross reference | The dictionary from which the templated text tags are taken. If no tags are used can be empty |

### Study Design Eligibility Criteria sheet

#### Sheet Name

`studyDesignEligibilityCriteria`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing eligibility definitions. 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | category | Category | Either `Inclusion` or `Exclusion` |
| B | identifier	| Identifier | Text string, the identifier for the criteria |
| C | name | The name identifier for the criteria | Text string |
| D | description	| Description | Text string, can be empty |
| E | label | Display label | Text string, can be empty |
| F | text	| Criteria text | Templated text |
| G | dictionary| Dictionary cross reference | The dictionary from which the templated text tags are taken. If no tags are used can be empty |

### Study Design Estimands sheet

#### Sheet Name

`studyDesignEstimands`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing estimand definitions. Note that column H can repeat for the same content in columns A through G.

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | xref or name	| Identifier | Text string |
| B | summaryMeasure	| The summary measure | Text string |
| C | populationDescription	| Description | Text string, can be empty |
| D (optional) | label | Display label | Text string, can be empty. Default value is '' |
| E | intercurrentEventName or name	| Name | Text string |
| F | intercurrentEventDescription or description| Description | Text string, can be empty |
| G | treatmentXref	| Treatment cross reference | Cross reference to a treatment |
| H | endpointXref	| Endpoint cross reference | Cross reference to an endpont |
| I | intercurrentEventstrategy| Strategy | Text string. This column can be repeated fo reach intercurrent event required for the Estimand |

### Study Design Procedures sheet

#### Sheet Name

`studyDesignProcedures`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing procedure definitions.

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | xref, procedureName or name	| Identifier | Text string |
| B | procedureDescription or description	| Type | Text string, can be empty |
| C (optional) | label | Display label | Text string, can be empty. Default value is '' |
| D | procedureType	| Type | Text string |
| E | procedureCode or code	| Code reference | External CT reference  |
| F | procedureIsConditional | Conditional flag | Boolean |
| G | procedureIsConditionalReason | Reason | Text string |

### Study Design Encounters sheet

#### Sheet Name

`studyDesignEncounters`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing encounter definitions.

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | xref	| Identifier | Text string |
| B | encounterName or name	| Name | Text string |
| C | encounterDescription or description	| Description | Text string, can be empty |
| D (optional) | label | Display label | Text string, can be empty. Default value is '' |
| E | encounterType or type	| The type | CDISC code reference |
| F | encounterEnvironmentalSetting	| Encounter environment | CDISC code reference |
| G | encounterContactModes	| Contact modes | CDISC code reference |
| H | transitionStartRule	| Start rule | Text string |
| I | transitionEndRule| End Rule | Text string |
| J | window | Timing reference that defines the window | Text string |

### Study Design Elements sheet

#### Sheet Name

`studyDesignElements`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing element definitions.

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | xref | Identifier | Text string |	
| B | studyElementName or name| Name | Text string |	
| C | studyElementDescription or description | Description | Text string, can be empty |	
| D (optional) | label | Display label | Text string, can be empty. Default value is '' |
| E | transitionStartRule | Start rule | Text string |	
| F | transitionEndRule | End rule | Text string |

### Study Design Content sheet

#### Sheet Name

`studyDesignContent`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing the narrative content: 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | sectionNumber | The section number | Text string with section numbers separated by '.' characters. Section numbers from row to row can only increase by a single level down, e.g. '1.2' to '1.2.1' and not '1.2.1.1'. The section numbers will be used to create parent child relationships in the data created. | 
| B | name | Name of the section. | Text string. Can be left blank in which case a default value will be used based on the section number |
| C | sectionTitle | The section title | Text String |
| D | sectionText | The section text | HTML formatted text String |


### Study Design Sites sheet

#### Sheet Name

`studyDesignSites`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing organizations and associated sites. Note that columns G through I can repeat for the same content in columns A to F. For additional site rows leave columns A to F blank.

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | name | Organization name | Text string |
| B | label | Organization display label | Text string, can be empty |
| C | type | Organisation type | CDISC code reference |
| D | identifierScheme | The scheme for the organisation identifier | Example would be 'DUNS' |
| E | identifier | Organisation identifier | Text string |
| F | address | Organisation address | Address |
| G | siteName | Site name | Formated using a pipe delimited form, see below |
| H | siteDescription | Site description | Text string, can be empty|
| I | siteLabel | Site display Label | Text string, can be empty |

### Dictionary Sheet

#### Sheet Name

`dictionaries`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2. Each row contains a dictionary and dictionary entry definitions. The sheet defines one or more dictionaries and the entries within each dictionary. Note that columns D through F can repeat for the same content in columns A to C. For additional dictionary entry rows leave columns A to C blank.

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | name | The dictionary name | Text string | 
| B | description | Description | Text string. Can be empty |	
| C | label | Label | Text string. Can be empty |	
| D | key | The entry key | Text String. Must be unique within the dictionary |
| E | class | The class name | The name of the class within the model from which the data for the dictionary entry is to be taken |
| F | xref | Cross reference name | The name of the instance from which the data is to be taken. Use the entries in the name columns from other sheets |
| F | atrribute | The attribute name | The name of the attribute from which the data is to be taken. |

### Configuration Sheet

#### Sheet Name

`configuration`

#### Sheet Contents

A set of rows consisting of configuration parameters. The first column is the type of configuration parameter while the second is the value. The values for specific parameters may vary in their format

| Parameter | Description | Format and Values |
| :--- | :--- | :--- |
| CT Version | Allows for the version of a specific external CT to be set. Multiple rows can be included to set the versions for several CTs | Of the form CT name = Version value, For example `SNOMED = 21st June 2012`|
| Empty None | Allows for string fields to be set to '' rather than null/none values so as to accomodate the SDR validation checks | Set to 'EMPTY' to use ''. Any other value will permit  null values to be used |
| SDR Prev Next | Deprecated | Deprecated |
| SDR Root | Deprecated | Deprecated |
| SDR Description | Deprecated | Deprecated |

# Issues

See the [github issues](https://github.com/data4knowledge/usdm/issues)

# Build Notes

Build with `python3 -m build --sdist --wheel`

Upload to pypi using `twine upload dist/* `