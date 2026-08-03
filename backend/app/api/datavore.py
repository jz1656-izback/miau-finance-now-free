from app.api.datavore_shared import *
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/datavore", tags=["Datavore"])

# Import sub-modules to register routes on this router
from app.api import datavore_map  # noqa: F401,E402
from app.api import datavore_market  # noqa: F401,E402
from app.api import datavore_calc  # noqa: F401,E402
from app.api import datavore_screener  # noqa: F401,E402
from app.api import datavore_macro  # noqa: F401,E402
from app.api import datavore_ticker  # noqa: F401,E402
from app.api import datavore_globe  # noqa: F401,E402
