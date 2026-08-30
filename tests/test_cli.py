from src.cli import main


# CLI-01
def test_valid_python_file_is_analyzed_successfully(tmp_path, capsys):
    source_file = tmp_path / "example.py"
    source_file.write_text(
        """
value = 10
print(value)
""",
        encoding="utf-8",
    )

    exit_code = main([str(source_file)])

    assert exit_code == 0


# CLI-02
def test_cli_outputs_all_analysis_sections(tmp_path, capsys):
    source_file = tmp_path / "example.py"
    source_file.write_text(
        """
def greet():
    print("Hello")
""",
        encoding="utf-8",
    )

    main([str(source_file)])
    captured = capsys.readouterr()

    assert "Python Static Code Analysis" in captured.out
    assert "Complexity" in captured.out
    assert "Unused Variables" in captured.out
    assert "Naming Violations" in captured.out
    assert "Duplicate Code" in captured.out
    assert "Code Metrics" in captured.out


# CLI-03
def test_missing_file_is_rejected(tmp_path, capsys):
    missing_file = tmp_path / "missing.py"

    exit_code = main([str(missing_file)])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "not found" in captured.err.lower()


# CLI-04
def test_directory_is_rejected(tmp_path, capsys):
    exit_code = main([str(tmp_path)])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "file" in captured.err.lower()


# CLI-05
def test_non_python_file_is_rejected(tmp_path, capsys):
    text_file = tmp_path / "example.txt"
    text_file.write_text("value = 10", encoding="utf-8")

    exit_code = main([str(text_file)])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert ".py" in captured.err.lower()


# CLI-06
def test_invalid_python_syntax_is_reported(tmp_path, capsys):
    source_file = tmp_path / "broken.py"
    source_file.write_text(
        "def broken_function(\n",
        encoding="utf-8",
    )

    exit_code = main([str(source_file)])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "syntax" in captured.err.lower()