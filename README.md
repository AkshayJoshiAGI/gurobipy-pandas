# gurobipy-pandas: Convenience wrapper for building optimization models from pandas data

-----

**This package is in beta development and not supported. The API may change without warning.**

-----

[![PyPI - Version](https://img.shields.io/pypi/v/gurobipy-pandas.svg)](https://pypi.org/project/gurobipy-pandas)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gurobipy-pandas.svg)](https://pypi.org/project/gurobipy-pandas)

-----

## Features

`gurobipy-pandas` allows users to:

- create gurobipy variables tied to the index of a series or dataframe
- construct constraints row-wise using algebraic expressions
- read model solutions and constraint slacks natively as pandas series

## Installation

```console
pip install gurobipy-pandas
```

## Dependencies

- [gurobipy: Python modelling interface for the Gurobi Optimizer](https://pypi.org/project/gurobipy/)
- [pandas: powerful Python data analysis toolkit](https://github.com/pandas-dev/pandas)

## Documentation

Full documentation for `gurobipy-pandas` is hosted on [readthedocs](https://gurobi-optimization-gurobipy-pandas.readthedocs-hosted.com/en/v0.1.0b2)

## License

`gurobipy-pandas` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
