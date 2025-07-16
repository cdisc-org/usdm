from usdm_excel.duplicate_object import duplicate_object
from usdm_model.code import Code
from usdm_model.alias_code import AliasCode
from usdm_model.geographic_scope import GeographicScope


def test_one_level(globals):
    globals.id_manager.clear()
    source = Code(
        id="Code_N",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label",
    )
    result: Code = duplicate_object(source, globals)
    assert result.model_dump() == {
        "id": "Code_1",
        "code": "code",
        "codeSystem": "codesys",
        "codeSystemVersion": "3",
        "decode": "label",
        "extensionAttributes": [],
        "instanceType": "Code",
    }


def test_two_levels(globals):
    globals.id_manager.clear()
    code = Code(
        id="Code_N",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label",
    )
    alias_code = AliasCode(
        id="Code_M",
        standardCode=code,
    )
    result: AliasCode = duplicate_object(alias_code, globals)
    assert result.model_dump() == {
        "id": "AliasCode_1",
        "instanceType": "AliasCode",
        "standardCode": {
            "code": "code",
            "codeSystem": "codesys",
            "codeSystemVersion": "3",
            "decode": "label",
            "extensionAttributes": [],
            "id": "Code_1",
            "instanceType": "Code",
        },
        "standardCodeAliases": [],
        "extensionAttributes": [],
    }


def test_three_levels(globals):
    globals.id_manager.clear()
    code = Code(
        id="Code_N",
        code="code",
        codeSystem="codesys",
        codeSystemVersion="3",
        decode="label",
    )
    alias_code = AliasCode(
        id="Code_M",
        standardCode=code,
    )
    geo_scope = GeographicScope(
        id="Code_O",
        type=code,
        code=alias_code,
    )
    result: GeographicScope = duplicate_object(geo_scope, globals)
    assert result.model_dump() == {
        "id": "GeographicScope_1",
        "type": {
            "code": "code",
            "codeSystem": "codesys",
            "codeSystemVersion": "3",
            "decode": "label",
            "extensionAttributes": [],
            "id": "Code_1",
            "instanceType": "Code",
        },
        "code": {
            "id": "AliasCode_1",
            "instanceType": "AliasCode",
            "standardCode": {
                "code": "code",
                "codeSystem": "codesys",
                "codeSystemVersion": "3",
                "decode": "label",
                "extensionAttributes": [],
                "id": "Code_2",
                "instanceType": "Code",
            },
            "standardCodeAliases": [],
            "extensionAttributes": [],
        },
        "extensionAttributes": [],
        "instanceType": "GeographicScope",
    }
