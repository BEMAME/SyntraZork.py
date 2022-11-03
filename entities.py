entitySyn={} # dict with synonyms for all entities, is populated by entity init

class Entity:
    def __init__(self, name, lookT, synonyms=[]):
        self.name = name
        self.lookT = lookT
        self.synonyms = synonyms
        entitySyn[self.name] = self.synonyms #this puts the synonyms of each entity into the entitySyn dict

    def look(self):
        print(self.lookT)

class Thing(Entity):
    def __init__(self,pickup=False,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.pickup = pickup

class Person(Entity):
    def __init__(self,helloT,pName,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helloT = helloT
        self.pName = pName

    def hello(self):
        print(self.helloT)

class Protagonist:
    cheated = False
    nStairsClimbed = 0

    def __init__(self,score=0,inv={"laptop","pen"}):
        self.score = score
        self.inv = inv

    def changeScore(self,points):
        self.score = self.score + points

        s = lambda x: 'point' if (abs(points) == 1) else 'points'

        if points < 0:
            print(f">Your score decreased by {abs(points)} {s(points)}.")
        else:
            print(f">Your score increased by {points} {s(points)}.")

    def inventory(self):
        print("Your backpack contains the following items;")
        print(">",', '.join(self.inv))

    def prtScore(self):
        print (f"Your score is {self.score}.")

Player = Protagonist()

receptionist = Person(
    name="receptionist",
    pName="Sasha",
    lookT="The receptionist is working on her computer. She is very focused.",
    helloT="With a start, the receptionist looks up at you. 'Oh, good evening. Anything you wanted to [ask]?'",
    synonyms=["receptionist","reception","desk","sasha"]#todo autopopulate synonyms with name
    #def ask() #TODO
)

pen = Thing(name = "pen",
            lookT = "This old pen has been in your backpack for a very long time.",
            pickup = True)

laptop = Thing(name = "laptop",
            lookT = "You look at your tiny laptop. It can barely run PyCharm.",
            pickup = True)