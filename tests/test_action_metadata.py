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
        "comment",
    }

    assert expected_inputs.issubset(set(inputs))


def test_action_metadata_defaults_to_github_mode() -> None:
    data = load_action_metadata()
    inputs = data["inputs"]

    assert inputs["mode"]["default"] == "github"
    assert inputs["output"]["default"] == ".reviewpack"
    assert inputs["upload-artifact"]["default"] == "true"
    assert inputs["comment"]["default"] == "false"


def test_action_metadata_has_expected_steps() -> None:
    data = load_action_metadata()
    steps = data["runs"]["steps"]
    step_names = {step["name"] for step in steps}

    assert "Set up Python" in step_names
    assert "Install Reviewpack" in step_names
    assert "Run Reviewpack" in step_names
    assert "Show Reviewpack next steps" in step_names
    assert "Upload Reviewpack artifact" in step_names
    assert "Post Reviewpack PR comment" in step_names


def test_action_metadata_uploads_hidden_reviewpack_outputs() -> None:
    data = load_action_metadata()
    steps = data["runs"]["steps"]

    upload_steps = [step for step in steps if step["name"] == "Upload Reviewpack artifact"]

    assert len(upload_steps) == 1

    upload_step = upload_steps[0]
    upload_with = upload_step["with"]

    assert upload_with["if-no-files-found"] == "error"
    assert upload_with["include-hidden-files"] is True


def test_action_metadata_next_steps_mentions_handoff_files_and_comment_mode() -> None:
    data = load_action_metadata()
    steps = data["runs"]["steps"]

    guidance_steps = [step for step in steps if step["name"] == "Show Reviewpack next steps"]

    assert len(guidance_steps) == 1

    run_text = guidance_steps[0]["run"]

    assert "ai-handoff.md" in run_text
    assert "ai-context.md" in run_text
    assert "reviewpack-output" in run_text or "ARTIFACT_NAME" in run_text
    assert "comment" in run_text


def test_action_metadata_comment_step_is_opt_in() -> None:
    data = load_action_metadata()
    steps = data["runs"]["steps"]

    comment_steps = [step for step in steps if step["name"] == "Post Reviewpack PR comment"]

    assert len(comment_steps) == 1

    comment_step = comment_steps[0]

    assert comment_step["if"] == "${{ inputs.comment == 'true' }}"
    assert "python -m reviewpack.github_comment" in comment_step["run"]
