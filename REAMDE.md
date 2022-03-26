[![PyPI version](https://badge.fury.io/py/flake8-scream.svg)](https://badge.fury.io/py/flake8-scream)
[![Code on Github](https://img.shields.io/badge/Code-GitHub-brightgreen)](https://github.com/MartinThoma/flake8-scream)
[![Actions Status](https://github.com/MartinThoma/flake8-scream/workflows/Unit%20Tests/badge.svg)](https://github.com/MartinThoma/flake8-scream/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# flake8-scream

A [flake8](https://flake8.pycqa.org/en/latest/index.html) plugin that helps you simplify your code.

Linters which run in CI should not have false-positives as they quickly become
super annoying. For this reason, several rules were removed from
`flake8-simplify`. As those rules typically still provide some value, they are
now here.

`flake8-scream` does scream at you. Sometimes those are false-positives, hence
use the messages with care. And only use them once in a while. Definitely not
in CI.

## Installation

Install with `pip`:

```bash
pip install flake8-scream
```

## Usage

Just call `flake8 .` in your package or `flake your.py`:

```
$ flake8 .
./foo/__init__.py:690:12: SCR101 Multiple isinstance-calls which can be merged into a single call for variable 'other'
```

## Rules

* `SCR204`: Use 'a >= b' instead of 'not (a < b)' ([example](#SCR204))
* `SCR205`: Use 'a > b' instead of 'not (a <= b)' ([example](#SCR205))
* `SCR206`: Use 'a <= b' instead of 'not (a > b)' ([example](#SCR206))
* `SCR207`: Use 'a < b' instead of 'not (a <= b)' ([example](#SCR207))

### SCR204

```python
# Bad
not a < b

# Good
a >= b
```

### SCR205

```python
# Bad
not a <= b

# Good
a > b
```

### SCR206

```python
# Bad
not a > b

# Good
a <= b
```

### SCR207

```python
# Bad
not a >= b

# Good
a < b
```
