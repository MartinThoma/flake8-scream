import ast
import logging
import sys
from typing import Any, Generator, List, Tuple, Type

from flake8_simplify.utils import Call, UnaryOp

from flake8_scream.rules.ast_call import get_scr902, get_scr903
from flake8_scream.rules.ast_classdef import get_scr119
from flake8_scream.rules.ast_unary_op import (
    get_scr204,
    get_scr205,
    get_scr206,
    get_scr207,
)

logger = logging.getLogger(__name__)


if sys.version_info < (3, 8):  # pragma: no cover (<PY38)
    # Third party
    import importlib_metadata
else:  # pragma: no cover (PY38+)
    # Core Library
    import importlib.metadata as importlib_metadata


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors: List[Tuple[int, int, str]] = []

    def visit_UnaryOp(self, node_v: ast.UnaryOp) -> None:
        node = UnaryOp(node_v)
        self.errors += get_scr204(node)
        self.errors += get_scr205(node)
        self.errors += get_scr206(node)
        self.errors += get_scr207(node)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        self.errors += get_scr902(Call(node))
        self.errors += get_scr903(Call(node))
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.errors += get_scr119(node)
        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)  # type: ignore

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()

        # Add parent
        add_meta(self._tree)
        visitor.visit(self._tree)

        for line, col, msg in visitor.errors:
            yield line, col, msg, type(self)


def add_meta(root: ast.AST, level: int = 0) -> None:
    previous_sibling = None
    for node in ast.iter_child_nodes(root):
        if level == 0:
            node.parent = root  # type: ignore
        node.previous_sibling = previous_sibling  # type: ignore
        node.next_sibling = None  # type: ignore
        if previous_sibling:
            node.previous_sibling.next_sibling = node  # type: ignore
        previous_sibling = node
        for child in ast.iter_child_nodes(node):
            child.parent = node  # type: ignore
        add_meta(node, level=level + 1)
