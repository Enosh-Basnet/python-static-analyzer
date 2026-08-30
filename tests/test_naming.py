import pytest

from src.naming import find_naming_violations

# Normal Behavior Tests for Naming Violations
# NT-14
def test_valid_function_name_has_no_violation():
    source = """
def calculate_total():
    return 10
"""

    assert find_naming_violations(source) == {}


# NT-15
def test_invalid_function_name_is_reported():
    source = """
def CalculateTotal():
    return 10
"""

    result = find_naming_violations(source)

    assert result["functions"] == ["CalculateTotal"]


# NT-16
def test_valid_class_name_has_no_violation():
    source = """
class CodeAnalyzer:
    pass
"""

    assert find_naming_violations(source) == {}


# NT-17
def test_invalid_class_name_is_reported():
    source = """
class code_analyzer:
    pass
"""

    result = find_naming_violations(source)

    assert result["classes"] == ["code_analyzer"]


# NT-18
def test_invalid_variable_name_is_reported():
    source = """
TotalValue = 10
"""

    result = find_naming_violations(source)

    assert result["variables"] == ["TotalValue"]



    #Boundary Tests for Naming Violations
    # BT-11
def test_single_lowercase_character_variable_is_valid():
    source = "x = 10"

    assert find_naming_violations(source) == {}


# BT-12
def test_variable_with_numbers_is_valid():
    source = "value2 = 10"

    assert find_naming_violations(source) == {}


# BT-13
def test_placeholder_underscore_is_ignored():
    source = "_ = 10"

    assert find_naming_violations(source) == {}


# BT-14
def test_dunder_method_is_valid():
    source = """
class Example:
    def __init__(self):
        self.value = 10
"""

    assert find_naming_violations(source) == {}


    ## Invalid Input Tests for Naming Violations

    # IT-09
def test_none_input_is_rejected():
    with pytest.raises(TypeError):
        find_naming_violations(None)


# IT-10
def test_integer_input_is_rejected():
    with pytest.raises(TypeError):
        find_naming_violations(123)


# IT-11
def test_list_input_is_rejected():
    with pytest.raises(TypeError):
        find_naming_violations(["value = 10"])


# IT-12
def test_invalid_python_syntax_raises_syntax_error():
    source = """
def broken_function(
"""

    with pytest.raises(SyntaxError):
        find_naming_violations(source)