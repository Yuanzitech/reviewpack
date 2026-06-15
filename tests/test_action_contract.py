from pathlib import Path

import yaml


EXPECTED_ACTION_INPUTS = {
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


def load_action_metadata() -> dict:
    action_path = Path("action.yml")

    assert action_path.exists()

    data = yaml.safe_load(action_path.read_text(encoding="utf-8"))

    assert isinstance(data, dict)

    return data


def test_action_contract_has_expected_identity() -> None:
    data = load_action_metadata()

    assert data["name"] == "Reviewpack"
    assert "Privacy-first context packs" in data["description"]
    assert data["author"] == "Yuanzitech"
    assert data["runs"]["using"] == "composite"


def test_action_contract_input_names_remain_stable() -> None:
    data = load_action_metadata()
    inputs = data["inputs"]

    assert set(inputs) == EXPECTED_ACTION_INPUTS


def test_action_contract_default_values_remain_stable() -> None:
    data = load_action_metadata()
    inputs = data["inputs"]

    assert inputs["mode"]["default"] == "github"
    assert inputs["pr-url"]["default"] == ""
    assert inputs["base"]["default"] == "main"
    assert inputs["head"]["default"] == "HEAD"
    assert inputs["output"]["default"] == ".reviewpack"
    assert inputs["preview-ai-input"]["default"] == "false"
    assert inputs["upload-artifact"]["default"] == "true"
    assert inputs["artifact-name"]["default"] == "reviewpack-output"
    assert inputs["github-token"]["default"] == ""
    assert inputs["comment"]["default"] == "false"


def test_action_contract_comment_mode_remains_opt_in() -> None:
    data = load_action_metadata()
    inputs = data["inputs"]
    steps = data["runs"]["steps"]

    assert inputs["comment"]["default"] == "false"

    comment_steps = [step for step in steps if step["name"] == "Post Reviewpack PR comment"]

    assert len(comment_steps) == 1

    comment_step = comment_steps[0]

    assert comment_step["if"] == "${{ inputs.comment == 'true' }}"
    assert "python -m reviewpack.github_comment" in comment_step["run"]


def test_action_contract_artifact_upload_defaults_remain_enabled() -> None:
    data = load_action_metadata()
    inputs = data["inputs"]

    assert inputs["upload-artifact"]["default"] == "true"
    assert inputs["artifact-name"]["default"] == "reviewpack-output"


def test_action_contract_artifact_upload_includes_hidden_files() -> None:
    data = load_action_metadata()
    steps = data["runs"]["steps"]

    upload_steps = [step for step in steps if step["name"] == "Upload Reviewpack artifact"]

    assert len(upload_steps) == 1

    upload_step = upload_steps[0]

    assert upload_step["if"] == "${{ inputs.upload-artifact == 'true' }}"
    assert upload_step["uses"] == "actions/upload-artifact@v4"
    assert upload_step["with"]["name"] == "${{ inputs.artifact-name }}"
    assert upload_step["with"]["path"] == "${{ inputs.output }}"
    assert upload_step["with"]["if-no-files-found"] == "error"
    assert upload_step["with"]["include-hidden-files"] is True


def test_action_contract_run_step_supports_github_and_local_modes() -> None:
    data = load_action_metadata()
    steps = data["runs"]["steps"]

    run_steps = [step for step in steps if step["name"] == "Run Reviewpack"]

    assert len(run_steps) == 1

    run_text = run_steps[0]["run"]

    assert 'if [ "$MODE" = "github" ]; then' in run_text
    assert 'elif [ "$MODE" = "local" ]; then' in run_text
    assert 'reviewpack github "$PR_URL"' in run_text
    assert "reviewpack local" in run_text
    assert "--base" in run_text
    assert "--head" in run_text
    assert "--output" in run_text


def test_action_contract_next_steps_mentions_artifact_and_ai_handoff() -> None:
    data = load_action_metadata()
    steps = data["runs"]["steps"]

    guidance_steps = [step for step in steps if step["name"] == "Show Reviewpack next steps"]

    assert len(guidance_steps) == 1

    run_text = guidance_steps[0]["run"]

    assert "ai-handoff.md" in run_text
    assert "ai-context.md" in run_text
    assert "ai-review-prompt.md" in run_text
    assert "reviewpack.json" in run_text
    assert "ARTIFACT_NAME" in run_text
    assert "comment" in run_text


def test_action_contract_comment_step_requires_token_and_pr_url() -> None:
    data = load_action_metadata()
    steps = data["runs"]["steps"]

    comment_steps = [step for step in steps if step["name"] == "Post Reviewpack PR comment"]

    assert len(comment_steps) == 1

    run_text = comment_steps[0]["run"]

    assert "github-token is required when comment mode is enabled" in run_text
    assert "pr-url is required when comment mode is enabled" in run_text

    env = comment_steps[0]["env"]

    assert env["REVIEWPACK_GITHUB_TOKEN"] == "${{ inputs.github-token }}"
    assert env["REVIEWPACK_PR_URL"] == "${{ inputs.pr-url }}"
    assert env["REVIEWPACK_OUTPUT_DIR"] == "${{ inputs.output }}"
    assert env["REVIEWPACK_ARTIFACT_NAME"] == "${{ inputs.artifact-name }}"
    assert "github.server_url" in env["REVIEWPACK_WORKFLOW_RUN_URL"]
    assert "github.run_id" in env["REVIEWPACK_WORKFLOW_RUN_URL"]


def test_github_action_docs_document_comment_mode_permissions_and_fork_limits() -> None:
    docs = Path("docs/github-action.md").read_text(encoding="utf-8")

    assert 'comment: "true"' in docs
    assert "pull-requests: write" in docs
    assert "pull-requests: read" in docs
    assert "forks" in docs.lower()
    assert "write permissions" in docs
    assert "disabled by default" in docs


def test_readme_documents_optional_comment_mode_permissions() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert 'comment: "true"' in readme
    assert "pull-requests: write" in readme
    assert "does not post PR comments" in readme
    assert "No PR comments by default" in readme


def test_chinese_readme_documents_optional_comment_mode_permissions() -> None:
    readme = Path("README.zh-CN.md").read_text(encoding="utf-8")

    assert 'comment: "true"' in readme
    assert "pull-requests: write" in readme
    assert "默认不会自动评论 PR" in readme
    assert "默认不评论 PR" in readme
