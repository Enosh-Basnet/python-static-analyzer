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
        self.used_after_assign: set[str] = set()

    def _record_read(self, name: str) -> None:
        if name == "_":
            return
        if name in self.assigned:
            self.used_after_assign.add(name)

    def _record_write(self, name: str) -> None:
        if name == "_":
            return
        if name not in self.assigned:
            self.assigned.append(name)

    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, ast.Load):
            self._record_read(node.id)
        elif isinstance(node.ctx, ast.Store):
            self._record_write(node.id)

    def visit_Assign(self, node: ast.Assign) -> None:
        # Evaluate RHS value expression before LHS target assignments
        self.visit(node.value)
        for target in node.targets:
            self.visit(target)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if node.value:
            self.visit(node.value)
        self.visit(node.annotation)
        self.visit(node.target)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        # Augmented assignment reads target variable first, evaluates RHS, then writes target
        if isinstance(node.target, ast.Name):
            self._record_read(node.target.id)
        else:
            self.visit(node.target)

        self.visit(node.value)

        if isinstance(node.target, ast.Name):
            self._record_write(node.target.id)

    def visit_For(self, node: ast.For) -> None:
        self.visit(node.iter)
        self.visit(node.target)
        for stmt in node.body:
            self.visit(stmt)
        for stmt in node.orelse:
            self.visit(stmt)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self.visit(node.iter)
        self.visit(node.target)
        for stmt in node.body:
            self.visit(stmt)
        for stmt in node.orelse:
            self.visit(stmt)

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

        unused = [var for var in visitor.assigned if var not in visitor.used_after_assign]
        if unused:
            results[scope_name] = unused

    return results