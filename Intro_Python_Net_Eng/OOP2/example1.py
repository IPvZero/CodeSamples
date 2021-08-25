from johnmodule import CreateEmail

my_email = CreateEmail("John")
my_email._provider = ["spam.com", "spam.co.uk"]
print(my_email.generate())
