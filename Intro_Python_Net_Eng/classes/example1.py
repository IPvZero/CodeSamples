class Drummer:
    member_type = "Percussionist"
    def __init__(self, style, lead_hand, brand):
        self.style = style
        self.lead_hand = lead_hand
        self.brand = brand

    def paradiddle(self):
        if self.lead_hand == "left":
            print("L! R! L! L!")
        else:
            print("R! L! R! R!")

    def introduction(self):
        print("Hello I am a drummer! What do you do for a living?")

    def drum_lessons(self, grip):
        if grip == "traditional":
            print("Sure I can teach you no probs!")
        else:
            print("Sorry! I only teach traditional grip!")



buddy_rich = Drummer("jazz", "right", "Slingerland")
#buddy_rich.paradiddle()
#buddy_rich.introduction()
buddy_rich.drum_lessons("matched")
