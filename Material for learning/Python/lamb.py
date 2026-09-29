# lambda parameters: expression

# lambda x: x * x

# cube= lambda x:x**3
# print(cube(3))

# square = lambda x: x * x

# print(square(5))

# students = [
#     ('Alice', 88),
#     ('Bob', 95),
#     ('Charlie', 72)
# ]

# sorted_students = sorted(
#     students,
#     key=lambda student: student[1]
# )

# print(sorted_students)


# multiply = lambda x, y: x * y

# print(multiply(3, 4))


# numbers = [1,2,3,4,5,6,7,8,9,10]

# result = list(
#     filter(
#         lambda x: x % 2 == 0,
#         numbers
#     )
# )

# print(result)

# employees = [
#     {'name': 'Alice', 'salary': 70000},
#     {'name': 'Bob', 'salary': 50000},
#     {'name': 'Charlie', 'salary': 90000}
# ]

# highest_paid = sorted(
#     employees,
#     key=lambda employee: employee['salary'],
    
# )

# print(highest_paid)


# f = lambda x: x + 1
# print(f(5))

# sorted([3,1,2], key=lambda x: -x)

# Basic lambda
func = lambda x: expression

# Multiple arguments
func = lambda x, y: expression

# Conditional
func = lambda x: value1 if condition else value2

# Sort by property
sorted(data, key=lambda x: expression)

# Descending
sorted(
    data,
    key=lambda x: expression,
    reverse=True
)

# Dictionary by value
sorted(
    d.items(),
    key=lambda x: x[1]
)

# Dictionary by value descending
sorted(
    d.items(),
    key=lambda x: x[1],
    reverse=True
)

# Value descending + key ascending
sorted(
    d.items(),
    key=lambda x: (-x[1], x[0])
)

# Map
list(
    map(lambda x: expression, data)
)

# Filter
list(
    filter(lambda x: condition, data)
)

# Maximum by property
max(
    data,
    key=lambda x: expression
)

# Minimum by property
min(
    data,
    key=lambda x: expression
)