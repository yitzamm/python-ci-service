from app.services import add, multiply


def test_add_success():
    # nosec: safe test code, no user input
    assert add(2, 3) == 5 


def test_add_negative():
    # nosec: safe test code, no user input
    assert add(-1, 1) == 0 


def test_multiply_success():
    # nosec: safe test code, no user input
    assert multiply(2, 3) == 6 


def test_multiply_negative():
    # nosec: safe test code, no user input
    assert multiply(-1, 1) == -1 
