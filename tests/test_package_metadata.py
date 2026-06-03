from pathlib import Path


def read_pyproject() -> str:
    pyproject = Path("pyproject.toml")

    assert pyproject.exists()

    return pyproject.read_text(encoding="utf-8")


def test_pyproject_has_expected_project_name() -> None:
    text = read_pyproject()

    assert 'name = "reviewpack"' in text


def test_pyproject_has_non_placeholder_project_urls() -> None:
    text = read_pyproject()

    assert "https://github.com/Yuanzitech/reviewpack" in text
    assert "https://github.com/yourname/reviewpack" not in text


def test_pyproject_defines_cli_entrypoint() -> None:
    text = read_pyproject()

    assert '[project.scripts]' in text
    assert 'reviewpack = "reviewpack.cli:app"' in text


def test_pyproject_declares_hatch_wheel_package() -> None:
    text = read_pyproject()

    assert "[tool.hatch.build.targets.wheel]" in text
    assert 'packages = ["reviewpack"]' in text


def test_pyproject_requires_supported_python_version() -> None:
    text = read_pyproject()

    assert 'requires-python = ">=3.10"' in text
