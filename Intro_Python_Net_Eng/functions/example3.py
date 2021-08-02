def my_test_function():
    print("Welcome to CBT Nuggets")


#for num in range(0, 4):
#    my_test_function()

def adder(a, b):
    print(a + b)


def create_email(username, provider):
    """
    This function takes 2 arguments. First pass in a username.
    Second pass in your email provider (eg gmail, outlook, etc)
    """
    print(f"Your new email is {username}@{provider}.com")


#create_email("IPvZero", "gmail")
print(create_email.__doc__)
