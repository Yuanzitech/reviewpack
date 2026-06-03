from pathlib import Path

import yaml


def load_publish_workflow() -> dict:
    workflow_path = Path(".github/workflows/publish.yml")

    assert workflow_path.exists()

    data = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))

    assert isinstance(data, dict)

    return data


def get_workflow_triggers(data: dict) -> dict:
    triggers = data.get("on")

    if triggers is None:
        triggers = data.get(True)

    assert isinstance(triggers, dict)

    return triggers


def test_publish_workflow_has_manual_trigger() -> None:
    data = load_publish_workflow()
    triggers = get_workflow_triggers(data)

    assert "workflow_dispatch" in triggers


def test_publish_workflow_has_expected_inputs() -> None:
    data = load_publish_workflow()
    triggers = get_workflow_triggers(data)
    workflow_dispatch = triggers["workflow_dispatch"]
    inputs = workflow_dispatch["inputs"]

    assert "repository" in inputs
    assert "dry-run" in inputs
    assert inputs["repository"]["default"] == "testpypi"
    assert inputs["dry-run"]["default"] is True


def test_publish_workflow_has_build_and_publish_jobs() -> None:
    data = load_publish_workflow()
    jobs = data["jobs"]

    assert "build" in jobs
    assert "publish-testpypi" in jobs
    assert "publish-pypi" in jobs


def test_publish_workflow_uses_trusted_publishing_permissions() -> None:
    data = load_publish_workflow()
    jobs = data["jobs"]

    assert jobs["publish-testpypi"]["permissions"]["id-token"] == "write"
    assert jobs["publish-pypi"]["permissions"]["id-token"] == "write"


def test_publish_workflow_publish_jobs_depend_on_build() -> None:
    data = load_publish_workflow()
    jobs = data["jobs"]

    assert jobs["publish-testpypi"]["needs"] == "build"
    assert jobs["publish-pypi"]["needs"] == "build"
