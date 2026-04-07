import copy
import os
import sys

import pytest
from fastapi.testclient import TestClient

# Add the src directory to the import path so tests can import the application module.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")
sys.path.insert(0, SRC_DIR)

import app as app_module  # noqa: E402

INITIAL_ACTIVITIES = copy.deepcopy(app_module.activities)

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities state before each test."""
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(INITIAL_ACTIVITIES))
    yield

@pytest.fixture
def client():
    return TestClient(app_module.app)
