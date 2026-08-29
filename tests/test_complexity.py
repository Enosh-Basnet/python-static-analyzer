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