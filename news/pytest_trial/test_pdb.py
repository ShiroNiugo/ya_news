import pytest


pytestmark = pytest.mark.skip # Все тесты в этом файле будут пропущены


# test_pdb.py
def transform_list(x):
    x.append(1)
    x.extend([2, 3])
    return x


def test_list():
    a = []
    a = transform_list(a)
    a = [4] + a
    assert a == [1, 2, 3, 4]


@pytest.mark.skip
def test_will_be_skipped():
    assert True
