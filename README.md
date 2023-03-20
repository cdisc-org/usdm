# CDISC / Transcelerate Unified Study Definitions Model

## 

## Format of Workbook

### General

The workbook consists of several sheets each with a dedicated purpose.

- Study sheet
- Study Identifiers sheet
- Study Design Indications and Interventions sheet

### CDISC Terminology


### Study Sheet

| Column Name | Content | Format |
| --- | --- | --- |
| studyTitle | The study title | Simple text string |
| studyVersion | String version | Simple text string |
| studyType | CDISC code | String in the form `<C code>=<decode (preferred term)>` |
| studyPhase | CDISC code | String in the form `<C code>=<decode (preferred term)>` |
	
### Study Identifiers	Sheet
	
organisationIdentifierScheme	The scheme for the organisation identifier. Example would be 'DUNS'
organisationIdentifier	Organisation identifier, a string
organisationName	String name
organisationType	Set to either 'registry', 'sponsor' or 'regulatory'
studyIdentifier	String identifier
organisationAddress	"The orgnaisation address formated using a pipe delimited form:

line|city|district|state|postal_code|<country code>

All fields are free text except for <country code>. <country code> is either a two caracter or three character ISO-3166 country code.
	
### indications_interventions sheet
	
| Column Name | Content | Format |
| --- | --- | --- |
| type | The type, either IND for indication or INT for intervention ||
| description | A free text description for the indication or intervvention ||
| codes | A set of codes, comma separated | Each code is of the form `<code system>: <code> = <decode>`. For example `SNOMED: 12345678 = decode, ICD-10: code = decode` |	
	
	