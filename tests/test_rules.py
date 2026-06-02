from reviewpack.config import ReviewpackConfig
from reviewpack.models import ChangedFile, FileCategory
from reviewpack.rules import categorize_file, generate_risk_signals


def test_categorize_source_file() -> None:
    assert categorize_file("src/app.py") == FileCategory.SOURCE


def test_categorize_test_file() -> None:
    assert categorize_file("tests/test_app.py") == FileCategory.TEST


def test_categorize_docs_file() -> None:
    assert categorize_file("README.md") == FileCategory.DOCS


def test_categorize_dependency_file() -> None:
    assert categorize_file("package.json") == FileCategory.DEPENDENCY


def test_categorize_ci_file() -> None:
    assert categorize_file(".github/workflows/ci.yml") == FileCategory.CI


def test_generate_source_without_tests_signal() -> None:
    files = [
        ChangedFile(
            path="src/app.py",
            additions=10,
            deletions=2,
            category=FileCategory.SOURCE,
        )
    ]

    signals = generate_risk_signals(files)

    assert any(signal.title == "Source changed without tests" for signal in signals)


def test_generate_high_risk_path_signal() -> None:
    config = ReviewpackConfig()
    files = [
        ChangedFile(
            path="src/auth/token.py",
            additions=10,
            deletions=2,
            category=FileCategory.SOURCE,
        )
    ]

    signals = generate_risk_signals(files, config)

    assert any(signal.title == "High-risk area changed" for signal in signals)
