from app.main import add
from app.main import multiply

def test_add_success():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, 1) == 0

def test_multiply_success():
    assert multiply(2, 3) == 6

def test_multiply_negative():
    assert multiply(-1, 1) == -1