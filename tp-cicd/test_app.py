from app import addition

def test_addition():
    assert addition(2, 3) == 5

def test_addition_zero():
    assert addition(10, 0) == 10
