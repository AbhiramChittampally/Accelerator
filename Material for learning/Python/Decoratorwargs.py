#example
import functools

# LEVEL 1: The Factory (Takes your custom arguments)
def repeat(times):
    
    # LEVEL 2: The Actual Decorator (Takes the function)
    def decorator(func):
        
        # LEVEL 3: The Wrapper (Does the actual work)
        @functools.wraps(func)  # Always goes on the innermost wrapper!
        def wrapper(*args, **kwargs):
            
            # Loop however many 'times' the factory was told
            for _ in range(times):
                result = func(*args, **kwargs)
                
            return result # Return the final result
            
        return wrapper
        
    return decorator

# --- Let's test it! ---

@repeat(times=3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alex")



#boilerplate code for decorators with args
import functools

def my_parameterized_decorator(config_arg1, config_arg2):
    """LEVEL 1: The Factory. Receives your custom settings."""
    
    def decorator(func):
        """LEVEL 2: The Decorator. Receives the target function."""
        
        @functools.wraps(func) # CRITICAL: Preserves function metadata
        def wrapper(*args, **kwargs):
            """LEVEL 3: The Wrapper. Executes the logic."""
            
            # --- Do something BEFORE using config_arg1 ---
            
            result = func(*args, **kwargs)
            
            # --- Do something AFTER using config_arg2 ---
            
            return result
            
        return wrapper
    return decorator



#example with @retry
import time
import random

# (Assuming the 3-level @retry decorator factory is defined above this)

@retry(max_attempts=3, delay=1, exceptions=(ConnectionError,))
def fetch_user_data(user_id):
    """Simulates a network call that sometimes fails."""
    
    # Simulate a random network failure
    if random.random() < 0.6: 
        print(f"Network timeout for user {user_id}!")
        raise ConnectionError("Failed to connect.")
        
    return {"id": user_id, "name": "Srikanth"}

# When you call this, the decorator automatically handles the retries!
data = fetch_user_data(42)
print(f"Got data: {data}")