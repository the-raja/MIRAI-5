"""Root conftest for pytest to set PYTHONPATH."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
