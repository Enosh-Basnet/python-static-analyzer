import ast


class ScopeCollector(ast.NodeVisitor):
    """Collects all scope-defining AST nodes (modules and functions)."""

    def __init__(self) -> None:
        self.scopes: list[tuple[str, ast.AST]] = []

    def visit_Module(self, node: ast.Module) -> None:
        self.scopes.append(("<module>", node))
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.scopes.append((node.name, node))
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.scopes.append((node.name, node))
        self.generic_visit(node)


class VariableScopeVisitor(ast.NodeVisitor):
    """Collects variable assignments and usages within a single scope level."""

    def __init__(self, root: ast.AST) -> None:
        self.root = root
        self.assigned: list[str] = []
        self.used: set[str] = set()

    def visit_Name(self, node: ast.Name) -> None:
        if node.id == "_":
            return

        if isinstance(node.ctx, ast.Store):
            if node.id not in self.assigned:
                self.assigned.append(node.id)
        elif isinstance(node.ctx, ast.Load):
            self.used.add(node.id)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node is self.root:
            self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        if node is self.root:
            self.generic_visit(node)


def find_unused_variables(source: str) -> dict[str, list[str]]:
    """Finds variables that are assigned but never read within the same lexical scope."""
    if not isinstance(source, str):
        raise TypeError(f"Expected source as str, received {type(source).__name__}")

    tree = ast.parse(source)
    collector = ScopeCollector()
    collector.visit(tree)

    results: dict[str, list[str]] = {}

    for scope_name, scope_node in collector.scopes:
        visitor = VariableScopeVisitor(scope_node)
        visitor.visit(scope_node)

        unused = [var for var in visitor.assigned if var not in visitor.used]
        if unused:
            results[scope_name] = unused

    return results