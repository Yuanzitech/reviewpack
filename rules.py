from __future__ import annotations

from fnmatch import fnmatch

from reviewpack.config import ReviewpackConfig
from reviewpack.models import ChangedFile, FileCategory, RiskLevel, RiskSignal


DEPENDENCY_FILES = {
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "requirements.txt",
    "requirements-dev.txt",
    "pyproject.toml",
    "poetry.lock",
    "Pipfile",
    "Pipfile.lock",
    "go.mod",
    "go.sum",
    "Cargo.toml",
    "Cargo.lock",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
}

CI_PATTERNS = [
    ".github/workflows/**",
    ".gitlab-ci.yml",
    "azure-pipelines.yml",
    "circle.yml",
    ".circleci/**",
]

DOCS_PATTERNS = [
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "docs/**",
]

TEST_PATTERNS = [
    "tests/**",
    "test/**",
    "__tests__/**",
    "**/tests/**",
    "**/test/**",
    "**/*_test.py",
    "**/test_*.py",
    "**/*.test.js",
    "**/*.test.ts",
    "**/*.spec.js",
    "**/*.spec.ts",
]

INFRA_PATTERNS = [
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "k8s/**",
    "helm/**",
    "terraform/**",
    "*.tf",
]

CONFIG_PATTERNS = [
    ".editorconfig",
    ".prettierrc",
    ".eslintrc",
    ".eslintrc.*",
    "ruff.toml",
    "mypy.ini",
    "pytest.ini",
    "tox.ini",
    "tsconfig.json",
    "vite.config.*",
    "webpack.config.*",
]

SOURCE_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".kts",
    ".rb",
    ".php",
    ".cs",
    ".cpp",
    ".cc",
    ".c",
    ".h",
    ".hpp",
    ".swift",
    ".scala",
    ".sql",
}


def matches_any(path: str, patterns: list[str]) -> bool:
    """Return True when a path matches at least one glob pattern."""

    return any(fnmatch(path, pattern) for pattern in patterns)


def has_source_extension(path: str) -> bool:
    """Return True when the file extension looks like source code."""

    return any(path.endswith(extension) for extension in SOURCE_EXTENSIONS)


def categorize_file(path: str, config: ReviewpackConfig | None = None) -> FileCategory:
    """Categorize a changed file path."""

    active_config = config or ReviewpackConfig()

    if matches_any(path, active_config.test_paths) or matches_any(path, TEST_PATTERNS):
        return FileCategory.TEST

    if matches_any(path, active_config.docs_paths) or matches_any(path, DOCS_PATTERNS):
        return FileCategory.DOCS

    if path in DEPENDENCY_FILES:
        return FileCategory.DEPENDENCY

    if matches_any(path, CI_PATTERNS):
        return FileCategory.CI

    if matches_any(path, INFRA_PATTERNS):
        return FileCategory.INFRA

    if matches_any(path, CONFIG_PATTERNS):
        return FileCategory.CONFIG

    if has_source_extension(path):
        return FileCategory.SOURCE

    return FileCategory.UNKNOWN


def touches_high_risk_path(files: list[ChangedFile], config: ReviewpackConfig) -> list[str]:
    """Return files that match configured high-risk path patterns."""

    matched: list[str] = []

    for changed_file in files:
        if matches_any(changed_file.path, config.risk_paths_high):
            matched.append(changed_file.path)

    return matched


def generate_risk_signals(
    files: list[ChangedFile],
    config: ReviewpackConfig | None = None,
) -> list[RiskSignal]:
    """Generate deterministic risk signals from changed files."""

    active_config = config or ReviewpackConfig()
    signals: list[RiskSignal] = []

    source_files = [item.path for item in files if item.category == FileCategory.SOURCE]
    test_files = [item.path for item in files if item.category == FileCategory.TEST]
    docs_files = [item.path for item in files if item.category == FileCategory.DOCS]
    dependency_files = [item.path for item in files if item.category == FileCategory.DEPENDENCY]
    ci_files = [item.path for item in files if item.category == FileCategory.CI]
    infra_files = [item.path for item in files if item.category == FileCategory.INFRA]

    total_changed_lines = sum(item.additions + item.deletions for item in files)

    if source_files and not test_files:
        signals.append(
            RiskSignal(
                level=RiskLevel.MEDIUM,
                title="Source changed without tests",
                message="Source files changed, but no test files were updated.",
                files=source_files,
            )
        )

    if source_files and not docs_files:
        signals.append(
            RiskSignal(
                level=RiskLevel.LOW,
                title="Source changed without docs",
                message="Source files changed, but no documentation files were updated.",
                files=source_files,
            )
        )

    if dependency_files:
        signals.append(
            RiskSignal(
                level=RiskLevel.MEDIUM,
                title="Dependency files changed",
                message="Dependency files changed. Review compatibility, security, and lockfile consistency.",
                files=dependency_files,
            )
        )

    if ci_files:
        signals.append(
            RiskSignal(
                level=RiskLevel.MEDIUM,
                title="CI workflow changed",
                message="CI configuration changed. Review triggers, permissions, secrets usage, and required checks.",
                files=ci_files,
            )
        )

    if infra_files:
        signals.append(
            RiskSignal(
                level=RiskLevel.MEDIUM,
                title="Infrastructure files changed",
                message="Infrastructure-related files changed. Review deployment, runtime, and environment impact.",
                files=infra_files,
            )
        )

    high_risk_files = touches_high_risk_path(files, active_config)
    if high_risk_files:
        signals.append(
            RiskSignal(
                level=RiskLevel.HIGH,
                title="High-risk area changed",
                message="Configured high-risk paths changed. Review security, compatibility, and edge cases carefully.",
                files=high_risk_files,
            )
        )

    if len(files) > active_config.large_pr.changed_files:
        signals.append(
            RiskSignal(
                level=RiskLevel.MEDIUM,
                title="Large pull request",
                message="This pull request changes many files. Consider splitting or performing focused review.",
                files=[item.path for item in files],
            )
        )

    if total_changed_lines > active_config.large_pr.changed_lines:
        signals.append(
            RiskSignal(
                level=RiskLevel.MEDIUM,
                title="Large line change",
                message="This pull request changes many lines. Review scope, test coverage, and rollback safety.",
                files=[item.path for item in files],
            )
        )

    return signals
