from app.services import add, multiply


def test_add_success():
    assert add(2, 3) == 5  # nosec: safe test code


def test_add_negative():
    assert add(-1, 1) == 0  # nosec: safe test code


def test_multiply_success():
    assert multiply(2, 3) == 6  # nosec: safe test code


def test_multiply_negative():
    assert multiply(-1, 1) == -1  # nosec: safe test code
