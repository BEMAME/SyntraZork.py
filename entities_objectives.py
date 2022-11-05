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
        if self.name == "receptionist" and findClassRoom.done is False: #receptionist will ask if you need help
            receptionist.hello()
        if self.name == "display" and findClassRoom.done is False:
            findClassRoom.complete()

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
        if self.name == "receptionist" and findClassRoom.done is False:
            findClassRoom.complete()

class Protagonist:
    def __init__(self,nStairsClimbed=0,score=0,inv={"laptop"}):
        self.nStairsClimbed = nStairsClimbed
        self.score = score
        self.inv = inv

    def changeScore(self,points):
        self.score = self.score + points

        if points == 0:
            return None #this is needed for repeatable Objectives in which the score for repeating the objective is 0.

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

class Objective:
    def __init__(self,completeT,score,done=False,repeatable=False,repeatT="",repeatScore=0,confirmT=""):
        self.completeT = completeT
        self.score = score
        self.done = done
        self.repeatable = repeatable
        self.repeatT = repeatT
        self.repeatScore = repeatScore
        self.confirmT = confirmT

    def complete(self):
        if self.done is False: #player hasn't completed the objective yet
            self.done = True
            print(self.completeT)
            Player.changeScore(self.score)

        elif self.done is True and self.repeatable is True: #player completes a repeatable objective again
            print(self.repeatT)
            Player.changeScore(self.repeatScore)

        elif self.done is True and self.repeatable is False: #player completes a non-repeatable objective
            print(self.confirmT)

# an easter egg
getPoints = Objective(
    completeT="> You grab some points.",
    score=3,
    repeatable=True,
    repeatT="> Hey! Don't get greedy now!",
    repeatScore=-1
)

findClassRoom = Objective(
    completeT="> You found out which classroom you should go to!",
    score=1,
)

getPen = Objective(
    completeT='"You can keep that if you want.", says the receptionist.\n'
              '> You have a pen!',
    score=1
)

manyStairsClimbed = Objective(
    completeT="> You getting tired from walking up all these the stairs...",
    score=-1,
    repeatable=True,
    repeatT=f"> You've climbed {Player.nStairsClimbed} stairs today... Your programmer's muscles ache.",
    #TODO: Ask Kian: Player.nStairsClimbed is always the initial value of 0, how to update?
    repeatScore=-1
)

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
            lookT = "A Synta-branded pen you got from the reception desk.",
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