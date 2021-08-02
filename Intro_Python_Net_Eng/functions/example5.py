def generate_email(username, provider="gmail"):
    email_addy = f"{username}@{provider}.com"
    return email_addy

#my_email = generate_email("ipvzero")
#print(my_email)

my_names = ["Trevor", "Knox", "John", "Simona", "Bob"]
my_email_list = []

for name in my_names:
    new_email = generate_email(name, "cbtnuggets")
    my_email_list.append(new_email)

for email in my_email_list:
    print(f"New email account generated: {email}")
