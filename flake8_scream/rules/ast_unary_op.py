import ast
from typing import List, Tuple

from flake8_simplify.utils import UnaryOp, is_exception_check, to_source


def get_scr204(node: UnaryOp) -> List[Tuple[int, int, str]]:
    """Get a list of all calls of the type "not (a < b)"."""
    SCR204 = "SCR204 Use '{a} >= {b}' instead of 'not ({a} < {b})'"
    errors: List[Tuple[int, int, str]] = []
    if (
        (
            not isinstance(node.op, ast.Not)
            or not isinstance(node.operand, ast.Compare)
            or len(node.operand.ops) != 1
            or not isinstance(node.operand.ops[0], ast.Lt)
        )
        or isinstance(node.parent, ast.If)
        and is_exception_check(node.parent)
    ):
        return errors
    comparison = node.operand
    left = to_source(comparison.left)
    right = to_source(comparison.comparators[0])
    errors.append((node.lineno, node.col_offset, SCR204.format(a=left, b=right)))
    return errors


def get_scr205(node: UnaryOp) -> List[Tuple[int, int, str]]:
    """Get a list of all calls of the type "not (a <= b)"."""
    SCR205 = "SCR205 Use '{a} > {b}' instead of 'not ({a} <= {b})'"
    errors: List[Tuple[int, int, str]] = []
    if (
        (
            not isinstance(node.op, ast.Not)
            or not isinstance(node.operand, ast.Compare)
            or len(node.operand.ops) != 1
            or not isinstance(node.operand.ops[0], ast.LtE)
        )
        or isinstance(node.parent, ast.If)
        and is_exception_check(node.parent)
    ):
        return errors
    comparison = node.operand
    left = to_source(comparison.left)
    right = to_source(comparison.comparators[0])
    errors.append((node.lineno, node.col_offset, SCR205.format(a=left, b=right)))
    return errors


def get_scr206(node: UnaryOp) -> List[Tuple[int, int, str]]:
    """Get a list of all calls of the type "not (a > b)"."""
    SCR206 = "SCR206 Use '{a} <= {b}' instead of 'not ({a} > {b})'"
    errors: List[Tuple[int, int, str]] = []
    if (
        (
            not isinstance(node.op, ast.Not)
            or not isinstance(node.operand, ast.Compare)
            or len(node.operand.ops) != 1
            or not isinstance(node.operand.ops[0], ast.Gt)
        )
        or isinstance(node.parent, ast.If)
        and is_exception_check(node.parent)
    ):
        return errors
    comparison = node.operand
    left = to_source(comparison.left)
    right = to_source(comparison.comparators[0])
    errors.append((node.lineno, node.col_offset, SCR206.format(a=left, b=right)))
    return errors


def get_scr207(node: UnaryOp) -> List[Tuple[int, int, str]]:
    """Get a list of all calls of the type "not (a >= b)"."""
    SCR207 = "SCR207 Use '{a} < {b}' instead of 'not ({a} >= {b})'"
    errors: List[Tuple[int, int, str]] = []
    if (
        (
            not isinstance(node.op, ast.Not)
            or not isinstance(node.operand, ast.Compare)
            or len(node.operand.ops) != 1
            or not isinstance(node.operand.ops[0], ast.GtE)
        )
        or isinstance(node.parent, ast.If)
        and is_exception_check(node.parent)
    ):
        return errors
    comparison = node.operand
    left = to_source(comparison.left)
    right = to_source(comparison.comparators[0])
    errors.append((node.lineno, node.col_offset, SCR207.format(a=left, b=right)))
    return errors
