# Example 1 — List Unpacking

# python — Code Example
# numbers = [10, 20, 30]

# print(*numbers)


# Example 2 — Passing Arguments

# python — Code Example
# def add(a, b, c):
#     return a + b + c

# values = [1, 2, 3]

# print(add(*values))


# Example 3 — Dictionary Unpacking

# python — Code Example
# def create_user(name, age):
#     print(name, age)

# user = {
#     'name': 'Alice',
#     'age': 25
# }

# create_user(**user)


# Example 4 — Merge Lists

# python — Code Example
# list1 = [1, 2]
# list2 = [3, 4]

# combined = [*list1, *list2]

# Example 5 — Merge Dictionaries

# python — Code Example
# config = {**defaults, **user_settings}