import ast
from typing import Set

from flake8_scream import Plugin


def _results(code: str) -> Set[str]:
    """Apply the plugin to the given code."""
    tree = ast.parse(code)
    plugin = Plugin(tree)
    return {f"{line}:{col} {msg}" for line, col, msg, _ in plugin.run()}
