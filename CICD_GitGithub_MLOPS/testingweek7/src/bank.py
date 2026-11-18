# def withdraw(balance, amount):
#     if amount <= 0:
#         raise ValueError("Withdrawal amount must be positive")

#     if amount > balance:
#         raise ValueError("Insufficient funds")

#     return balance - amount


def withdraw(balance: float, amount: float) -> float:
    if amount <= 0:
        raise ValueError("Withdrawal amount must be positive")

    if amount > balance:
        raise ValueError("Insufficient funds")

    return balance - amount
