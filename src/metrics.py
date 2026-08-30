import ast


def calculate_metrics(source: str) -> dict[str, int]:
    """Calculates code metrics (logical lines, functions, classes, imports) for Python source code."""
    if not isinstance(source, str):
        raise TypeError(f"Expected source as str, received {type(source).__name__}")

    tree = ast.parse(source)

    logical_lines = sum(
        1
        for line in source.splitlines()
        if line.strip() and not line.strip().startswith("#")
    )

    functions = 0
    classes = 0
    imports = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions += 1
        elif isinstance(node, ast.ClassDef):
            classes += 1
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            imports += 1

    return {
        "logical_lines": logical_lines,
        "functions": functions,
        "classes": classes,
        "imports": imports,
    }