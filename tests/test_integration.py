import json
import csv
import yaml
from usdm_db import USDMDb
from bs4 import BeautifulSoup
from uuid import UUID

SAVE_ALL = False


def save_error_csv(file, contents):
    writer = csv.DictWriter(
        file, fieldnames=["sheet", "row", "column", "message", "level"]
    )
    writer.writeheader()
    writer.writerows(contents)


def to_int(value):
    try:
        return int(value)
    except:
        return None


def read_error_csv(file):
    reader = csv.DictReader(file)
    items = list(reader)
    for item in items:
        item["row"] = to_int(item["row"])
        item["column"] = to_int(item["column"])
    return items


def prep_errors_for_csv_compare(errors):
    for error in errors:
        error["sheet"] = error["sheet"] if error["sheet"] else ""
    return errors


def format_html(result):
    soup = BeautifulSoup(result, "html.parser")
    return soup.prettify()


def run_test(filename, save=False):
    usdm = USDMDb()
    errors = usdm.from_excel(f"tests/integration_test_files/{filename}.xlsx")
    result = usdm.to_json()
    # errors = excel.errors()

    # Useful if you want to see the results.
    if save or SAVE_ALL:
        with open(
            f"tests/integration_test_files/{filename}.json", "w", encoding="utf-8"
        ) as f:
            f.write(json.dumps(json.loads(result), indent=2))
        with open(
            f"tests/integration_test_files/{filename}_errors.csv", "w", newline=""
        ) as f:
            save_error_csv(f, errors)

    with open(f"tests/integration_test_files/{filename}.json", "r") as f:
        expected = json.dumps(
            json.load(f)
        )  # Odd, but doing it for consistency of processing
    assert result == expected
    with open(f"tests/integration_test_files/{filename}_errors.csv", "r") as f:
        expected = read_error_csv(f)
    assert prep_errors_for_csv_compare(errors) == expected


def run_test_html(filename, save=False, highlight=False):
    suffix = "_highlight" if highlight else ""
    usdm = USDMDb()
    errors = usdm.from_excel(f"tests/integration_test_files/{filename}.xlsx")
    result = usdm.to_html("SPONSOR", highlight)

    # Useful if you want to see the results.
    if save or SAVE_ALL:
        with open(f"tests/integration_test_files/{filename}{suffix}.html", "w") as f:
            f.write(format_html(result))
        with open(
            f"tests/integration_test_files/{filename}{suffix}_html_errors.csv",
            "w",
            newline="",
        ) as f:
            save_error_csv(f, errors)

    with open(f"tests/integration_test_files/{filename}{suffix}.html", "r") as f:
        expected = f.read()
    assert format_html(result) == expected
    with open(
        f"tests/integration_test_files/{filename}{suffix}_html_errors.csv", "r"
    ) as f:
        expected = read_error_csv(f)
    assert prep_errors_for_csv_compare(errors) == expected


def run_test_timeline(filename, level=USDMDb.FULL_HTML, save=False):
    usdm = USDMDb()
    usdm.from_excel(f"tests/integration_test_files/{filename}.xlsx")
    result = usdm.to_timeline(level)

    # Useful if you want to see the results.
    if save or SAVE_ALL:
        with open(
            f"tests/integration_test_files/{filename}_timeline_{level}.html", "w"
        ) as f:
            f.write(result)

    with open(
        f"tests/integration_test_files/{filename}_timeline_{level}.html", "r"
    ) as f:
        expected = f.read()
    assert result == expected


def run_test_neo4j(filename, mocker, save=False):
    fake_uuids = (
        UUID(f"00000000-0000-4000-8000-{i:012}", version=4) for i in range(10000)
    )
    mocker.patch("usdm_db.neo4j_dict.uuid4", side_effect=fake_uuids)
    usdm = USDMDb()
    usdm.from_excel(f"tests/integration_test_files/{filename}.xlsx")
    result = usdm.to_neo4j_dict()

    # Useful if you want to see the results.
    if save or SAVE_ALL:
        with open(f"tests/integration_test_files/{filename}_neo4j_dict.yaml", "w") as f:
            f.write(yaml.dump(result))

    with open(f"tests/integration_test_files/{filename}_neo4j_dict.yaml", "r") as f:
        expected = yaml.safe_load(f)
    assert result == expected


def run_test_fhir(filename, mocker, save=False):
    fake_uuids = (
        UUID(f"00000000-0000-4000-8000-{i:012}", version=4) for i in range(1, 10)
    )
    mocker.patch("usdm_db.uuid4", side_effect=fake_uuids)
    usdm = USDMDb()
    usdm.from_excel(f"tests/integration_test_files/{filename}.xlsx")
    result = usdm.to_fhir("sponsor")

    # print(f"RESULT: {result}")

    if save or SAVE_ALL:
        with open(
            f"tests/integration_test_files/{filename}_fhir.json", "w", encoding="utf-8"
        ) as f:
            f.write(json.dumps(json.loads(result), indent=2))

    with open(f"tests/integration_test_files/{filename}_fhir.json", "r") as f:
        expected = json.load(f)
    result_dict = json.loads(result)
    result_dict["entry"][0]["resource"]["date"] = expected["entry"][0]["resource"][
        "date"
    ]  # Date is dynamic, bit of a fiddle but datetime mocking is a pain.
    json.dumps(result_dict) == json.dumps(expected)


def test_observational_1():
    run_test("observational")


def test_full_1():
    run_test("full_1")


def test_full_1_timeline():
    run_test_timeline("full_1")


def test_full_1_timeline_body():
    run_test_timeline("full_1", USDMDb.BODY_HTML)


def test_full_1_html():
    run_test_html("full_1")


def test_full_2():
    run_test("full_2")


def test_full_2_html():
    run_test_html("full_2")


def test_full_3():
    run_test("full_3")


def test_full_3_html():
    run_test_html("full_3")


def test_full_4():
    run_test("full_4")


def test_full_5():
    run_test("full_5")


def test_full_6():
    run_test("full_6")


def test_encounter_1():
    run_test("encounter_1")


def test_simple_1():
    run_test("simple_1")


def test_scope_1():
    run_test("scope_1")


def test_amendment_1():
    run_test("amendment_1")


def test_eligibility_criteria_1():
    run_test("eligibility_criteria_1")


def test_simple_1_html():
    run_test_html("simple_1")


def test_config_1():
    run_test("config_1")


def test_config_2():
    run_test("config_2")


def test_no_activity_sheet():
    run_test("no_activity_sheet")


def test_address():
    run_test("address")


def test_complex_1():
    run_test("complex_1")


def test_arms_epochs_1():
    run_test("arms_epochs")


def test_cycles_1():
    run_test("cycles_1")


def test_multiple_column_names():
    run_test("multiple_column_names")


def test_invalid_section_levels():
    run_test("invalid_section_levels")


def test_new_field_names():
    run_test("new_labels")


def test_timing_check():
    run_test("timing_check")


def test_v2_soa_1():
    run_test("simple_1_v2")


def test_v2_soa_2():
    run_test("decision_1_v2")


def test_timeline_1():
    run_test_timeline("simple_1_v2")


def test_timeline_2():
    run_test_timeline("decision_1_v2")


def test_timeline_3():
    run_test_timeline("complex_1")


def test_timeline_4():
    run_test_timeline("cycles_1")


def test_path_error():
    run_test("path_error")


def test_references():
    run_test("references")


def test_references_html():
    run_test_html("references")


def test_references_html_highlight():
    run_test_html("references", highlight=True)


def test_simple_neo4j_1(mocker):
    run_test_neo4j("simple_1", mocker)


def test_full_neo4j_1(mocker):
    run_test_neo4j("full_1", mocker)


def test_full_neo4j_2(mocker):
    run_test_neo4j("full_2", mocker)


def test_full_neo4j_3(mocker):
    run_test_neo4j("full_3", mocker)


def test_full_fhir_1(mocker):
    run_test_fhir("full_1", mocker)


def test_group_activities_1(mocker):
    run_test("group_activities_1", mocker)


def test_notes_1(mocker):
    run_test("annotations_and_abbreviations", mocker)


def test_template_1(mocker):
    run_test("template", mocker)


def test_interventions_1(mocker):
    run_test("interventions", mocker)


def test_study_devices_1(mocker):
    run_test("devices", mocker)


def test_time_duration_1(mocker):
    run_test("timeline_duration", mocker)


def test_minimum(mocker):
    run_test("minimum", mocker)
