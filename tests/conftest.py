import importlib

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client():
    # Reload module to reset in-memory state between tests
    importlib.reload(app_module)
    return TestClient(app_module.app)
