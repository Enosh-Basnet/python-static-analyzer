import pytest

from src.duplicate_code import find_duplicate_code

# -------------------------
# Normal Behaviour Tests
# -------------------------


# NT-19
def test_exact_three_line_duplicate_is_detected():
    source = """
a = 10
b = 20
print(a + b)

x = 5

a = 10
b = 20
print(a + b)
"""

    result = find_duplicate_code(source)

    assert len(result) == 1
    assert result[0]["block"] == (
        "a = 10",
        "b = 20",
        "print(a + b)",
    )
    assert len(result[0]["occurrences"]) == 2


# NT-20
def test_unique_code_returns_no_duplicates():
    source = """
a = 10
b = 20
print(a + b)

x = 30
y = 40
print(x * y)
"""

    assert find_duplicate_code(source) == []


# NT-21
def test_duplicate_block_occurring_three_times_is_detected():
    source = """
a = 1
b = 2
print(a + b)

a = 1
b = 2
print(a + b)

a = 1
b = 2
print(a + b)
"""

    result = find_duplicate_code(source)

    assert len(result) == 1
    assert len(result[0]["occurrences"]) == 3


# NT-22
def test_leading_and_trailing_whitespace_is_ignored():
    source = """
a = 1
b = 2
print(a + b)

    a = 1
    b = 2
    print(a + b)
"""

    result = find_duplicate_code(source)

    assert len(result) == 1


# NT-23
def test_blank_and_comment_only_lines_do_not_break_duplicate_block():
    source = """
a = 1

# first comment
b = 2
print(a + b)

a = 1
# another comment

b = 2
print(a + b)
"""

    result = find_duplicate_code(source)

    assert len(result) == 1
    assert result[0]["block"] == (
        "a = 1",
        "b = 2",
        "print(a + b)",
    )

# -------------------------
# Boundary Tests
# -------------------------


# BT-15
def test_two_line_duplicate_is_not_reported():
    source = """
a = 1
b = 2

a = 1
b = 2
"""

    assert find_duplicate_code(source) == []


# BT-16
def test_exactly_three_lines_meets_default_threshold():
    source = """
a = 1
b = 2
c = 3

a = 1
b = 2
c = 3
"""

    result = find_duplicate_code(source)

    assert len(result) == 1


# BT-17
def test_empty_source_returns_no_duplicates():
    assert find_duplicate_code("") == []


# BT-18
def test_single_block_without_repetition_is_not_duplicate():
    source = """
a = 1
b = 2
c = 3
"""

    assert find_duplicate_code(source) == []


# BT-19
def test_custom_four_line_threshold_requires_four_lines():
    source = """
a = 1
b = 2
c = 3

a = 1
b = 2
c = 3
"""

    assert find_duplicate_code(source, min_block_size=4) == []


# -------------------------
# Invalid Input Tests
# -------------------------


# IT-13
def test_none_source_is_rejected():
    with pytest.raises(TypeError):
        find_duplicate_code(None)


# IT-14
def test_integer_source_is_rejected():
    with pytest.raises(TypeError):
        find_duplicate_code(123)


# IT-15
def test_non_integer_block_size_is_rejected():
    with pytest.raises(TypeError):
        find_duplicate_code("a = 1", min_block_size="3")


# IT-16
def test_block_size_below_minimum_is_rejected():
    with pytest.raises(ValueError):
        find_duplicate_code("a = 1", min_block_size=2)