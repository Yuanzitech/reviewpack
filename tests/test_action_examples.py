from pathlib import Path

import yaml


EXAMPLE_WORKFLOWS = {
    "examples/github-action.yml",
    "examples/github-action-local.yml",
    "examples/github-action-comment.yml",
}


def load_workflow(path: str) -> dict:
    workflow_path = Path(path)

    assert workflow_path.exists()

    data = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))

    assert isinstance(data, dict)

    return data


def get_reviewpack_step(workflow: dict) -> dict:
    jobs = workflow["jobs"]

    assert isinstance(jobs, dict)
    assert "reviewpack" in jobs

    steps = jobs["reviewpack"]["steps"]

    reviewpack_steps = [
        step
        for step in steps
        if isinstance(step, dict) and str(step.get("uses", "")).startswith("Yuanzitech/reviewpack@")
    ]

    assert len(reviewpack_steps) == 1

    return reviewpack_steps[0]


def test_expected_github_action_example_files_exist() -> None:
    for workflow_path in sorted(EXAMPLE_WORKFLOWS):
        assert Path(workflow_path).exists(), f"Missing workflow example: {workflow_path}"


def test_github_mode_example_uses_expected_inputs() -> None:
    workflow = load_workflow("examples/github-action.yml")
    reviewpack_step = get_reviewpack_step(workflow)

    with_config = reviewpack_step["with"]

    assert with_config["mode"] == "github"
    assert with_config["pr-url"] == "${{ github.event.pull_request.html_url }}"
    assert with_config["github-token"] == "${{ github.token }}"
    assert with_config["preview-ai-input"] == "true"

    permissions = workflow["jobs"]["reviewpack"]["permissions"]

    assert permissions["contents"] == "read"
    assert permissions["pull-requests"] == "read"


def test_local_mode_example_uses_expected_inputs() -> None:
    workflow = load_workflow("examples/github-action-local.yml")
    reviewpack_step = get_reviewpack_step(workflow)

    with_config = reviewpack_step["with"]

    assert with_config["mode"] == "local"
    assert with_config["base"] == "main"
    assert with_config["head"] == "HEAD"
    assert with_config["preview-ai-input"] == "true"

    permissions = workflow["jobs"]["reviewpack"]["permissions"]

    assert permissions["contents"] == "read"

    checkout_steps = [
        step
        for step in workflow["jobs"]["reviewpack"]["steps"]
        if isinstance(step, dict) and step.get("uses") == "actions/checkout@v4"
    ]

    assert len(checkout_steps) == 1
    assert checkout_steps[0]["with"]["fetch-depth"] == 0


def test_comment_mode_example_is_explicitly_opt_in() -> None:
    workflow = load_workflow("examples/github-action-comment.yml")
    reviewpack_step = get_reviewpack_step(workflow)

    with_config = reviewpack_step["with"]

    assert with_config["mode"] == "github"
    assert with_config["pr-url"] == "${{ github.event.pull_request.html_url }}"
    assert with_config["github-token"] == "${{ github.token }}"
    assert with_config["comment"] == "true"
    assert with_config["preview-ai-input"] == "true"

    permissions = workflow["jobs"]["reviewpack"]["permissions"]

    assert permissions["contents"] == "read"
    assert permissions["pull-requests"] == "write"


def test_examples_do_not_enable_comment_mode_except_comment_example() -> None:
    github_workflow = load_workflow("examples/github-action.yml")
    local_workflow = load_workflow("examples/github-action-local.yml")
    comment_workflow = load_workflow("examples/github-action-comment.yml")

    github_step = get_reviewpack_step(github_workflow)
    local_step = get_reviewpack_step(local_workflow)
    comment_step = get_reviewpack_step(comment_workflow)

    assert github_step["with"].get("comment") is None
    assert local_step["with"].get("comment") is None
    assert comment_step["with"]["comment"] == "true"


def test_examples_use_current_checkout_action() -> None:
    for workflow_path in sorted(EXAMPLE_WORKFLOWS):
        workflow = load_workflow(workflow_path)
        steps = workflow["jobs"]["reviewpack"]["steps"]

        checkout_steps = [
            step
            for step in steps
            if isinstance(step, dict) and str(step.get("uses", "")).startswith("actions/checkout@")
        ]

        assert len(checkout_steps) == 1
        assert checkout_steps[0]["uses"] == "actions/checkout@v4"


def test_examples_use_reviewpack_action_reference() -> None:
    for workflow_path in sorted(EXAMPLE_WORKFLOWS):
        workflow = load_workflow(workflow_path)
        reviewpack_step = get_reviewpack_step(workflow)

        assert reviewpack_step["uses"].startswith("Yuanzitech/reviewpack@")
