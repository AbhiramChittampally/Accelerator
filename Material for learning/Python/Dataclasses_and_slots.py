from dataclasses import dataclass

@dataclass
class AppConfig:
    host: str
    port: int
config = AppConfig('localhost', 8000)

print(config)    
#  Python automatically generates:
# init
# repr
# eq
# for you.



# #frozen dataclass
# from dataclasses import dataclass

# @dataclass(frozen=True)
# class AppConfig:
#     host: str
#     port: int
   
# #frozen instance error
# config = AppConfig('localhost', 8000)

# config.port = 9000    


#post initialization with post_init
from dataclasses import dataclass

@dataclass
class AppConfig:
    host: str
    port: int

    def __post_init__(self):           #post initialization method
        if self.port <= 0:
            raise ValueError('Invalid port')
      
# #slots in todays python
# from dataclasses import dataclass

# @dataclass(slots=True)
# class Employee:
#     ID:int
#     name:str
#     salary:int
    
#     def display(self):
#         print(f"Employee ID: {self.ID}")
#         print(f"Employee Name: {self.name}")
#         print(f"Employee Salary: {self.salary}")
    
    
# id1=int(input())
# name=input()
# salary=int(input())
# Emp=Employee(id1,name,salary)
# Emp.display()