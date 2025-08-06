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

See a simple example test program [here](https://github.com/data4knowledge/usdm_data/blob/main/test_simple.py)

## Format of Workbook

### Examples

Example workbooks can be found in the [test file directory](https://github.com/cdisc-org/usdm/tree/main/tests/integration_test_files).

### Sheets

The workbook consists of several sheets each with a dedicated purpose. All sheets must be present except for those marked optional.

- Study sheet
- Organisations sheet
- Study Identifiers sheet
- Study References sheet
- Study Amendments sheet
- Study Amendments Changes sheet
- Study Amenedment Impact sheet
- Study Design sheet
- Study Design Arms sheet
- Study Design Epochs sheet
- One or more Timeline sheets
- Study Design Timing sheet
- Study Design Activities sheet (optional)
- Study Design Indications sheet
- Study Design Interventions sheet
- Study Products Sheet
- Study Devices Sheet
- Study Product Organization Roles Sheet
- Study Design Populations sheet
- Study Design Characteristcis sheet
- Study Design Objectives and Endpoints sheet
- Study Design Eligibility Criteria sheet
- Study Design Estimands sheet
- Study Design Procedures sheet
- Study Design Encounters sheet
- Study Design Elements sheet
- One or more Document Template sheets
- Document Content sheet
- Study Design Sites sheet (optional)
- Notes Sheet (optional)
- Abbreviations Sheet (optional)
- People Sheet (optional)
- Roles Sheet (optional)
- Study Design Conditions sheet (optional)
- Dictionaries Sheet
- Configuration sheet

The content of each sheet is described below. A graphical representation of the sheets can be found [here](https://github.com/cdisc-org/usdm/blob/main/docs/sheets.png)

### CDISC Terminology

For those cells where CDISC codes are used the user can enter either the CDISC C Code, for example `C15602`, the CDISC submission value, for example `PHASE III TRIAL`, or the preferred term, for example `Phase III Trial`

### Multiple Values

Some cells allow for multiple values. These are all comma separated. If users wish to include a comma within such strings then the string can be enclosed in quotes. For example `123, "123,456", 789`.

### External Terminology

For those cells where external CT is referenced the user can enter code in the form `<code system>: <code> = <decode>`. For example `SPONSOR: A = decode 1, SPONSOR: B = decode 2`. Where multiple codes are needed then the values are separated by commas.

### Boolean Values

For boolean fields the following can be used to indicate a `true` value `'Y', 'YES', 'T', 'TRUE', '1'` or the lower case equivalents.

### Address Values

An address is of the form: ```<lines>,district,city,state,postal_code,<country code>```. All fields are text strings but note that:

- `<lines>`: one or more comma separated strings. As many as needed can be included.
- `<country code>`: `<country code>` is either a two or three character ISO-3166 country code. 

Examples

- ```line 1, line 2, A District, A City, A State, 12345, USA```, two lines before the district
- ```line 1, A District, A City, A State, 12345, USA```, single line before the district
- ```"14, X Street", A District, A City, A State, 12345, USA```, note the commas to allow a comma to be included
- ```14, X Street| A District| A City| A State| 12345| USA```, using pipe separators, no need for quotes around the first line

Note that `|` can be used in place of the commas for backward compatibility.

### Person Name Values

A name is of the form: ```<prefixes>,<first names>,family name,<suffixes>```. All fields are text strings but note that:

- `<prefixes>`: one or more space separated strings. As many as needed can be included.
- `<first names>` one or more comma separated first names 
- `<suffixes>` one or more space separated strings. As many as needed can be included.

Examples

- ```Mr, Fred, Smith, BSc```, Single prefix, first name, family name and suffic
- ```Mr, Fred, John, Smith,```, No suffix, two first names
- ```", Fred, Smith,```, Just a first and family name

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

Some entries can include "tags" that allow the text to reference structured content from elsewhere in the model. An example is an eligibility criterion referring to population definitions or an activity name. These sections of text are formatted as `<usdm:tag name="...tag_name..."/>` within the text. The `...tag_name...` refers to an entry within a dictionary (see the dictionaries sheet)

An example of Templated Text is `Subjects shall be between <usdm:tag name="min_age"/> and <usdm:tag name="max_age"/>` where the min and max ages will be inserted using the dictionary entries that refer to particular attribute values from within the structured parts of the model.

### Geographic Scopes & Enrollment

Geographic Scopes appear in a few of the sheets. These take the form `Global`, `Region: <region>` or , `Country: <country>`. Regions and Countries are taken from the ISO3166 value set. Examples are `Global` or `Region: Europe, Country: USA`. Where multiple codes are needed then the values are separated by commas. Note, if a global entry is specified then no other values are required and will be ignored. 

In some cases (subject recruitment) values are associated with the scopes. The enrollment data is of the form: `Global: <enrollment>`, `Region: <region>=<enrollment>` or , `Country: <country>=<enrollment>`. The enrollment is either a percentage or an absolute value. Regions and Countries are taken from the ISO3166 value set. Examples are `Global: 65%` or `Region: Europe=15, Country: USA=20%`. Where multiple codes are needed then the values are separated by commas. Note, if a global entry is specified then no other values are required and will be ignored.

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

| Key Word | Purpose | Format and Values |
| :--- | :--- | :--- |
| studyVersion | String version | Text string |
| studyAcronym | The study acronym | Text string |
| studyRationale | the study rationale | Text string |
| businessTherapeuticAreas | The set of business therapuetic area codes | External CT code format. Likely filled with sponsor terms |
| briefTitle | The brief title | Text string | 
| officialTitle	| The officiall title | Text string| 
| publicTitle | The public title | Text string| 
| scientificTitle | The scientific title | Text string| 
| protocolVersion | The version of the protocol | Text string | 
| protocolStatus | The status | CDISC code reference | 

A header row in row 16 followed by repeating rows from row 17, containing a series of dates: 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | category | The date category | Either `study_version` or `protocol_document` for a date that applies to the study version or the document | 
| B | name | A name for the date | text string | 
| C | description	| A date description | Text string, can be blank | 
| D | label	| A date label | Text string| 
| E | type | the type of date | CDISC code reference | 
| F | date| The date | Date field, dd/mm/yyyy | 
| H | scopes | The geographic scopes for the date | Geographic scope |


### Study Organizations	Sheet
	
#### Sheet Name

`studyOrganizations`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, each containing a study identifier: 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | identifierScheme | The scheme for the organisation identifier. | Example would be 'DUNS' |
| B | identifier | Organisation identifier | Text string |
| C | name | Organisation name | Text string |
| D | label | Display label | Text string, can be empty. Default value is '' |
| E | type, organizationType or type | Organisation type | CDISC code reference |
| F | address | The organisation address | Address |

### Study Identifiers Sheet
	
#### Sheet Name

`studyIdentifiers`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, each containing a study identifier: 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | identifier | The identifier for the study | Text string |
| B | organization | The organisation name as per the studyOrganizations sheet | Text string |

### Study References Sheet
	
#### Sheet Name

`studyReferences`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, each containing a study reference identifier: 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | identifier | The identifier for the study | Text string |
| B | organization | The organisation name as per the studyOrganizations sheet | Text string |
| C | type | The type of identifier | CDISC code reference |

### Study Amendments	Sheet
	
#### Sheet Name

`studyAmendments`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing a study amendment: 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | name | Name of the change | Text string |
| B | description | Description for the change | Text string |
| C | label | Change label. Default value is '' | Text string |
| D | number | The amendment number | Integer |
| E | summary | The amendment summary | Text string |
| F | substantialImpact | True or false value  indicating if the amendment is substantial | Boolean |
| G | primaryReason | Primary reason for the amendment | CDISC code reference |
| H | secondaryReasons | Secondary reasons for amendment. Multiple values can be supplied separated by a comma | CDISC code reference |
| I | enrollment | The current state of subject enrollment, either global, regional or country | Geographic scope with enrollment |
| J (optional) | template | The name of the template for the document to which the amendment applies. Defaults to 'SPONSOR'. See configuration sheet for template names | Text string. |

### Study Amendments Changes Sheet
	
#### Sheet Name

`amendmentChanges`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing a study amendment changes: 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | amendment | The amendment to which the change belongs, references the main amendment sheet | Integer |
| B | name | Name of the change | Text string |
| C | description | Description for the change | Text string |
| D | label | Change label. Default value is '' | Text string |
| E | rationale | The rationale for the change | Text string |
| F | summary | Summary of the change | Text string |
| G | sections | Section references | Comma separated text string consisting of `<section number>: <description of change>` |

### Study Amendments Impact Sheet
	
#### Sheet Name

`amendmentImpact`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing a study amendment impacts: 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | amendment | The amendment to which the change belongs, references the main amendment sheet | Integer |
| B | text | Text describing the impact of the amendment | Test string |
| C | substantial | Indicates the change is substantial | Boolean |
| D | type | The type of impact | CDISC code referernce |
    
### Study Design sheet

#### Sheet Name

`studyDesign`

#### Sheet Contents

The study design sheet consists of two parts, the upper section for those single values and then a section for the arms and epochs.

For the single values, the keyword is in column A while the value is in column B.

| Key Word | Purpose | Format and Values |
| :--- | :--- | :--- |
| studyDesignName or name | Study design name | Text string |
| studyDesignDescription or description | Study design description | Text string |
| label | Study design label. Default value is '' | Text string |
| studyType | The study type. This is where Interventional / Observation selection is made | CDISC code reference |
| studyPhase | The study phase | CDISC code reference |
| therapeuticAreas | Set of therapeutic area codes | Set of external CT references, comma separated |
| studyDesignRationale | Study design rationale | Text string |
| studyDesignBlindingScheme | Code for the blinding scheme | CDISC code reference |
| trialIntentTypes | Codes for the trial intent types | Comma separated CDISC code references |
| trialTypes | Code for the trial type | CDISC code reference|
| interventionModel | | CDISC code reference |
| characteristics | Set of characteristics | Set of CDISC code references |
| timePerspective | Observation study time perspective | CDISC code reference |
| samplingMethod | Sampling method | CDISC code reference |
| mainTimeline | Name of main timeline sheet | This must be present |
| otherTimelines | Names of other timeline sheets | Commma separated list of sheet names. Can be empty |

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
| G (optional) | notes | Any relevant notes | List of note references, comma separated |


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
| E (optional) | notes | Any relevant notes | List of note references, comma separated |

### V1 Timeline sheets

No longer supported

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
| 4 | duration | Timeline duration quantity | Quantity |
| 5 | durationWillVary | Reason timeline will vary | Text string |
| 6 | durationDescription | Timeline duration description | Text string |

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

The activity section consists of three columns, A to C, starting in row 10, row 9 being a title row. As many rows as needed can be added. Note that only one of parent or child activity should be entered on any given row.

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | Parent Activity | Parent Activity. | Text string |
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
| D (optional) | notes | Any relevant notes | List of note references, comma separated |

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
| D | isRareDisease | Rare disease flag | Boolean |	
| E | codes | The set of indication or intervention codes | A set of external CT codes, comma separated |	

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
| G | product | The product | the name of the product |
| H | minimumResponseDuration | The minimum response duration | |
| I | administrationName | Name | Text string | 
| J | administrationDescription | Description | Text string, can be empty |
| K | administrationLabel | Display label | Text string, can be empty |
| L | administrationRoute | Route of administration | CDISC code reference |
| M | administrationDose | Dose quantity | Quantity |
| N | administrationFrequency | Administration freqeunce | CDISC code reference |
| O | administrationDurationDescription | Description | Text string, can be empty |
| P | administrationDurationWillVary | Duration will vary flag | Boolean |
| Q | administrationDurationWillVaryReason | Duration will vary reason | Text string |
| R | administrationDurationQuantity| administration quantity | Quantity |

### Study Design Products Sheet
	
#### Sheet Name

`studyDesignProducts`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | name | Name | Text string |
| B | description | Description | Text string, can be empty |
| C | label | Display label | Text string, can be empty |
| D | administrableDoseForm | Administrable dose form | CDISC code reference |
| E | productDesignation | Product designation | CDISC code reference |
| F | productSourcing | Product sourcing | CDISC code reference |
| G | ingredientRole | Ingredient role | CDISC code reference |
| H | substanceName | Substance name | Text string |
| I | substanceDescription | Substance description | Text string, can be empty |
| J | substanceLabel | Substance label | Text string, can be empty |
| K | substanceCode | Substance code | Text string, can be empty |
| L | strengthName | Strength name | Text string |
| M | strengthDescription | Strength description | Text string, can be empty |
| N | strengthLabel | Strength label | Text string, can be empty |
| O | strengthNumerator | Strength numerator | Text string |
| P | strengthDenominator | Strength denominator | Text string |
| Q | referenceSubstanceName | Reference substance name | Text string |
| R | referenceSubstanceDescription | Reference substance description | Text string, can be empty |
| S | referenceSubstanceLabel | Reference substance label | Text string, can be empty |
| T | referenceSubstanceCode | Reference substance code | Text string, can be empty |
| U | referenceSubstanceStrengthName | Reference substance strength name | Text string |
| V | referenceSubstanceStrengthDescription | Reference substance strength description | Text string, can be empty |
| W | referenceSubstanceStrengthLabel | Reference substance strength label | Text string, can be empty |
| X | referenceSubstanceStrengthNumerator | Reference substance strength numerator | Text string |
| Y | referenceSubstanceStrengthDenominator | Reference substance strength denominator | Text string |

### Study Devices Sheet
	
#### Sheet Name

`studyDevices`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | name | Name | Text string |
| B | description | Description | Text string, can be empty |
| C | label | Display label | Text string, can be empty |
| D | hardwareVersion | Hardware version | Text string |
| E | softwareVersion | Software version | Text string |
| F | sourcing | Sourcing | CDISC code reference |
| G | product | Product | Text string |
| H | notes | Notes | List of note references, comma separated |

### Study Product Organization Roles Sheet
	
#### Sheet Name

`studyProductOrganizationRoles`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | name | Name | Text string |
| B | description | Description | Text string, can be empty |
| C | label | Display label | Text string, can be empty |
| D | organizationId | Organization ID | Cross reference to an organization |
| E | code | Code | CDISC code reference |
| F | appliesToIds | Applies to IDs | List of cross references to a product, either interventions or devices |

### Study Design Populations sheet

#### Sheet Name

`studyDesignPopulations`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2 containing population or sub-population definitions. Note that not every entry in columns E through I need to be filled in, just enough to define  either the whole population of the sub-populations. Sub-populations need not be specificed.

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
| I | characterisitcs | List of characteristics for the cohort (ignored for main population) | Comma separated list of charcateristics name references |
| J | indications | List of indications for the cohort (ignored for main population) | Comma separated list of indications name references |

### Study Design Characteristics sheet

#### Sheet Name

`studyDesignCharacteristics`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2 containing characteristics for cohorts.

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | name	| Identifier | Text string | 
| B | description| Description | Text string, can be empty | 
| C | label | Display label | Text string, can be empty |
| D | text	| Criteria text | Templated text |
| E | dictionary| Dictionary cross reference | The dictionary from which the templated text tags are taken. If no tags are used can be empty |

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

A header row in row 1 followed by repeating rows from row 2, containing estimand definitions. Note that column I and J can repeat for the same content in columns A through H.

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | xref or name | Identifier | Text string |
| B | summaryMeasure	| The summary measure | Text string |
| C | populationDescription	| Description | Text string, can be empty |
| D | populationSubset | Name of the related population | Text string |
| E | intercurrentEventName or name	| Name | Text string |
| F | intercurrentEventDescription or description| Description | Text string, can be empty |
| G | treatmentXref	| Treatment cross reference | Cross reference to a treatment |
| H | endpointXref| Endpoint cross reference | Cross reference to an endpont |
| I | intercurrentEventStrategy| The strategy for the event | Text string. |
| J | intercurrentEventText| The text for the event | Text string. |

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
| F | encounterEnvironmentalSetting	| Encounter environment | One or more CDISC code references |
| G | encounterContactModes	| Contact modes | One or more CDISC code references |
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

### Document Template Sheets

#### Sheet Name

default name: `document`

Several content sheets can be included within the workbook and named as desired. Typical use might be the inclusion of a sponsor protocol format and the new M11 format

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing the narrative content: 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | name | Name of the section. | Text string. Can be left blank in which case a default value will be used based on the section number |
| B | sectionNumber | The section number | Text string with section numbers separated by '.' characters. Section numbers from row to row can only increase by a single level down, e.g. '1.2' to '1.2.1' and not '1.2.1.1'. The section numbers will be used to create parent child relationships in the data created. | 
| C | displaySectionNumber | Display Section Number | Boolean value indicating if the section number should be displayed within the document | 
| D | sectionTitle | Section Title | Text String |
| E | displaySectionTitle | Display Section Title | Boolean value indicating if the section title should be displayed within the document | 
| F | content | The content reference | The name of item include |

### Document Content sheet

#### Sheet Name

default name: `documentContent`

Several content sheets can be included within the workbook and named as desired. Typical use might be the inclusion of a sponsor protocol format and the new M11 format

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing the narrative content: 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | name | Name of the content | Text string. Can be left blank in which case a default value will be used based on the section number |
| B | text | The content text | HTML formatted text String |

There are some prefined macros that can be used to generate content. These are pre processed when the content sheet is read and transated into the appropriate USDM references ```usdm:ref``` or ```usdm:tag```. These macros use a similar syntax to the USDM references: 

```<usdm:macro id="macro name" attrib1="data1" attrib2="data2" .../>```

| Macro Name | Purpose | Attributes |
| :--- | :--- | :--- |
| xref | Refer to a data element by name reference | 'klass', 'name' and 'attribute'. The name is the name used within the workbook to define the content. |
| image | Insert an mage into the document | 'file' and 'type'. The file attribute specifies the name of a file in the same directory as the Excel workbook. |
| element | Refer to a predefined element | 'name' of the element. Supported element names are 'study_phase', 'study_short_title', 'study_full_title', 'study_acronym', 'study_rationale', 'study_version_identifier', 'study_identifier', 'study_regulatory_identifiers', 'study_date', 'approval_date', 'organization_name_and_address', 'amendment' and 'amendment_scope' |
| section | Add a pre defined section into the document | 'name' and 'template'. Supported section are 'title_page', 'inclusion', 'exclusion' and 'objective_endpoints'. Supported templates are 'm11' and 'plain' |
| bc | Add in a reference to a BC | 'name' and 'activity' where the name is the name of the BC as used in the SoA and activity is the name of the activity it is referenced from (in case several activities reference the same BC). This macro is needed as the BCs are not explicitly defined and thus named, they are read from the CDISC library and can appear multiple times. |
| note | Insert a note into the document | 'text' |
| abbreviation | Insert one or more abbreviations into the document | 'items', 'separator'. The items is a list of abbreviations to be inserted, comma separated. The separator is the character used to separate the items when displayed, default is a comma. |

Examples of macros are:

```<usdm:macro id="xref" klass="Objective" name="OBJ1" attribute="text"/>```

```<usdm:macro id="xref" klass="StudyDesignPopulation" name="STUDY_POP" attribute="@plannedCompletionNumber/Range/maxValue"/>```

```<usdm:macro id="element" name="study_identifier"/>```

```<usdm:macro id="image" file="design.png" type="png"/>```

```<usdm:macro id="section" name="inclusion" template="plain"/>```

```<usdm:macro id="bc" name="Body temperature" activity="Vital signs / Temperature">```

```<usdm:macro id="note" text="A note here please"/>```

```<usdm:macro id="abbreviations" items="AD, ECG" separator=";"/>```

### Study Design Sites sheet

#### Sheet Name

`studyDesignSites`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing organizations and associated sites. Note that columns G through I can repeat for the same content in columns A to F. For additional site rows leave columns A to F blank.

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | name | Site name | Formated using a pipe delimited form, see below |
| B | description | Site description | Text string, can be empty|
| C | label | Site display Label | Text string, can be empty |
| D | country | Country the site is in | CDISC code reference |
| E | organization | Organization name | Text string |

### Study Design Conditions sheet

#### Sheet Name

`studyDesignConditions`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2, containing the conditions: 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | name | Condition name | Text string |
| B | label | Condition display label | Text string, can be empty |
| C | description | Condition description | CDISC code reference |
| D | text | The condition text | Text string |
| E | appliesTo | List of cross references for items to which the condition applies | Comma separated list |
| F | context | List of cross references for the context in which the condition applies | Comma separated list |

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
| G | atrribute | The attribute path or name | The name or path of the attribute from which the data is to be taken |
| H (optonal) | value | The value | A fixed value. If this column is used then the 'class', 'xref' and 'attribute' fields should be empty |

The attribute path follows a simplified 'Xpath' syntax of ```@attribute-name[/class/@attribute-name]``` form. The class attribute pairs can be repeated to arrive as the desired attribute. This has been provided since not all instances of all classes are named which prevents thenm being addressed directly, for example Range of Quantity instances.

An example for accessing the Population planned age, max value is ```@plannedAge/Range/@maxValue/Quantity/@value```. In this instance the ```class``` column would be set to ```Population``` and the ```xref``` column set to the name of the Population entry in the population shseet. 

Note that the '@' symbol does not need to be included with attribute names but it guides the eye making it easier to read the path.

### Notes Sheet

#### Sheet Name

`notes`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2. Each row contains a note. 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | name | The note name | Text string | 
| B | text | The note text | Text string. |	
| C | codes | The set of codes | A set of external CT codes, comma separated |	

### Abbreviations Sheet

#### Sheet Name

`abbreviations`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2. Each row contains a note. 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | abbreviatedText | The abbreviation | Text string | 
| B | expandedText | The full text | Text string. |	
| C (optional) | notes | Any relevant notes | List of note references, comma separated |

### People Sheet

#### Sheet Name

`people`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2. Each row contains an assigned person definition. 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | name | The dictionary name | Text string | 
| B | description | Description | Text string. Can be empty |	
| C | label | Label | Text string. Can be empty |	
| D | jobTitle | The job title | Text string | 
| E | organization | Cross reference (name) to an organization to which the person is associated | Text string. |	
| F | personName | The persons names | Name string. |	


### Roles Sheet

#### Sheet Name

`roles`

#### Sheet Contents

A header row in row 1 followed by repeating rows from row 2. Each row contains an assigned person definition. 

| Column | Column Name | Purpose | Format and Values |
| :--- | :--- | :--- | :--- |
| A | name | The dictionary name | Text string | 
| B | description | Description | Text string. Can be empty |	
| C | label | Label | Text string. Can be empty |	
| D | people | Cross reference (name) to one or more persons performing the role | Comma separated list of strings. Can be empty. | 
| E | masking | The masking associated with the role. Can be empty if no masking. | Text string. Can be empty |	
| F | role | The role | CDISC code reference | 
| G | organizations | Cross reference (name) to one or more organizations performing the role | Comma separated list of strings. Can be empty. |
| H (optional) | notes | Any relevant notes | List of note references, comma separated |


### Configuration Sheet

#### Sheet Name

`configuration`

#### Sheet Contents

A set of rows consisting of configuration parameters. The first column is the type of configuration parameter while the second is the value. The values for specific parameters may vary in their format

| Parameter | Description | Format and Values |
| :--- | :--- | :--- |
| CT Version | Allows for the version of a specific external CT to be set. Multiple rows can be included to set the versions for several CTs | Of the form ctName = Version, for example `SNOMED = 21st June 2012`|
| Empty None | Allows for string fields to be set to '' rather than null/none values so as to accomodate the SDR validation checks | Set to 'EMPTY' to use ''. Any other value will permit  null values to be used |
| Template | Configures a protocol template and the associated template sheet | Entries take the form of templateName = sheetName, for example `Sponsor = sponsorContent`. The template name and the sheet name are simple strings. Template names are at the user's discretion but the string `m11` or `M11` is reserved as the template name for the M11 Template format. The sheet name must match a sheet within the workbook that must be structured as per the template sheet format. |
| Use Template | Deprecated | Deprecated |
| USDM Version | Deprecated | Deprecated |
| SDR Prev Next | Deprecated | Deprecated |
| SDR Root | Deprecated | Deprecated |
| SDR Description | Deprecated | Deprecated |

An example configuration is

| First Column | Second Column |
| :--- | :--- | 
| CT Version | SNOMED=January 31, 2018 |
| CT Version | SPONSOR =   12 |
| CT Version | ICD-10=1 |
| Template | lilly=lillyFormat |
| Template | m11=m11Format |

This sets up three CT versions and two templates.

# Issues

See the [github issues](https://github.com/data4knowledge/usdm/issues)

# Build Notes

## Checklist

1. Everything on main branch?
1. Readme updated with any necessary changes?
1. Version updated?
1. All tests passing?

Then

1. Build and upload
1. Write release note

## Build steps for deployment to pypi.org

- Build with `python3 -m build --sdist --wheel`
- Upload to pypi.org using `twine upload dist/* `