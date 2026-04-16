from __future__ import annotations

import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent

# Vercel can execute this file with Root Directory set to `app`. Adding the
# parent directory lets Python resolve the `app` package consistently both on
# Vercel and in local development.
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from app.main import app
