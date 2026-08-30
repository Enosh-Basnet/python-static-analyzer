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

    def visit_Match(self, node: ast.Match) -> None:
        for case in node.cases:
            if not self._is_default_case(case):
                self.complexity += 1
        self.generic_visit(node)

    @staticmethod
    def _is_default_case(case: ast.match_case) -> bool:
        return (
            isinstance(case.pattern, ast.MatchAs)
            and case.pattern.pattern is None
            and case.pattern.name is None
            and case.guard is None
        )

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        # Prevent nested function definitions from contributing to the parent function's score
        pass

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        # Prevent nested function definitions from contributing to the parent function's score
        pass


class FunctionCollector(ast.NodeVisitor):
    """Collects all functions and methods along with their scope-qualified names."""

    def __init__(self) -> None:
        self.class_stack: list[str] = []
        self.functions: list[tuple[str, ast.FunctionDef | ast.AsyncFunctionDef]] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.class_stack.append(node.name)
        self.generic_visit(node)
        self.class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        name = f"{'.'.join(self.class_stack)}.{node.name}" if self.class_stack else node.name
        self.functions.append((name, node))
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        name = f"{'.'.join(self.class_stack)}.{node.name}" if self.class_stack else node.name
        self.functions.append((name, node))
        self.generic_visit(node)


def calculate_complexity(source: str) -> dict[str, int]:
    """Calculates cyclomatic complexity for functions and methods in Python source code."""
    if not isinstance(source, str):
        raise TypeError(f"Expected source as str, received {type(source).__name__}")

    tree = ast.parse(source)
    collector = FunctionCollector()
    collector.visit(tree)

    results: dict[str, int] = {}
    for name, func_node in collector.functions:
        visitor = DecisionPointVisitor()
        for statement in func_node.body:
            visitor.visit(statement)
        results[name] = visitor.complexity

    return results