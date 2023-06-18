__version__ = "1.0.0"

# Import public API functions
from gurobipy_pandas.api import add_vars  # noqa: F401
from gurobipy_pandas.api import add_constrs  # noqa: F401
from gurobipy_pandas.api import set_interactive  # noqa: F401

# Import accessors module to register accessors.
import gurobipy_pandas.accessors  # noqa: F401
