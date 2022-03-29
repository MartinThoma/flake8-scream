[![PyPI version](https://badge.fury.io/py/flake8-scream.svg)](https://badge.fury.io/py/flake8-scream)
[![Code on Github](https://img.shields.io/badge/Code-GitHub-brightgreen)](https://github.com/MartinThoma/flake8-scream)
[![Actions Status](https://github.com/MartinThoma/flake8-scream/workflows/Unit%20Tests/badge.svg)](https://github.com/MartinThoma/flake8-scream/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# flake8-scream

A [flake8](https://flake8.pycqa.org/en/latest/index.html) plugin that helps you scream your code.


## Rules

* [`SCR119`](https://github.com/MartinThoma/flake8-simplify/issues/37) ![](https://shields.io/badge/-legacyfix-inactive): Use dataclasses for data containers ([example](#SCR119))
* [`SCR902`](https://github.com/MartinThoma/flake8-simplify/issues/125): Use keyword-argument instead of magic boolean ([example](#SIM902))

## Disabling Rules

You might have good reasons to
[ignore some flake8 rules](https://flake8.pycqa.org/en/3.1.1/user/ignoring-errors.html).
To do that, use the standard Flake8 configuration. For example, within the `setup.cfg` file:

```python
[flake8]
ignore = SCR106, SCR113, SCR119, SCR9
```

## Examples

### SCR119

Dataclasses were introduced with [PEP 557](https://www.python.org/dev/peps/pep-0557/)
in Python 3.7. The main reason not to use dataclasses is to support legacy Python versions.

Dataclasses create a lot of the boilerplate code for you:

* `__init__`
* `__eq__`
* `__hash__`
* `__str__`
* `__repr__`

A lot of projects use them:

* [black](https://github.com/psf/black/blob/master/src/black/__init__.py#L1472)

### SCR902

```python
# Bad
foo(False)
bar(True)

# Good
foo(verbose=False)
bar(enable_magic=True)
```

The false-positives that are currentl not possible to fix are in positional-only
arguments. There is no way to determine in the AST given by Flake8 if a function
has positional-only arguments.
