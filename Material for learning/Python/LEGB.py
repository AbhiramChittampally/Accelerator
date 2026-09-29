#local scope
def greet():
    message = 'Hello'
    print(message)

greet()



#enclosing scope
def outer():

    message = 'Outer Variable'

    def inner():
        print(message)

    inner()
    
#global scope
app_name = 'Inventory System'

def show_app():
    print(app_name)
    

#Using global:

# python — Code Example
counter = 0

def increment():
    global counter
    counter += 1

increment()

# What about nested functions?

# ChatGPT
# •
# AI Assistant
# Example Card
# python — Code Example
def outer():

    count = 0

    def inner():
        nonlocal count
        count += 1
        print(count)

    inner()