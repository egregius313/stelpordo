import pytest

from .api_wrapper import BASE_URL, healthcheck

def pytest_sessionstart():
    try:
        up = healthcheck()
    except Exception:
        up = False
    if not up:
        pytest.exit(f"API healthcheck failed at {BASE_URL}/healthcheck")
