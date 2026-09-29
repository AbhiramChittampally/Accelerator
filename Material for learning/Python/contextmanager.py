# THE OLD WAY (Dangerous!)
# file = open("data.txt", "r")
# data = file.read()
# # If the program crashes on the line above, the file stays open forever!
# file.close() 

# # THE MODERN WAY (Context Manager)
# with open("data.txt", "r") as file:                           #using with keyword to open the file, which automatically handles closing the file after the block is executed  
#     data = file.read()
# As soon as we leave the indented block, Python automatically closes the file.


#example of your own context manager by the class based approach using __enter__ and __exit__ methods
# class MyContextManager:
#     def __enter__(self):
#         print("1. Opening the toy box...")
#         return self # This is what gets assigned to the 'as' variable

#     def __exit__(self, exc_type, exc_value, traceback):
#         # This ALWAYS runs, even if the code inside crashes.
#         print("3. Packing up and locking the box!")
#         # exc_type, exc_value, and traceback hold error details if a crash happened.

# # Usage:
# with MyContextManager() as my_box:
#     print("2. Playing with the toys!")


#generator way using contextlib
# from contextlib import contextmanager

# @contextmanager
# def my_simple_manager():
#     print("1. Opening the toy box...")
    
#     try:
#         yield "Here is your toy!"  # Pauses here and gives the resource to the 'with' block
#     finally:
#         # The 'finally' block acts as our guaranteed __exit__
#         print("3. Packing up and locking the box!")

# # Usage:
# with my_simple_manager() as toy:
#     print(f"2. {toy}")



#real world example of context manager 
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        print(f"--> Connecting to database: {self.db_name}")
        self.connection = f"Connection_Object_for_{self.db_name}"
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(f"--> ERROR DETECTED: {exc_value}. Rolling back transaction!")
        else:
            print("--> Success! Committing transaction to save data.")
            
        print(f"--> Closing connection to {self.db_name}.\n")
        return True # Suppresses the error so our program doesn't crash


# --- Let's test it! ---

# Scenario A: Everything goes well
with DatabaseConnection("UserDB") as db:
    print("Saving new user: Alice...")

# Scenario B: A crash happens inside the block
with DatabaseConnection("UserDB") as db:
    print("Saving new user: Bob...")
    raise ValueError("Bob's data is corrupted!")
    print("This line will never print.")