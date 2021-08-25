class Dog():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def sounds(self):
        return "WOOF!"

class Frenchie(Dog):
    def __init__(self, name, age):
        super().__init__(name, age)

    def sounds(self):
        return "YAP YAP"

    def breathing(self):
        return "Gremlin"

murphy = Frenchie("Murphy", 1)
print(murphy.sounds())

#zeus = Dog("Zeus", 2)
#print(zeus.breathing())
