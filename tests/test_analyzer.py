import pytest

from src.analyzer import analyze_source


# INT-01
def test_analyzer_returns_all_analysis_categories():
    source = """
value = 10
print(value)
"""

    result = analyze_source(source)

    assert set(result.keys()) == {
        "complexity",
        "unused_variables",
        "naming_violations",
        "duplicate_code",
        "metrics",
    }


# INT-02
def test_analyzer_combines_results_from_multiple_components():
    source = """
import os

BadVariable = 10

def check_value(value):
    if value > 0:
        return value
    return 0
"""

    result = analyze_source(source)

    assert result["complexity"]["check_value"] == 2
    assert "BadVariable" in result["naming_violations"]["variables"]
    assert result["metrics"]["functions"] == 1
    assert result["metrics"]["imports"] == 1


# INT-03
def test_analyzer_reports_unused_variable():
    source = """
unused_value = 10
print("Hello")
"""

    result = analyze_source(source)

    assert result["unused_variables"]["<module>"] == ["unused_value"]


# INT-04
def test_valid_empty_source_returns_complete_empty_analysis():
    result = analyze_source("")

    assert result["complexity"] == {}
    assert result["unused_variables"] == {}
    assert result["naming_violations"] == {}
    assert result["duplicate_code"] == []

    assert result["metrics"] == {
        "logical_lines": 0,
        "functions": 0,
        "classes": 0,
        "imports": 0,
    }


# INT-05
def test_non_string_source_is_rejected():
    with pytest.raises(TypeError):
        analyze_source(None)


# INT-06
def test_invalid_python_syntax_is_rejected():
    source = """
def broken_function(
"""

    with pytest.raises(SyntaxError):
        analyze_source(source)