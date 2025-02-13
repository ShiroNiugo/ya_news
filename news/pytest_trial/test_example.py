# test_example.py
import pytest
from time import sleep


@pytest.fixture
def give_me_a_string():
    return 'Какой чудесный день!'


# Новая фикстура возвращает список со строкой из первой фикстуры.
@pytest.fixture
def pack_to_list(give_me_a_string):  # Фикстура может вызывать другие фикстуры.
    return [give_me_a_string]


# Тестовая функция использует обе фикстуры и проверяет их содержимое.
def test_string_fixture(pack_to_list, give_me_a_string):
    assert pack_to_list == [give_me_a_string]


def one_more(x):
    return x + 1


@pytest.mark.parametrize(
    'input_arg, expected_result',  # Названия аргументов, передаваемых в тест.
    [
        (4, 5),
        pytest.param(3, 5, marks=pytest.mark.xfail)
    ],  # Список кортежей со значениями аргументов.
    ids=['First parameter', 'Second parameter',]  # Названия тестов.
)
def test_one_more(input_arg, expected_result):  # Те же параметры, что и в декораторе.
    assert one_more(input_arg) == expected_result


def get_sort_list(str):
    new_list = sorted(str.split(', '))
    return new_list


def test_sort():
    """Тестируем функцию get_sort_list()."""    
    result = get_sort_list('Яша, Саша, Маша, Даша')
    assert result == ['Даша', 'Маша', 'Саша', 'Яша']


@pytest.mark.slow
def test_type():
    """Тестируем тип данных, возвращаемых из get_sort_list()."""
    sleep(3)
    # Провальный тест:
    # ожидаем число, но вернётся список.
    result = get_sort_list('Яша, Саша, Маша, Даша')
    assert isinstance(result, int)


def cartesian_product(a, b):
    return a * b


@pytest.mark.parametrize('x', [1, 2])
@pytest.mark.parametrize('y', ['one', 'two'])
def test_cartesian_product(x, y):
    assert cartesian_product(x, y) is not None
