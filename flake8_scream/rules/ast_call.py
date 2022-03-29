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


def get_scr903(node: Call) -> List[Tuple[int, int, str]]:
    """Find bare numeric function arguments."""
    RULE = "SCR903 Use keyword-argument instead of magic number for '{func}'"
    acceptable_magic_numbers = (0, 1, 2)
    errors: List[Tuple[int, int, str]] = []

    if isinstance(node.func, ast.Attribute):
        call_name = node.func.attr
    elif isinstance(node.func, ast.Name):
        call_name = node.func.id
    else:
        logger.debug(f"Unknown call type: {type(node.func)}")
        return errors

    nb_args = len(node.args)
    if nb_args <= 1 or call_name.startswith("_"):
        return errors

    functions_any_arg = ["partial", "min", "max", "minimum", "maximum"]
    functions_1_arg = ["sqrt", "sleep", "hideColumn"]
    functions_2_args = [
        "arange",
        "uniform",
        "zeros",
        "percentile",
        "setColumnWidth",
        "float_power",
        "power",
        "pow",
        "float_power",
        "binomial",
    ]
    if any(
        (
            call_name in functions_any_arg,
            call_name in functions_1_arg and nb_args == 1,
            call_name in functions_2_args and nb_args == 2,
            call_name in ["linspace"] and nb_args == 3,
            "color" in call_name.lower() and nb_args in [3, 4],
            "point" in call_name.lower() and nb_args in [2, 3],
        )
    ):
        return errors

    has_bare_int = any(
        isinstance(call_arg, ast.Num)
        and call_arg.n not in acceptable_magic_numbers
        for call_arg in node.args
    )

    is_setter = call_name.lower().startswith("set") and nb_args <= 2
    is_exception = isinstance(node.func, ast.Name) and node.func.id == "range"
    is_exception = is_exception or (
        isinstance(node.func, ast.Attribute)
        and node.func.attr
        in [
            "get",
            "insert",
        ]
    )
    if has_bare_int and not (is_exception or is_setter):
        source = to_source(node)
        errors.append((node.lineno, node.col_offset, RULE.format(func=source)))
    return errors
