from functools import wraps
from functools import wraps






#boilerplate code for decorators
from functools import wraps

# 1. Define the Decorator
def my_custom_decorator(func):
    """Docstring explaining what this decorator adds."""
    
    @wraps(func)  # CRITICAL: Preserves the original function's name and docstring
    def wrapper(*args, **kwargs):
        
        # --- 1. Code to execute BEFORE the original function ---
        # e.g., start a timer, check permissions, log a message
        
        # --- 2. Execute the original function ---
        result = func(*args, **kwargs)
        
        # --- 3. Code to execute AFTER the original function ---
        # e.g., stop a timer, format the result, log completion
        
        # --- 4. Return the result back to the caller ---
        return result
        
    return wrapper

# 2. Apply the Decorator
@my_custom_decorator
def target_function(param1, param2):
    # --- Your actual function logic goes here ---
    pass



#example
# 1. THE DECORATOR: The Magic Backpack
def shout_decorator(func):
    # """Makes any returned text uppercase and adds exclamation marks."""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get the normal text from the function
        original_text = func(*args, **kwargs)
        
        # Change it before giving it back
        return original_text.upper() + "!!!"
        
    return wrapper

# 2. THE FUNCTION: The regular robot
@shout_decorator
def say_hello(name: str) -> str:
    return f"Hello there, {name}"

# 3. THE TEST
print(say_hello("Alice"))

# Output:
# HELLO THERE, ALICE!!!