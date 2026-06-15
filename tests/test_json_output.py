import json

from reviewpack.analyzer import analyze_reviewpack_input
from reviewpack.demo import build_demo_reviewpack_input
from reviewpack.renderers import write_reviewpack_outputs


EXPECTED_TOP_LEVEL_KEYS = {
    "pr",
    "changed_files",
    "stats",
    "risk_signals",
    "review_focus",
    "metadata",
}


EXPECTED_PR_KEYS = {
    "title",
    "author",
    "url",
    "description",
    "state",
    "is_draft",
    "base_branch",
    "head_branch",
    "commit_count",
    "labels",
}


EXPECTED_CHANGED_FILE_KEYS = {
    "path",
    "additions",
    "deletions",
    "category",
    "status",
}


EXPECTED_STATS_KEYS = {
    "files_changed",
    "additions",
    "deletions",
    "source_files",
    "test_files",
    "docs_files",
    "dependency_files",
    "ci_files",
    "config_files",
    "infra_files",
    "unknown_files",
}


EXPECTED_RISK_SIGNAL_KEYS = {
    "level",
    "title",
    "message",
    "files",
}


EXPECTED_REVIEW_FOCUS_KEYS = {
    "title",
    "reason",
}


def load_demo_json_output(tmp_path) -> dict:
    result = analyze_reviewpack_input(build_demo_reviewpack_input())

    write_reviewpack_outputs(result, tmp_path)

    json_path = tmp_path / "reviewpack.json"

    assert json_path.exists()

    return json.loads(json_path.read_text(encoding="utf-8"))


def test_reviewpack_json_has_expected_top_level_keys(tmp_path) -> None:
    data = load_demo_json_output(tmp_path)

    assert EXPECTED_TOP_LEVEL_KEYS.issubset(data.keys())


def test_reviewpack_json_pr_object_has_expected_keys(tmp_path) -> None:
    data = load_demo_json_output(tmp_path)

    assert isinstance(data["pr"], dict)
    assert EXPECTED_PR_KEYS.issubset(data["pr"].keys())


def test_reviewpack_json_changed_files_have_expected_keys(tmp_path) -> None:
    data = load_demo_json_output(tmp_path)

    assert isinstance(data["changed_files"], list)
    assert data["changed_files"]

    for changed_file in data["changed_files"]:
        assert EXPECTED_CHANGED_FILE_KEYS.issubset(changed_file.keys())


def test_reviewpack_json_stats_has_expected_keys(tmp_path) -> None:
    data = load_demo_json_output(tmp_path)

    assert isinstance(data["stats"], dict)
    assert EXPECTED_STATS_KEYS.issubset(data["stats"].keys())


def test_reviewpack_json_risk_signals_have_expected_keys(tmp_path) -> None:
    data = load_demo_json_output(tmp_path)

    assert isinstance(data["risk_signals"], list)
    assert data["risk_signals"]

    for risk_signal in data["risk_signals"]:
        assert EXPECTED_RISK_SIGNAL_KEYS.issubset(risk_signal.keys())


def test_reviewpack_json_review_focus_items_have_expected_keys(tmp_path) -> None:
    data = load_demo_json_output(tmp_path)

    assert isinstance(data["review_focus"], list)
    assert data["review_focus"]

    for review_focus_item in data["review_focus"]:
        assert EXPECTED_REVIEW_FOCUS_KEYS.issubset(review_focus_item.keys())


def test_reviewpack_json_metadata_contains_expected_defaults(tmp_path) -> None:
    data = load_demo_json_output(tmp_path)

    assert isinstance(data["metadata"], dict)
    assert data["metadata"]["ai_used"] is False
    assert data["metadata"]["network_used"] is False


def test_json_output_document_exists() -> None:
    from pathlib import Path

    assert Path("docs/json-output.md").exists()
