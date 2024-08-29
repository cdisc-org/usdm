from usdm_model.organization import Organization
from usdm_excel.base_sheet import BaseSheet

def get_organization(parent: BaseSheet, index: int) -> Organization:
  organization = None
  org_type = parent.read_cdisc_klass_attribute_cell_by_name('Organization', 'organizationType', index, ['organisationType', 'organizationType', 'type'])     
  org_id_scheme = parent.read_cell_by_name(index, ['organisationIdentifierScheme', 'organizationIdentifierScheme', 'identifierScheme'])
  org_identifier = parent.read_cell_by_name(index, ['organisationIdentifier', 'organizationIdentifier'])
  org_name = parent.read_cell_by_name(index, ['organisationName', 'organizationName', 'name'])
  org_label = parent.read_cell_by_name(index, 'label', default="", must_be_present=False)
  org_address = parent.read_address_cell_by_name(index, ['organisationAddress', 'organizationAddress', 'address'])
  if org_address:
    parent.globals.cross_references.add(org_address.id, org_address)   
  organization = parent.create_object(Organization, {'identifierScheme': org_id_scheme, 'identifier': org_identifier, 'name': org_name, 'label': org_label, 'organizationType': org_type, 'legalAddress': org_address})
  if organization:
    parent.globals.cross_references.add(organization.id, organization)   
  return organization
