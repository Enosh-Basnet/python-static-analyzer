import ast
import re


def is_snake_case(name: str) -> bool:
    """Checks if a name adheres to snake_case rules, ignoring placeholders and dunders."""
    if name == "_":
        return True
    if name.startswith("__") and name.endswith("__"):
        return True
    return bool(re.match(r"^[a-z_][a-z0-9_]*$", name))


def is_pascal_case(name: str) -> bool:
    """Checks if a name adheres to PascalCase rules."""
    return bool(re.match(r"^[A-Z][a-zA-Z0-9]*$", name))


class NamingVisitor(ast.NodeVisitor):
    """Traverses the AST to collect naming violations for functions, classes, and variables."""

    def __init__(self) -> None:
        self.functions: list[str] = []
        self.classes: list[str] = []
        self.variables: list[str] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if not is_snake_case(node.name) and node.name not in self.functions:
            self.functions.append(node.name)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        if not is_snake_case(node.name) and node.name not in self.functions:
            self.functions.append(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        if not is_pascal_case(node.name) and node.name not in self.classes:
            self.classes.append(node.name)
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, ast.Store):
            if not is_snake_case(node.id) and node.id not in self.variables:
                self.variables.append(node.id)
        self.generic_visit(node)


def find_naming_violations(source: str) -> dict[str, list[str]]:
    """Analyzes Python source code and returns naming violations grouped by category."""
    if not isinstance(source, str):
        raise TypeError(f"Expected source as str, received {type(source).__name__}")

    tree = ast.parse(source)
    visitor = NamingVisitor()
    visitor.visit(tree)

    results: dict[str, list[str]] = {}
    if visitor.functions:
        results["functions"] = visitor.functions
    if visitor.classes:
        results["classes"] = visitor.classes
    if visitor.variables:
        results["variables"] = visitor.variables

    return results