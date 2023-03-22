# CDISC / Transcelerate Unified Study Definitions Model

## 

## Format of Workbook

### General

The workbook consists of several sheets each with a dedicated purpose.

- Study sheet
- Study Identifiers sheet
- Study Design Indications and Interventions sheet

### CDISC Terminology

For those cells containing definition where CDISC codes are used the user can enter either the CDISC C Code, for example `C15602`, the CDISC submission value, for example `PHASE III TRIAL`, or the preferred term, for example `Phase III Trial`

### Study Sheet

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
	
| Column Name | Description | Format and Values |
| :--- | :--- | :--- |
| organisationIdentifierScheme | The scheme for the organisation identifier.  | Example would be 'DUNS' |
| organisationIdentifier | Organisation identifier | A text string |
| organisationName | Organisation name | A text string |
| organisationType | Organisation type | Set to either `registry`, `sponsor` or `regulatory` |
| studyIdentifier | The identifier for the study | A text string |
| organisationAddress | The organisation address | Formated using a pipe delimited - allows for commas in items within the address - form, i.e. `line|city|district|state|postal_code|<country code>`. All fields are free text except for `<country code>`. `<country code>` is either a two or three character ISO-3166 country code. |
	
### Study Design Indications and Interventions Sheet
	
| Column Name | Description | Format and Values |
| :--- | :--- | :--- |
| type | The type, either IND for indication or INT for intervention ||
| description | A free text description for the indication or intervvention ||
| codes | A set of codes, comma separated | Each code is of the form `<code system>: <code> = <decode>`. For example `SNOMED: 12345678 = decode, ICD-10: code = decode` |	
	
### Configuration Sheet

A set of rows consisting of configuration parameters. The first column is the type of configuration parameter while the second is the value. The values for specific parameters may vary in their format

| Parameter | Description | Format and Values |
| :--- | :--- | :--- |
| CT Version | Allows for the version of a specific external CT to be set. Multiple rows can be included to set the versions for several CTs | Of the form CT name = Version value, For example `SNOMED = 21st June 2012`|

