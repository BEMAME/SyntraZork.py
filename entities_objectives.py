entitySyn = {}  # dict with synonyms for all entities, is populated by entity init


class Entity:
    def __init__(self, name, lookT, synonyms):
        self.name = name
        self.lookT = lookT
        self.synonyms = synonyms
        self.synonyms.append(self.name)
        entitySyn[self.name] = self.synonyms  # this puts the synonyms of each entity into the entitySyn dict

    def look(self):
        print(self.lookT)
        if self.name == "receptionist" and findClassRoom.done is False:  # receptionist will ask if you need help
            receptionist.hello()
        if self.name == "display" and findClassRoom.done is False:
            findClassRoom.complete()


class Thing(Entity):
    def __init__(self, useL=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.useL = useL


class Person(Entity):
    def __init__(self, helloT, askT, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helloT = helloT
        self.askT = askT

    def hello(self):
        print(self.helloT)

    def ask(self):
        print(self.askT)
        if self.name == "receptionist" and findClassRoom.done is False:
            findClassRoom.complete()


class Protagonist:
    def __init__(self, nStairsClimbed=0, score=0, inv={"laptop","bottle"}):
        self.nStairsClimbed = nStairsClimbed
        self.score = score
        self.inv = inv

    def changeScore(self, points):
        self.score = self.score + points

        if points == 0:
            return None  # this is needed for repeatable Objectives in which the score for repeating the objective is 0.

        s = lambda x: 'point' if (abs(points) == 1) else 'points'
        if points < 0:
            print(f"> Your score decreased by {abs(points)} {s(points)}.")
        else:
            print(f"> Your score increased by {points} {s(points)}.")

    def inventory(self):
        print("Your backpack contains the following items;")
        print("> ", ', '.join(self.inv))

    def prtScore(self):
        print(f"Your score is {self.score}.")


Player = Protagonist()


class Objective:
    def __init__(self, completeT, score, done=False, repeatable=False, repeatT="", repeatScore=0, confirmT=""):
        self.completeT = completeT
        self.score = score
        self.done = done
        self.repeatable = repeatable
        self.repeatT = repeatT
        self.repeatScore = repeatScore
        self.confirmT = confirmT

    def complete(self):
        if self.done is False:  # player hasn't completed the objective yet
            self.done = True
            print(self.completeT)
            Player.changeScore(self.score)

        elif self.done is True and self.repeatable is True:  # player completes a repeatable objective again
            print(self.repeatT)
            Player.changeScore(self.repeatScore)

        elif self.done is True and self.repeatable is False:  # player completes a non-repeatable objective
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
    completeT="> You found which classroom you should go to!",
    score=1
)

hurtEgo = Objective(
    completeT="> Your ego is hurt. Should have known better.",
    score=-1,
    repeatable=False,
    confirmT="> Your ego still hurts from the last time..."
)

getPen = Objective(
    completeT='"You can keep that if you want.", says the receptionist.\n'
              '> You have a pen!',
    score=1
)

getBeer = Objective(
    completeT="Without a word, the barkeep gives you one of the heavy beers on display.\n"
              "> You have a beer! Remember to drink responsibly.",
    score=1
)

getCoffee = Objective(
    completeT='"The barkeep fills up your Thermos bottle with fresh, hot coffee."\n'
              '> You have coffee!',
    score=1
)

manyStairsClimbed = Objective(
    completeT="> You getting tired from walking up all these the stairs...",
    score=-1,
    repeatable=True,
    repeatT=f"> You've climbed {Player.nStairsClimbed} stairs today... Your programmer's muscles ache.",
    # TODO: Ask Kian: Player.nStairsClimbed is always the initial value of 0, how to update?
    repeatScore=-1
)

receptionist = Person(
    name="receptionist",
    lookT="The receptionist is working on her computer. She is very focused.",
    helloT="With a start, the receptionist looks up at you. 'Oh, good evening. Anything you wanted to [ask]?'",
    synonyms=["reception", "desk"],
    askT="You ask the receptionist which classroom you should be in for the Python for Beginners Class.\n"
         '"Ah, yes. Room 102, first floor. Enjoy!"'
)

barista = Person(
    name="barista",
    lookT="The barkeep is washing up. He does not look up at you.",
    helloT='The barkeep shakes off his hands. "Sup?"',
    synonyms=["barkeep","bartender","barkeeper","server","barman","staff"],
    askT='You ask what you can [get] here. "Beer, coffee?", the barkeep seems somewhat impatient.'
)

pen = Thing(name="pen",
            lookT="The Syntra-branded pen you got from the reception desk.",
            synonyms = [])

laptop = Thing(name="laptop",
               lookT="You look at your tiny laptop. It can barely run PyCharm.",
               synonyms = [])

bottle = Thing(name="bottle",
               lookT="Your faithful old Thermos bottle. It's mostly empty, just a splash of cold coffee remains.",
               synonyms=["thermos","cup"])

display = Thing(name="display",
                lookT="The display lists all classes that are given this evening.\n"
                      "~~Social media consultant - Room 203~~\n"
                      "~~Project Management: Room 101~~\n"
                      "~~Python for Beginners: Room 102~~\n"
                      "~~Body Language: Room 201~~\n"
                      "~~Vitality Coach: Room 303~~",
                synonyms=[])

coffee = Thing(name="coffee",
               lookT="Your faithful old Thermos bottle, filled with hot coffee from the bar.",
               synonyms=[])

beer = Thing(name="beer",
             lookT="A specialty beer. Is this the right time to open it?",
             synonyms=[])

bar = Entity(name="bar",
             lookT="You pick up a faint whiff of freshly ground coffee. The bar to your west is opened.",
             synonyms=["café", "cafe", "pub"])

exit = Entity(name="exit",
              lookT="The entrance to the building. You came in this way.",
              synonyms=[])
