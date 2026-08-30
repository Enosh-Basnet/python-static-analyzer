## NORMAL BEHAVIOUR TESTS
import pytest

from src.metrics import calculate_metrics


# NT-24
def test_counts_single_function():
    source = """
def greet():
    return "Hello"
"""

    result = calculate_metrics(source)

    assert result["functions"] == 1


# NT-25
def test_counts_classes():
    source = """
class First:
    pass

class Second:
    pass
"""

    result = calculate_metrics(source)

    assert result["classes"] == 2


# NT-26
def test_counts_import_statements():
    source = """
import os
from pathlib import Path
"""

    result = calculate_metrics(source)

    assert result["imports"] == 2


# NT-27
def test_counts_combined_code_metrics():
    source = """
import os

class Calculator:
    def add(self, a, b):
        return a + b

def greet():
    return "Hello"
"""

    result = calculate_metrics(source)

    assert result["functions"] == 2
    assert result["classes"] == 1
    assert result["imports"] == 1


# NT-28
def test_counts_async_function():
    source = """
async def fetch_data():
    return None
"""

    result = calculate_metrics(source)

    assert result["functions"] == 1


## BOUNDARY TESTS
# BT-20
def test_empty_source_returns_zero_metrics():
    result = calculate_metrics("")

    assert result == {
        "logical_lines": 0,
        "functions": 0,
        "classes": 0,
        "imports": 0,
    }


# BT-21
def test_blank_and_comment_lines_are_not_counted():
    source = """
# comment

value = 10

# another comment
"""

    result = calculate_metrics(source)

    assert result["logical_lines"] == 1


# BT-22
def test_single_code_line_counts_as_one_logical_line():
    result = calculate_metrics("value = 10")

    assert result["logical_lines"] == 1


# BT-23
def test_multiple_names_in_one_import_statement_count_as_one_import():
    source = """
import os, sys
"""

    result = calculate_metrics(source)

    assert result["imports"] == 1


## INVALID INPUT TESTS
# IT-17
def test_none_input_is_rejected():
    with pytest.raises(TypeError):
        calculate_metrics(None)


# IT-18
def test_integer_input_is_rejected():
    with pytest.raises(TypeError):
        calculate_metrics(123)


# IT-19
def test_invalid_python_syntax_raises_syntax_error():
    source = """
def broken_function(
"""

    with pytest.raises(SyntaxError):
        calculate_metrics(source)



