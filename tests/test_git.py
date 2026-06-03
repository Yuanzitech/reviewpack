from reviewpack.git import parse_numstat, parse_numstat_line


def test_parse_numstat_line_for_text_file() -> None:
    changed_file = parse_numstat_line("12\t3\tsrc/app.py")

    assert changed_file is not None
    assert changed_file.path == "src/app.py"
    assert changed_file.additions == 12
    assert changed_file.deletions == 3


def test_parse_numstat_line_for_binary_file() -> None:
    changed_file = parse_numstat_line("-\t-\tassets/logo.png")

    assert changed_file is not None
    assert changed_file.path == "assets/logo.png"
    assert changed_file.additions == 0
    assert changed_file.deletions == 0


def test_parse_numstat_line_returns_none_for_invalid_line() -> None:
    assert parse_numstat_line("invalid") is None


def test_parse_numstat_parses_multiple_files() -> None:
    text = "\n".join(
        [
            "12\t3\tsrc/app.py",
            "5\t0\ttests/test_app.py",
            "-\t-\tassets/logo.png",
        ]
    )

    files = parse_numstat(text)

    assert len(files) == 3
    assert files[0].path == "src/app.py"
    assert files[1].path == "tests/test_app.py"
    assert files[2].path == "assets/logo.png"
