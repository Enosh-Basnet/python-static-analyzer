import ast


class DecisionPointVisitor(ast.NodeVisitor):
    """Traverses a function body AST to accumulate cyclomatic complexity decision points."""

    def __init__(self) -> None:
        self.complexity = 1

    def visit_If(self, node: ast.If) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_IfExp(self, node: ast.IfExp) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_comprehension(self, node: ast.comprehension) -> None:
        self.complexity += len(node.ifs)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        # Prevent nested function definitions from contributing to the parent function's score
        pass

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        # Prevent nested function definitions from contributing to the parent function's score
        pass


def calculate_complexity(source: str) -> dict[str, int]:
    """Calculates the cyclomatic complexity score for every function in the provided Python source code."""
    if not isinstance(source, str):
        raise TypeError(f"Expected source as str, received {type(source).__name__}")

    tree = ast.parse(source)
    results: dict[str, int] = {}

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            visitor = DecisionPointVisitor()
            for statement in node.body:
                visitor.visit(statement)
            results[node.name] = visitor.complexity

    return results