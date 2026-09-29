# from typing import Protocol 

# class ConfigProvider(Protocol): 
#     def load(self) -> dict: 
#         ...
        
#         #Next, you can create a completely independent class that happens to have the same method.  Pythonclass FileConfig: 
#     def load(self): 
#         return {}


#boilerplate code
from typing import Protocol

# 1. Define the Protocol (The Contract/Rule)
class MyProtocol(Protocol):
    def required_method(self, data: str) -> bool:
        """Docstring explaining what this method should do."""
        ...  # The ellipsis (...) is standard Python syntax for Protocols

# 2. Implement the Protocol (No inheritance needed!)
class MyImplementation:
    def required_method(self, data: str) -> bool:
        # --- Your actual logic goes here ---
        return True

# 3. Use the Protocol in your code
def process_data(handler: MyProtocol, input_data: str):
    """This function accepts ANY object that satisfies MyProtocol."""
    success = handler.required_method(input_data)
    return success

#example
from typing import Protocol

# 1. THE PROTOCOL: The Rule
class Flyer(Protocol):
    def fly(self) -> str:
        ...

# 2. THE CLASSES: They just follow the rule naturally
class Bird:
    def fly(self) -> str:
        return "Flap flap! I am a bird!"

class Airplane:
    def fly(self) -> str:
        return "Vroooom! I am a plane!"

# 3. THE TEST: This accepts ANY Flyer
def test_flight(thing: Flyer):
    print(thing.fly())

# Run it!
test_flight(Bird())
test_flight(Airplane())