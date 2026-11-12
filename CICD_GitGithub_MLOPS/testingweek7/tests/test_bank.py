
import pytest

from src.bank import withdraw


@pytest.fixture
def account_balance():
    return 1000


@pytest.mark.smoke
def test_basic_account_withdrawal():
    assert withdraw(1000, 100) == 900

@pytest.mark.parametrize(
    "balance, amount, expected",
    [
        (1000, 200, 800),
        (1000, 300, 700),
        (500, 100, 400),
        (2000, 500, 1500),
        (1000, 1000, 0),
    ]
)
def test_successful_withdrawal(balance, amount, expected):
    assert withdraw(balance, amount) == expected


def test_withdrawal_exceeds_balance(account_balance):
    with pytest.raises(ValueError):
        withdraw(account_balance, 1500)


def test_zero_withdrawal(account_balance):
    with pytest.raises(ValueError):
        withdraw(account_balance, 0)


def test_negative_withdrawal(account_balance):
    with pytest.raises(ValueError):
        withdraw(account_balance, -200)






@pytest.mark.skip(reason="Feature temporarily disabled")
def test_international_withdrawal():
    assert withdraw(1000, 100) == 900


@pytest.mark.skipif(
    __import__("sys").platform == "win32",
    reason="This test is intended for non-Windows systems"
)
def test_linux_specific_behavior():
    assert withdraw(1000, 100) == 900


@pytest.mark.xfail(reason="Known issue: overdraft support is not implemented")
def test_overdraft_support():
    assert withdraw(1000, 1500) == -500
