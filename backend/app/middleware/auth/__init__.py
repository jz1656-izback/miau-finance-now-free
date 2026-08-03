"""Auth middleware — re-exports from auth/base.py for backwards compatibility.

The original auth.py was converted to auth/base.py when the PQC JWT module
(auth/jwt_pqc.py) was added. All public symbols are re-exported here so
existing imports like ``from app.middleware.auth import get_current_user``
continue to work.
"""
from app.middleware.auth.base import *  # noqa: F401, F403
