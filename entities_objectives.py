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
    def __init__(self, consumeOnUse, useT="", useRoom=["ANY"], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consumeOnUse = consumeOnUse
        self.useT = useT
        self.useRoom = useRoom

    def use(self):
        if Player.currentRoom in self.useRoom or "ANY" in self.useRoom:
            print(self.useT)
            if self.consumeOnUse is True:
                Player.inv.remove(self.name)
                print(f"> You no longer have the {self.name}.")

            # specials
            if self.name == "coffee":
                drinkCoffee.complete()
                Player.drinks += 1
                Player.bladderCheck()
            elif self.name == "beer":
                Player.drinks += 3
                if Player.classComplete is True:
                    drinkBeerAfter.complete()
                else:
                    drinkBeer.complete()
                Player.bladderCheck()
            elif self.name == "toilets":
                Player.bladderCheck()

        else:
            print("You can't use that here.")



    def take(self):
        Player.currentRoom.itemD.pop(self.name)  # remove the item from room
        Player.inv.add(self.name)  # put item in inventory
        if self.name == "pen":  # todo: @kian: elegantere manier om dit te doen? Er zijn specifieke inputs die een
            # todo:             "complete" method triggeren, e.g. "get pen" of "get beer".
            getPen.complete()
        elif self.name == "beer":
            getBeer.complete()
        elif self.name == "coffee":
            Player.inv.remove("bottle")
            getCoffee.complete()
        else:
            print(f"You put the {self.name} in your backpack.")

class Person(Entity):
    def __init__(self, helloT, askT, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helloT = helloT
        self.askT = askT

    def hello(self):
        print(self.helloT)

    def ask(self):
        print(self.askT)
        if self.name in ["receptionist","teacher","barista"] and bladderFull.done is True:
            print(f"You ask the {self.name} where the toilets are."
                  '"First floor, east."')
        elif self.name == "receptionist" and findClassRoom.done is False:
            findClassRoom.complete()


class Protagonist:
    def __init__(self, currentRoom, classComplete=False, nStairsClimbed=0, score=0, drinks=0, inv={"laptop","bottle"}):
        self.currentRoom = currentRoom
        self.classComplete = classComplete
        self.nStairsClimbed = nStairsClimbed
        self.score = score
        self.drinks = drinks
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

    def bladderCheck(self):
        print(Player.currentRoom)
        if Player.drinks > 3:
            bladderFull.complete()
        if Player.drinks > 5:
            bladderDisaster.complete()
            Player.drinks = 0
        if Player.drinks > 0 and Player.currentRoom == "Toilets":
            bladderRelief.complete()
            print("test")
            Player.drinks = 0


Player = Protagonist(currentRoom="lobby")


class Objective:
    def __init__(self, completeT, score, completeRoom, done=False, repeatable=False, repeatT="", repeatScore=0, confirmT=""):
        self.completeT = completeT
        self.score = score
        self.completeRoom = completeRoom
        self.done = done
        self.repeatable = repeatable
        self.repeatT = repeatT
        self.repeatScore = repeatScore
        self.confirmT = confirmT

    def complete(self):
        if Player.currentRoom in self.completeRoom or "ANY" in self.completeRoom:
            if self.done is False:  # player hasn't completed the objective yet
                self.done = True
                print(self.completeT)
                Player.changeScore(self.score)

            elif self.done is True and self.repeatable is True:  # player completes a repeatable objective again
                print(self.repeatT)
                Player.changeScore(self.repeatScore)

            elif self.done is True and self.repeatable is False:  # player completes a non-repeatable objective
                print(self.confirmT)
        else:
            print("This is not the right place to use this item...")

# an easter egg
getPoints = Objective(
    completeT="> You grab some points.",
    score=2,
    completeRoom=["ANY"],
    repeatable=True,
    repeatT="> Hey! Don't get greedy now!",
    repeatScore=-1
)

findClassRoom = Objective(
    completeT="> You found which classroom you should go to!",
    score=1,
    completeRoom=["ANY"]
)

hurtEgo = Objective(
    completeT="> Your ego is hurt. Should have known better.",
    score=-1,
    completeRoom=["ANY"],
    repeatable=False,
    confirmT="> Your ego still hurts from the last time..."
)

getPen = Objective(
    completeT='"You can keep that if you want.", says the receptionist.\n'
              '> You have a pen!',
    score=1,
    completeRoom=["ANY"]
)

getBeer = Objective(
    completeT="Without a word, the barkeep gives you one of the heavy beers on display.\n"
              "> You have a beer! Remember to drink responsibly.",
    score=1,
    completeRoom=["ANY"]
)

getCoffee = Objective(
    completeT="The barkeep fills up your Thermos bottle with fresh, hot coffee.\n"
              '> Your bottle was upgraded into coffee!',
    score=1,
    completeRoom=["ANY"]
)

drinkCoffee = Objective(
    completeT="The coffee peps you up.",
    score=1,
    completeRoom=["ANY"],
    repeatable=False,
    confirmT="You've already hit diminishing returns on the coffee.\n"
             "Still tasty, but you no longer feel the cafeine hit."
)

drinkBeer = Objective(
    completeT="The beer reduces your ability to focus on the lessons.\n"
              "> You chose a really bad time to consume alcohol...",
    score=-3,
    completeRoom=["ANY"],
    repeatable=False,
    confirmT=""
)

drinkBeerAfter = Objective(
    completeT="In celebration of finishing the classes, you crack open the beer.\n"
              "After you finish your drink, you feel slightly embarrassed for impulsively\n"
              " consuming alcohol within the Syntra building."
              "> You chose a somewhat unfortunate time for consuming alcohol...",
    score=-3,
    completeRoom=["ANY"],
    repeatable=False,
    confirmT=""
)

manyStairsClimbed = Objective(
    completeT="You getting tired from walking up all these the stairs...",
    score=-1,
    completeRoom=["ANY"],
    repeatable=True,
    repeatT=f"You've climbed {Player.nStairsClimbed} stairs today... Your programmer's muscles ache.",
    # TODO: Ask Kian: Player.nStairsClimbed is always the initial value of 0, how to update?
    repeatScore=-1
)

bladderFull = Objective(
    completeT="> All these drinks have filled up your bladder...",
    score=0,
    completeRoom=["ANY"],
    repeatable=True,
    repeatScore=-1,
    repeatT="Although your bladder is already completely full, you decide to fill it up further.\n"
            "> This may end in disaster..."
)

bladderDisaster = Objective(
    completeT="You're too late. Emotions of warmth, relief and embarrassment wash over you.\n"
              "> You've had a little accident.",
    score=-10,
    completeRoom=["ANY"],
    repeatable=True,
    repeatScore=-5,
    repeatT="Once more you piss yourself. This time you're not quite as embarrassed.\n"
            "> You've had another little accident."
)

bladderRelief = Objective(
    completeT="You relieve yourself.",
    score=1,
    completeRoom=["toilets"],
    repeatable=True,
    repeatScore=0,
    repeatT="You have another quick tinkle. Better safe than sorry!"
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
            synonyms = [],
            consumeOnUse=False)

laptop = Thing(name="laptop",
               lookT="You look at your tiny laptop. It can barely run PyCharm.",
               synonyms = [],
               consumeOnUse=False)

bottle = Thing(name="bottle",
               lookT="Your faithful old Thermos bottle. It's mostly empty, just a splash of cold coffee remains.",
               synonyms=["thermos","cup"],
               consumeOnUse=False)

display = Thing(name="display",
                lookT="The display lists all classes that are given this evening.\n"
                      "~~Social media consultant - Room 203~~\n"
                      "~~Project Management: Room 101~~\n"
                      "~~Python for Beginners: Room 102~~\n"
                      "~~Body Language: Room 201~~\n"
                      "~~Vitality Coach: Room 303~~",
                synonyms=[],
                consumeOnUse=False)

coffee = Thing(name="coffee",
               lookT="Your faithful old Thermos bottle, filled with hot coffee from the bar.",
               useT="You take a sip of from your Thermos bottle.",
               synonyms=[],
               consumeOnUse=False)

beer = Thing(name="beer",
             lookT="A specialty beer. Is this the right time to open it?",
             useT="You drink the beer.",
             synonyms=[],
             consumeOnUse=True)

bar = Entity(name="bar",
             lookT="You pick up a faint whiff of freshly ground coffee. The bar to your west is opened.",
             synonyms=["café", "cafe", "pub"])

exit = Entity(name="exit",
              lookT="The entrance to the building. You came in this way.",
              synonyms=[])

toilet = Thing(name="toilet",
               lookT="Clean and well maintained.\n",
               synonyms=["toilets","lavatory","wc"],
               consumeOnUse="False")
