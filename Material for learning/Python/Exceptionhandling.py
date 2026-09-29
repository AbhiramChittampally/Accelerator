#most basic example
def divide_numbers(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Safety Net Caught It: You cannot divide by zero!")
        return None
    else:
        print("Math successful!")
        return result

# Execution
print(divide_numbers(10, 2))  # Works fine
print(divide_numbers(10, 0))  # Caught by the safety net! Program doesn't crash.