import pytest
from src.complexity import calculate_complexity


# NT-01
def test_function_without_decisions_has_complexity_one():
    source = """
def greet():
    print("Hello")
"""

    result = calculate_complexity(source)

    assert result["greet"] == 1


# NT-02
def test_function_with_one_if_has_complexity_two():
    source = """
def check_age(age):
    if age >= 18:
        return True
    return False
"""

    result = calculate_complexity(source)

    assert result["check_age"] == 2


# NT-03
def test_function_with_one_for_loop_has_complexity_two():
    source = """
def print_items(items):
    for item in items:
        print(item)
"""

    result = calculate_complexity(source)

    assert result["print_items"] == 2


# NT-04
def test_function_with_if_and_for_loop_has_complexity_three():
    source = """
def process_items(items):
    for item in items:
        if item > 0:
            print(item)
"""

    result = calculate_complexity(source)

    assert result["process_items"] == 3


# NT-05
def test_multiple_functions_receive_separate_complexity_scores():
    source = """
def greet():
    print("Hello")

def is_positive(number):
    if number > 0:
        return True
    return False
"""

    result = calculate_complexity(source)

    assert result["greet"] == 1
    assert result["is_positive"] == 2



# -------------------------
# Boundary Tests
# -------------------------

# BT-01
def test_empty_source_returns_empty_result():
    source = ""

    result = calculate_complexity(source)

    assert result == {}


# BT-02
def test_function_with_two_boolean_operands_has_complexity_two():
    source = """
def both_true(a, b):
    return a and b
"""

    result = calculate_complexity(source)

    assert result["both_true"] == 2


# BT-03
def test_function_with_three_boolean_operands_has_complexity_three():
    source = """
def all_true(a, b, c):
    return a and b and c
"""

    result = calculate_complexity(source)

    assert result["all_true"] == 3


# BT-04
def test_function_with_one_ternary_expression_has_complexity_two():
    source = """
def maximum(a, b):
    return a if a > b else b
"""

    result = calculate_complexity(source)

    assert result["maximum"] == 2


# BT-05
def test_if_elif_structure_counts_each_decision():
    source = """
def classify(number):
    if number > 0:
        return "positive"
    elif number < 0:
        return "negative"
    return "zero"
"""

    result = calculate_complexity(source)

    assert result["classify"] == 3


# -------------------------
# Invalid Input Tests
# -------------------------


# IT-01
def test_none_input_is_rejected():
    with pytest.raises(TypeError):
        calculate_complexity(None)


# IT-02
def test_integer_input_is_rejected():
    with pytest.raises(TypeError):
        calculate_complexity(123)


# IT-03
def test_list_input_is_rejected():
    with pytest.raises(TypeError):
        calculate_complexity(["def test():", "    pass"])


# IT-04
def test_invalid_python_syntax_raises_syntax_error():
    source = """
def broken_function(
"""

    with pytest.raises(SyntaxError):
        calculate_complexity(source)



# NT-06
def test_function_with_one_while_loop_has_complexity_two():
    source = """
def countdown(number):
    while number > 0:
        number -= 1
"""

    result = calculate_complexity(source)

    assert result["countdown"] == 2


# NT-07
def test_function_with_one_exception_handler_has_complexity_two():
    source = """
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
"""

    result = calculate_complexity(source)

    assert result["divide"] == 2


# NT-08
def test_comprehension_filter_increases_complexity():
    source = """
def positive_numbers(numbers):
    return [number for number in numbers if number > 0]
"""

    result = calculate_complexity(source)

    assert result["positive_numbers"] == 2


