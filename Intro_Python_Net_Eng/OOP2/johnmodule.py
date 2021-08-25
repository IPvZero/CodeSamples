import random

class CreateEmail:
    _provider = ["outlook.com", "outlook.co.uk"]

    def __init__(self, name):
        self.name = name

    def generate(self):
        suffix = random.choice(self._provider)
        email = f"{self.name}@{suffix}"
        return email
