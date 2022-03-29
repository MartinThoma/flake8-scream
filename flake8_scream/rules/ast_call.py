import ast
import logging
from typing import List, Tuple

from flake8_simplify.utils import Call, to_source

logger = logging.getLogger(__name__)


def get_scr902(node: Call) -> List[Tuple[int, int, str]]:
    """Find bare boolean function arguments."""
    RULE = "SCR902 Use keyword-argument instead of magic boolean for '{func}'"
    errors: List[Tuple[int, int, str]] = []

    if isinstance(node.func, ast.Attribute):
        call_name = node.func.attr
    elif isinstance(node.func, ast.Name):
        call_name = node.func.id
    else:
        logger.debug(f"Unknown call type: {type(node.func)}")
        return errors

    nb_args = len(node.args)

    if call_name in [
        "partial",
        "min",
        "max",
        # Common positional-only arguments:
        "getattr",
        "setattr",
        "pop",  # if its a dictionary
    ] or call_name.startswith("_"):
        return errors

    has_bare_bool = any(
        isinstance(call_arg, (ast.Constant, ast.NameConstant))
        and (call_arg.value is True or call_arg.value is False)
        for call_arg in node.args
    )

    is_setter = call_name.lower().startswith("set") and nb_args <= 2
    is_exception = isinstance(node.func, ast.Attribute) and node.func.attr in [
        "get"
    ]
    if has_bare_bool and not (is_exception or is_setter):
        source = to_source(node)
        errors.append((node.lineno, node.col_offset, RULE.format(func=source)))
    return errors
