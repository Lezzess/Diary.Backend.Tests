import pytest


@pytest.mark.parametrize("test_argument", {2, 4, 6, 8, 10})
def test_tutorial(test_argument):
    assert test_argument % 2 == 0
