from src.complexity import calculate_complexity
from src.duplicate_code import find_duplicate_code
from src.metrics import calculate_metrics
from src.naming import find_naming_violations
from src.unused_variables import find_unused_variables


def analyze_source(source: str) -> dict:
    """Performs static code analysis on Python source code by delegating to component analyzers."""
    if not isinstance(source, str):
        raise TypeError(f"Expected source as str, received {type(source).__name__}")

    return {
        "complexity": calculate_complexity(source),
        "unused_variables": find_unused_variables(source),
        "naming_violations": find_naming_violations(source),
        "duplicate_code": find_duplicate_code(source),
        "metrics": calculate_metrics(source),
    }