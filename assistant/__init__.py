"""Practice sales assistant, build v0.3, from the ProoV project "AI Agent Security".

A hypothetical scenario. This is not IBM's real assistant or real systems.
Every company, person and deal in this package is invented.
"""

from .agent import Request, Result, handle
from .crm import Lead
from .model import Action, ObedientModel

__version__ = "0.3"
__all__ = ["Action", "Lead", "ObedientModel", "Request", "Result", "handle"]
