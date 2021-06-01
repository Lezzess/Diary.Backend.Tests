import pytest

from core.web import HttpRequest


@pytest.fixture(scope="function")
def http() -> HttpRequest:
    return HttpRequest()
