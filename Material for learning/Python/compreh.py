
#list comprehension
# numbers = [1, 2, 3, 4, 5]
# squares = [x * x for x in numbers]
# print(squares)

# numbers = range(10)
# even_numbers = [x for x in numbers if x % 2 == 0]
# print(even_numbers)

# [x for x in range(10) if x > 5]



# ans={x:x**3 for x in range(1,11)}
# print(ans)

#dict comprehension

# numbers = [1,2,3,4,5]
# squares = {x: x*x for x in numbers}
# print(squares)

# names = ['Alice', 'Alice', 'Bob']
# result = {name: len(name) for name in names}

# {x:x+1 for x in [1,2,3]}

#set comprehension

# numbers = [1,1,2,2,3,3,4]
# unique_numbers = {x for x in numbers}
# print(unique_numbers)

# {x for x in [1,1,2,2,3]}

sen="abhiram vamshi revanth abhiram"
unique={x for x in sen.split()}
print(unique)


#ALL BP
# Basic
result = [x for x in data]

# Transformation
result = [x * 2 for x in data]

# Filtering
result = [x for x in data if condition]

# Transformation + filtering
result = [expression for x in data if condition]

# If-else
result = [value1 if condition else value2 for x in data]

# String transformation
result = [x.strip().lower() for x in data]




##BP
# Flatten 2D list
result = [item for row in matrix for item in row]

# Flatten + filter
result = [
    item
    for row in matrix
    for item in row
    if condition
]

# Flatten + transform + filter
result = [
    expression
    for row in matrix
    for item in row
    if condition
]

# All combinations
result = [(x, y) for x in a for y in b]

# Combinations with filter
result = [
    (x, y)
    for x in a
    for y in b
    if condition
]

# Create 2D list
matrix = [
    [expression for j in inner_data]
    for i in outer_data
]