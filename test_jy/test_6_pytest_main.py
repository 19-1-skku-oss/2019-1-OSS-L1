import pytest

@pytest.mark.parametrize("test_input,expected", [
    ("3+5", 8),("6*8", 43),pytest.param("4*5", 20, marks=pytest.mark.xfail(strict=True)),
    pytest.param("6*9", 42, marks=pytest.mark.xfail),
])

def test_eval(test_input, expected):
    assert eval(test_input) == expected
