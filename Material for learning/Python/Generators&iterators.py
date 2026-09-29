def magic_counter(stop_at):
    print("Starting the magic counter!")
    current = 1
    
    while current <= stop_at:
        print(f"About to yield {current}...")
        yield current  # The function PAUSES here and hands the number out
        print("Resuming after the pause!")
        current += 1

# 1. We create the dispenser. NO code runs yet!
dispenser = magic_counter(3)

# 2. We ask for the first value.
print(next(dispenser))  
# Output: 
# Starting the magic counter!
# About to yield 1...
# 1

# 3. We ask for the next value. It resumes right where it left off!
print(next(dispenser))
# Output:
# Resuming after the pause!
# About to yield 2...
# 2
print(next(dispenser))
print(next(dispenser))
# Output:   


#lazy data processor
def process_large_file(filepath):
    """Reads a file line-by-line without loading it all into RAM."""
    with open(filepath) as file:
        for line in file:
            # Clean the line and yield it out one at a time
            yield line.strip()

# Usage:
for clean_line in process_large_file("massive_10GB_log.txt"):
    print(clean_line)

#yield from
def flatten_data(nested_lists):
    for current_list in nested_lists:
        # Instead of writing a second loop here, we use 'yield from'
        yield from current_list

data = [[1, 2], [3, 4], [5]]
print(list(flatten_data(data))) # Output: [1, 2, 3, 4, 5]