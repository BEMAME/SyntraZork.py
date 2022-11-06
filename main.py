print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
      "\n~~~~  Welcome to SyntraZork! Input 'help' for options  ~~~~\n"
      "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

from rooms import *

class GameC:
    gameOver = False

    def __init__(self, gameStart=True):
        self.gameStart = gameStart

    def synonymCheck(self, inputVal):
        try:
            x = [target for target, syn in entitySyn.items() if inputVal in syn][0]
            return x  # this returns the key of the entitySyn dictionary
        except:
            None

    def helpMenu(self):
        print("[n] to go North\n"
              "[e] to go East\n"
              "[s] to go South\n"
              "[w] to go West\n"
              "[u] to go Up\n"
              "[d] to go Down\n"
              "[look] to look around the room\n"
              "[talk <person>] to start a conversation\n"
              "[look <object>] to look at an object.\n"
              "[use <object>] to use and object that's in your backpack.\n"
              "[take <object>] to pick up an object.\n"
              "[i] to show a list of items that are in your backpack."
              "[score] to display your current score\n"
              "[q] to quit")

    def walkInp(self):  # Returns new room if valid direction input,
                        # returns true/false is for checking if valid input given
        if len(inp.split()) > 1 and inp.lower() != "go home":
            return False, currentRoom

        if inp.lower() not in ["n", "e", "s", "w", "u", "d", "go home"]:
            return False, currentRoom

        if currentRoom.checkIfPresent(inp,currentRoom.exitsL):
            if inp.lower() == "n":
                coor[1] = coor[1]+1
            if inp.lower() == "e":
                coor[0] = coor[0]+1
            if inp.lower() == "s":
                coor[1] = coor[1]-1
            if inp.lower() == "w":
                coor[0] = coor[0]-1
            if inp.lower() == "u":
                coor[2] = coor[2]+1
                currentRoom.climbStairsExhaustion()
            if inp.lower() == "d":
                coor[2] = coor[2]-1
            if inp.lower() == "go home":  # this can only be selected from the "Outside" room
                Game.endGame()
            return True, currentRoom.enter()
        else:
            print(f"You cannot go that way.")
            return True,currentRoom

    def checkInputLen(self):  # is called when player enters 3 words or more - this is not allowed
        if len(inp.split()) > 2:
            print("You entered too many words. To interact with something or someone type '<action> <object',\n"
                  "e.g. 'ask receptionist' or 'look laptop'.")
            return True

        else:
            return False

    def optionsInp(self):  # various meta-options. Return true/false is for checking if valid input given
        if inp.split()[0].lower() not in ["help", "coor", "where", "location", "score", "points", "i", "inv",
                                          "inventory", "backpack"]:
            return False

        if inp.lower() == "help":
            Game.helpMenu()
            return True

        if inp.lower() in ["coor", "where", "location"]:
            print(f"{currentRoom.shortT} Your coordinates are {coor}.")
            return True

        if inp.lower() in ["score", "points"]:
            Player.prtScore()
            return True

        if inp.lower() in ["i", "inv", "inventory", "backpack"]:
            Player.inventory()
            return True

    # looking around the room. Return true/false is for checking if valid input given
    def lookInp(self):
        if inp.split()[0].lower() not in ["look"]:
            return False

        # player typed "look" or "look room" ==> give description of room
        if len(inp.split()) == 1 or inp.lower() == "look room":
            currentRoom.look()
            return True

        # player typed "look <something>"
        elif len(inp.split()) == 2:
            x = self.synonymCheck(inp.split()[1].lower())
            if x in Player.inv:
                print("You have a look in your backpack.")
                str_to_class(x).look()
            elif x in currentRoom.lookL:
                str_to_class(x).look()
            elif x in currentRoom.itemD:
                print(currentRoom.itemD[x])
            else:
                print("I don't understand what you want to look at. Are you sure it is visible?")
                print(entitySyn,"x=",x)

        return True

    def talkInp(self):
        if inp.split()[0].lower() not in ["talk","ask","call"]:
            return False

        if len(inp.split()) == 1:
            print("Who are you talking to?")

        elif len(inp.split()) == 2:
            x = self.synonymCheck(inp.split()[1].lower())
            if x in currentRoom.askL:
                str_to_class(x).ask()
            elif x in Player.inv:
                print(f"{x.capitalize()} isn't feeling very talkative.")
            else:
                return False

        return True

    def takeInp(self):
        if inp.split()[0].lower() not in ["get","grab","take"]:
            return False

        if len(inp.split()) == 1:
            print(f"What do you want to {inp.split()[0].lower()}?")
            return True

        elif len(inp.split()) == 2:
            x = self.synonymCheck(inp.split()[1].lower())

            if x in currentRoom.itemD:
                currentRoom.itemD.pop(inp.split()[1].lower()) #remove the item from room
                Player.inv.add(inp.split()[1].lower()) #put item in inventory
                if x == "pen":  # todo: @kian: elegantere manier om dit te doen? Er zijn specifieke inputs die een
                    # todo:             "complete" method triggeren, e.g. "get pen" of "get beer".
                    getPen.complete(currentRoom.name.lower())
                elif x == "beer":
                    getBeer.complete(currentRoom.name.lower())
                elif x == "coffee":
                    Player.inv.remove("bottle")
                    getCoffee.complete(currentRoom.name.lower())

                else:
                    print(f"You put the {x} in your backpack.")
                return True

            elif x in currentRoom.lookL:
                print(f"You can't pick the {inp.split()[1].lower()} up! You're just a programmer,"
                      f" not some strongman jock!")
                hurtEgo.complete(currentRoom.name.lower())
                return True

            elif x in Player.inv:
                print(f"You already have the {inp.split()[1].lower()}!")
                return True

            # an easter egg objective
            elif inp.split()[1].lower() == "points":
                getPoints.complete(currentRoom.name.lower())

            else:
                print(f"I'm not sure how to pick that up...")

        return True

    def useInp(self):
        if inp.split()[0].lower() not in ["use"]:
            return False

        if len(inp.split()) == 1:
            print(f"What do you want to {inp.split()[0].lower()}?")
            return True

        elif len(inp.split()) == 2:
            x = self.synonymCheck(inp.split()[1].lower())
            n = 'an' if inp.split()[1].lower()[0] in ["a","e","i","o","u"] else 'a'  # "a pen" versus "an objective"
            if x in Player.inv:
                str_to_class(x).use(currentRoom)

                if x == "coffee":
                    drinkCoffee.complete(currentRoom)
                elif x == "beer" and Player.classComplete is False:
                    drinkBeer.complete(currentRoom)
                elif x == "beer" and Player.classComplete is True:
                    drinkBeerAfter.complete(currentRoom)

            elif x in entitySyn:
                print(f"You don't have {n} {inp.split()[1].lower()}.")
            else:
                print(f"What's {n} {inp.split()[1].lower()}?")
            return True


    def invalidAction(self):
        print("I don't understand what you want to do. Type [help] for a list of basic commands.")

    def endGame(self):
        if Player.score < 0:  # horrible ending
            print(f"You cannot bear this any longer. You run towards your bicycle and ride off as fast as you can.\n"
                  f"When you look behind you, you see the Syntra building disappear behind the horizon.\n"
                  f"You swear never to return again.")
        elif -1 < Player.score < 10:  # bad ending
            print(f"You sigh as walk towards your bicycle. You don't feel like you've learned much today.\n"
                  "On the way home, you contemplate quitting the Python for beginners course.")
        elif Player.score > 9:  # good ending
            print(f"Satisfied, you walk towards your bicycle.\n"
                  "On the way home, many ideas for your Python project come to mind.\n"
                  "You jot them down on a piece of paper before you go to bed.")

        input("\n(press Enter to continue)")

        if "beer" in Player.inv:
            print(f"After a long day you're finally home!\n"
                  f"You sit down on your couch and crack open the heavy beer you got from the bar.")
            Player.changeScore(3)

            input("\n(press Enter to continue)")

        print(f"\n ~~You finished the game with a score of {Player.score}! Thanks for playing!")

        self.gameOver = True

        sys.exit()

Game = GameC()

while True:
    # setting up the very first room at the start of the game...
    if Game.gameStart is True:
        print("------------------------------------------------------------------------------------------------------")
        currentRoom = roomFromCoor(coor)
        print("A few weeks ago, you registered for the Syntra 'Python for Beginners' class.\n"
              "Full of excitement you enter the Syntra lobby. Classes start in 5 minutes.\n"
              "You should [look] around to find out where to go.")
        Game.gameStart = False
    inp = input("------------------------------------------------------------------------------------------------------"
                "\nWhat do you do? ___")
    #

    if inp == "":
        print("Type 'help' for an overview of basic commands.")
        continue

    if inp.lower() in ["q", "quit"]:
        break

    #checks what input was given and performs the action
    validAction = []
    walkValidInp, currentRoom = Game.walkInp()
    validAction.append(walkValidInp)
    validAction.append(Game.checkInputLen())
    validAction.append(Game.lookInp())
    validAction.append(Game.talkInp())
    validAction.append(Game.takeInp())
    validAction.append(Game.useInp())
    validAction.append(Game.optionsInp())
    if True not in validAction:
        Game.invalidAction()
