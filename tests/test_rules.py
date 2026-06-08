from reviewpack.config import ReviewpackConfig
from reviewpack.models import ChangedFile, FileCategory
from reviewpack.rules import (
    categorize_file,
    classify_changed_files,
    compute_change_stats,
    detect_risk_signals,
    matches_path_pattern,
)


def test_matches_path_pattern_supports_directory_prefix() -> None:
    assert matches_path_pattern("docs/usage.md", "docs/")
    assert not matches_path_pattern("src/docs.py", "docs/")


def test_matches_path_pattern_supports_exact_file() -> None:
    assert matches_path_pattern("pyproject.toml", "pyproject.toml")
    assert not matches_path_pattern("docs/pyproject.toml", "pyproject.toml")


def test_matches_path_pattern_supports_glob() -> None:
    assert matches_path_pattern("src/app.py", "src/*.py")
    assert not matches_path_pattern("src/app.js", "src/*.py")


def test_categorize_file_uses_default_patterns() -> None:
    assert categorize_file("tests/test_cli.py") == FileCategory.TEST
    assert categorize_file("README.md") == FileCategory.DOCS
    assert categorize_file("pyproject.toml") == FileCategory.DEPENDENCY
    assert categorize_file(".github/workflows/ci.yml") == FileCategory.CI
    assert categorize_file("Dockerfile") == FileCategory.INFRA
    assert categorize_file("src/app.py") == FileCategory.SOURCE


def test_categorize_file_uses_custom_patterns() -> None:
    config = ReviewpackConfig.model_validate(
        {
            "paths": {
                "docs": ["documentation/"],
                "tests": ["spec/"],
                "dependencies": ["uv.lock"],
            }
        }
    )

    assert categorize_file("documentation/index.md", config) == FileCategory.DOCS
    assert categorize_file("spec/test_app.py", config) == FileCategory.TEST
    assert categorize_file("uv.lock", config) == FileCategory.DEPENDENCY


def test_classify_changed_files_preserves_explicit_category() -> None:
    config = ReviewpackConfig()
    changed_files = [
        ChangedFile(
            path="custom/file.txt",
            additions=1,
            deletions=0,
            category=FileCategory.DOCS,
        )
    ]

    classified = classify_changed_files(changed_files, config)

    assert classified[0].category == FileCategory.DOCS


def test_compute_change_stats_counts_categories() -> None:
    changed_files = [
        ChangedFile(path="src/app.py", additions=10, deletions=1, category=FileCategory.SOURCE),
        ChangedFile(path="tests/test_app.py", additions=5, deletions=0, category=FileCategory.TEST),
        ChangedFile(path="README.md", additions=2, deletions=0, category=FileCategory.DOCS),
    ]

    stats = compute_change_stats(changed_files)

    assert stats.files_changed == 3
    assert stats.additions == 17
    assert stats.deletions == 1
    assert stats.source_files == 1
    assert stats.test_files == 1
    assert stats.docs_files == 1


def test_detect_risk_signals_uses_configured_large_pr_thresholds() -> None:
    config = ReviewpackConfig.model_validate(
        {
            "risk": {
                "large_pr_files": 2,
                "large_pr_lines": 10,
            }
        }
    )
    changed_files = [
        ChangedFile(path="src/app.py", additions=8, deletions=3, category=FileCategory.SOURCE),
        ChangedFile(path="tests/test_app.py", additions=1, deletions=0, category=FileCategory.TEST),
    ]
    stats = compute_change_stats(changed_files)

    signals = detect_risk_signals(changed_files, stats, config)
    titles = {signal.title for signal in signals}

    assert "Large pull request" in titles
    assert "Large line change" in titles


def test_detect_risk_signals_uses_configured_high_risk_paths() -> None:
    config = ReviewpackConfig.model_validate(
        {
            "risk": {
                "high_risk_paths": [
                    ".github/workflows/",
                    "pyproject.toml",
                ]
            }
        }
    )
    changed_files = [
        ChangedFile(path=".github/workflows/ci.yml", additions=1, deletions=1, category=FileCategory.CI),
        ChangedFile(path="README.md", additions=1, deletions=0, category=FileCategory.DOCS),
    ]
    stats = compute_change_stats(changed_files)

    signals = detect_risk_signals(changed_files, stats, config)

    assert any(signal.title == "Configured high-risk path changed" for signal in signals)
