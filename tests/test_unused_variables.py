from src.unused_variables import find_unused_variables


# NT-09
def test_module_level_unused_variable_is_reported():
    source = """
unused_value = 10
print("Hello")
"""

    result = find_unused_variables(source)

    assert result["<module>"] == ["unused_value"]


# NT-10
def test_used_variable_is_not_reported():
    source = """
value = 10
print(value)
"""

    result = find_unused_variables(source)

    assert result == {}


# NT-11
def test_unused_local_variable_inside_function_is_reported():
    source = """
def calculate():
    temp = 10
    return 5
"""

    result = find_unused_variables(source)

    assert result["calculate"] == ["temp"]


# NT-12
def test_only_unused_variable_is_reported_when_other_variable_is_used():
    source = """
def calculate():
    used_value = 10
    unused_value = 20
    return used_value
"""

    result = find_unused_variables(source)

    assert result["calculate"] == ["unused_value"]


# NT-13
def test_variables_are_analyzed_independently_across_scopes():
    source = """
module_value = 10

def process():
    local_value = 20
    return 1
"""

    result = find_unused_variables(source)

    assert result["<module>"] == ["module_value"]
    assert result["process"] == ["local_value"]