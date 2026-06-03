from pathlib import Path

import yaml


def load_action_metadata() -> dict:
    action_path = Path("action.yml")

    assert action_path.exists()

    data = yaml.safe_load(action_path.read_text(encoding="utf-8"))

    assert isinstance(data, dict)

    return data


def test_action_metadata_has_required_top_level_fields() -> None:
    data = load_action_metadata()

    assert data["name"] == "Reviewpack"
    assert "description" in data
    assert data["runs"]["using"] == "composite"


def test_action_metadata_defines_expected_inputs() -> None:
    data = load_action_metadata()
    inputs = data["inputs"]

    expected_inputs = {
        "mode",
        "pr-url",
        "base",
        "head",
        "output",
        "preview-ai-input",
        "upload-artifact",
        "artifact-name",
        "github-token",
    }

    assert expected_inputs.issubset(set(inputs))


def test_action_metadata_defaults_to_github_mode() -> None:
    data = load_action_metadata()
    inputs = data["inputs"]

    assert inputs["mode"]["default"] == "github"
    assert inputs["output"]["default"] == ".reviewpack"
    assert inputs["upload-artifact"]["default"] == "true"


def test_action_metadata_has_install_and_run_steps() -> None:
    data = load_action_metadata()
    steps = data["runs"]["steps"]
    step_names = {step["name"] for step in steps}

    assert "Set up Python" in step_names
    assert "Install Reviewpack" in step_names
    assert "Run Reviewpack" in step_names
    assert "Upload Reviewpack artifact" in step_names
