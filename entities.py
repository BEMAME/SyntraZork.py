entitySyn={} # dict with synonyms for all entities, is populated by entity init

class Entity:
    def __init__(self, name, lookT, synonyms):
        self.name = name
        self.lookT = lookT
        self.synonyms = synonyms
        self.synonyms.append(self.name)
        entitySyn[self.name] = self.synonyms #this puts the synonyms of each entity into the entitySyn dict

    def look(self):
        print(self.lookT)
        if self.name == "receptionist" and Player.knowsClassroomNumber is False:
            receptionist.hello()

        if self.name == "display" and Player.knowsClassroomNumber is False:
            Player.knowsClassroomNumber = True
            Player.changeScore(1)

class Thing(Entity):
    def __init__(self,pickup=False,useL=[],*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.pickup = pickup
        self.useL = useL

class Person(Entity):
    def __init__(self,pName,helloT,askT,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.pName = pName
        self.helloT = helloT
        self.askT = askT

    def hello(self):
        print(self.helloT)

    def ask(self):
        print(self.askT)
        if self.name == "receptionist" and Player.knowsClassroomNumber is False:
            Player.knowsClassroomNumber = True
            Player.changeScore(1)

class Protagonist:
    cheated = False
    knowsClassroomNumber = False
    nStairsClimbed = 0

    def __init__(self,score=0,inv={"laptop","pen"}):
        self.score = score
        self.inv = inv

    def changeScore(self,points):
        self.score = self.score + points

        s = lambda x: 'point' if (abs(points) == 1) else 'points'
        if points < 0:
            print(f"> Your score decreased by {abs(points)} {s(points)}.")
        else:
            print(f"> Your score increased by {points} {s(points)}.")

    def inventory(self):
        print("Your backpack contains the following items;")
        print("> ",', '.join(self.inv))

    def prtScore(self):
        print (f"Your score is {self.score}.")

Player = Protagonist()

receptionist = Person(
    name="receptionist",
    pName="Sasha",
    lookT="The receptionist is working on her computer. She is very focused.",
    helloT="With a start, the receptionist looks up at you. 'Oh, good evening. Anything you wanted to [ask]?'",
    synonyms=["reception","desk","sasha"],
    askT = "You ask the receptionist which classroom you should be in for the Python for Beginners Class.\n"
           '"Ah, yes. Room 102, first floor. Enjoy!"'
)


pen = Thing(name = "pen",
            lookT = "This old pen has been in your backpack for a very long time.",
            pickup = True,
            synonyms = [])

laptop = Thing(name = "laptop",
            lookT = "You look at your tiny laptop. It can barely run PyCharm.",
            pickup = True,
            synonyms = [])

display = Thing(name = "display",
                lookT = "The display lists all classes that are given this evening.\n"
                        "~~Social media consultant - Room 203~~\n"
                        "~~Project Management: Room 101~~\n"
                        "~~Python for Beginners: Room 102~~\n"
                        "~~Body Language: Room 201~~\n"
                        "~~Vitality Coach: Room 303~~",
                synonyms = [])

bar = Thing(name = "bar",
            lookT = "You pick up a faint whiff of freshly ground coffee. The bar to your west is opened.",
            synonyms = ["café", "cafe", "pub"])

exit = Thing(name = "exit",
            lookT = "This is the way you came in.",
            synonyms = [])