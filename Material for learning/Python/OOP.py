# class BankAccount:

#     bank_name = 'Python National Bank'

#     def __init__(self, owner, balance):
#         self.owner = owner
#         self.balance = balance
# account1 = BankAccount('Alice', 1000)
# account2 = BankAccount('Bob', 500)

# print(account1.bank_name)
# print(account2.bank_name)        

#inheritance
# class BankAccount:

#     def __init__(self, owner, balance):
#         self.owner = owner
#         self.balance = balance


# class SavingsAccount(BankAccount):

#     def add_interest(self):
#         self.balance *= 1.05

# #MRO(Method resolution order)
# print(SavingsAccount.__mro__)


# from abc import ABC, abstractmethod

# # 1. ABSTRACTION: An abstract class cannot be instantiated directly.
# class Vehicle(ABC):
#     @abstractmethod
#     def start_engine(self):
#         pass

# # 2. INHERITANCE: Car inherits from Vehicle
# class Car(Vehicle):
#     def __init__(self, brand, model, price):
#         self.brand = brand
#         self.model = model
#         # 3. ENCAPSULATION: Private variable (__price)
#         self.__price = price 

#     # Concrete implementation of abstract method
#     def start_engine(self):
#         return f"The {self.brand}'s engine is purring."

#     # Getter to access private data safely
#     def get_price(self):
#         return self.__price

# # 2. POLYMORPHISM: Another class with the exact same method name
# class Motorcycle(Vehicle):
#     def start_engine(self):
#         return f"The motorcycle engine roars to life!"


# # --- Execution ---
# car = Car("Tesla", "Model 3", 45000)
# bike = Motorcycle()

# # Testing Polymorphism & Abstraction
# for vehicle in (car, bike):
#     print(vehicle.start_engine())

# # Testing Encapsulation
# # print(car.__price) # Errors out! Attribute error.
# print(car.get_price()) # Output: 45000 (Safe access)


#MRO
# class A:
#     def process(self):
#         print("Process in A")

# class B(A):
#     def process(self):
#         print("Process in B")
#         super().process()

# class C(A):
#     def process(self):
#         print("Process in C")
#         super().process()

# class D(B, C):
#     def process(self):
#         print("Process in D")
#         super().process()

# # Create instance of D
# d = D()
# d.process()

# # View the explicit MRO hierarchy
# print(D.__mro__)


#Dunder Methods
class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    # Controls what print() displays
    def __str__(self):
        return f"'{self.title}'"

    # Controls what the developer sees in debugging logs
    def __repr__(self):
        return f"Book(title='{self.title}', pages={self.pages})"

    # Overloads the '+' operator
    def __add__(self, other):
        if isinstance(other, Book):
            return self.pages + other.pages
        return NotImplemented

    # Overloads the len() function
    def __len__(self):
        return self.pages

# --- Execution ---
book1 = Book("Python Basics", 300)
book2 = Book("Advanced OOP", 450)

print(book1)          # Triggers __str__: 'Python Basics'
print(repr(book1))    # Triggers __repr__: Book(title='Python Basics', pages=300)
print(book1 + book2)  # Triggers __add__: 750
print(len(book1))     # Triggers __len__: 300