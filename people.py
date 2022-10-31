class Person:
    def __init__(self,name,pron,lookT,helloT):
        self.name = name
        self.pron = pron
        self.lookT = lookT
        self.helloT = helloT

    def hello(self):
        print(self.helloT)

class Protagonist:
    cheated = False
    nStairsClimbed = 0

    def __init__(self,score=0,inv=()):
        self.score = score
        self.inv = inv

    def changeScore(self,points):
        self.score = self.score + points

        s = lambda x: 'point' if (abs(points) == 1) else 'points'

        if points < 0:
            print(f">Your score decreased by {abs(points)} {s(points)}.")
        else:
            print(f">Your score increased by {points} {s(points)}.")

    def prtScore(self):
        print (f"Your score is {self.score}.")

Player = Protagonist()

receptionist = Person(
    name="Sasha",
    pron="she",
    lookT="The receptionist is working on her computer. She is deep in thought.",
    helloT="With a start, the receptionist looks up at you. 'Oh, good evening. Anything you wanted to [ask]?'"

    #def ask()
)