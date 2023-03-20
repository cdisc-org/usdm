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

| Column Name | Description | Format and Values |
| :--- | :--- | :--- |
| studyTitle | The study title | Simple text string |
| studyVersion | String version | Simple text string |
| studyType | CDISC code | String. Either the C Code, the submission value or the preferred term for the term desired. |
| studyPhase | CDISC code | String. Either the C Code, the submission value or the preferred term for the term desired.  |
	
### Study Identifiers	Sheet
	
| Column Name | Description | Format and Values |
| :--- | :--- | :--- |
| organisationIdentifierScheme | The scheme for the organisation identifier.  | Example would be 'DUNS' |
| organisationIdentifier | Organisation identifier | A text string |
| organisationName | Organisation name | A text string |
| organisationType | Organisation type | Set to either `registry`, `sponsor` or `regulatory` |
| studyIdentifier | The identifier for the study | A text string |
| organisationAddress | The organisation address | Formated using a pipe delimited form `line|city|district|state|postal_code|<country code>`. All fields are free text except for `<country code>`. `<country code>` is either a two caracter or three character ISO-3166 country code. |
	
### Study Design Indications and Interventions Sheet
	
| Column Name | Description | Format and Values |
| :--- | :--- | :--- |
| type | The type, either IND for indication or INT for intervention ||
| description | A free text description for the indication or intervvention ||
| codes | A set of codes, comma separated | Each code is of the form `<code system>: <code> = <decode>`. For example `SNOMED: 12345678 = decode, ICD-10: code = decode` |	
	
	