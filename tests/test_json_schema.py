import json
from pathlib import Path
from typing import Any

from reviewpack.analyzer import analyze_reviewpack_input
from reviewpack.demo import build_demo_reviewpack_input
from reviewpack.renderers import write_reviewpack_outputs


SCHEMA_PATH = Path("schemas/reviewpack-result.schema.json")


def load_schema() -> dict[str, Any]:
    assert SCHEMA_PATH.exists()

    data = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    assert isinstance(data, dict)

    return data


def load_demo_reviewpack_json(tmp_path) -> dict[str, Any]:
    result = analyze_reviewpack_input(build_demo_reviewpack_input())

    write_reviewpack_outputs(result, tmp_path)

    output_path = tmp_path / "reviewpack.json"

    assert output_path.exists()

    data = json.loads(output_path.read_text(encoding="utf-8"))

    assert isinstance(data, dict)

    return data


def assert_required_keys(data: dict[str, Any], schema: dict[str, Any]) -> None:
    required = schema.get("required", [])

    assert isinstance(required, list)

    for key in required:
        assert key in data, f"Missing required key: {key}"


def assert_type(value: Any, expected_type: str | list[str], path: str) -> None:
    expected_types = expected_type if isinstance(expected_type, list) else [expected_type]

    if "null" in expected_types and value is None:
        return

    type_checks = {
        "object": lambda item: isinstance(item, dict),
        "array": lambda item: isinstance(item, list),
        "string": lambda item: isinstance(item, str),
        "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
        "boolean": lambda item: isinstance(item, bool),
    }

    for type_name in expected_types:
        check = type_checks.get(type_name)
        if check is not None and check(value):
            return

    raise AssertionError(f"{path} expected type {expected_types}, got {type(value).__name__}")


def assert_object_matches_schema(data: dict[str, Any], schema: dict[str, Any], path: str = "$") -> None:
    assert_required_keys(data, schema)

    properties = schema.get("properties", {})

    assert isinstance(properties, dict)

    for key, property_schema in properties.items():
        if key not in data:
            continue

        assert isinstance(property_schema, dict)

        expected_type = property_schema.get("type")
        if expected_type is not None:
            assert_type(data[key], expected_type, f"{path}.{key}")

        if property_schema.get("type") == "object" and isinstance(data[key], dict):
            assert_object_matches_schema(data[key], property_schema, f"{path}.{key}")

        if property_schema.get("type") == "array" and isinstance(data[key], list):
            item_schema = property_schema.get("items")
            if isinstance(item_schema, dict):
                for index, item in enumerate(data[key]):
                    expected_item_type = item_schema.get("type")
                    if expected_item_type is not None:
                        assert_type(item, expected_item_type, f"{path}.{key}[{index}]")

                    if expected_item_type == "object" and isinstance(item, dict):
                        assert_object_matches_schema(item, item_schema, f"{path}.{key}[{index}]")


def test_schema_file_is_valid_json() -> None:
    schema = load_schema()

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["title"] == "Reviewpack Result"
    assert schema["type"] == "object"


def test_schema_documents_pre_1_0_draft_status() -> None:
    schema = load_schema()

    assert "Draft pre-1.0" in schema["description"]


def test_schema_allows_additional_top_level_properties() -> None:
    schema = load_schema()

    assert schema["additionalProperties"] is True


def test_schema_defines_expected_top_level_required_keys() -> None:
    schema = load_schema()

    assert schema["required"] == [
        "pr",
        "changed_files",
        "stats",
        "risk_signals",
        "review_focus",
        "metadata",
    ]


def test_demo_reviewpack_json_matches_draft_schema(tmp_path) -> None:
    schema = load_schema()
    data = load_demo_reviewpack_json(tmp_path)

    assert_object_matches_schema(data, schema)


def test_schema_defines_file_category_enum() -> None:
    schema = load_schema()

    category_schema = schema["properties"]["changed_files"]["items"]["properties"]["category"]

    assert category_schema["enum"] == [
        "source",
        "test",
        "docs",
        "dependency",
        "ci",
        "config",
        "infrastructure",
        "unknown",
    ]


def test_schema_defines_risk_level_enum() -> None:
    schema = load_schema()

    level_schema = schema["properties"]["risk_signals"]["items"]["properties"]["level"]

    assert level_schema["enum"] == [
        "high",
        "medium",
        "low",
    ]


def test_json_integration_guide_exists_and_mentions_schema() -> None:
    guide_path = Path("docs/integration-json.md")

    assert guide_path.exists()

    guide = guide_path.read_text(encoding="utf-8")

    assert "schemas/reviewpack-result.schema.json" in guide
    assert "pre-1.0" in guide
    assert "Pin Reviewpack versions" in guide
    assert "Treat unknown fields as allowed" in guide
    assert "Treat optional fields as optional" in guide
