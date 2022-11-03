print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
      "\n~~~~  Welcome to SyntraZork! Input 'help' for options  ~~~~\n"
      "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

from rooms import *

class GameC:
    gameOver = False
    lookAt = ""
    askPerson = ""

    def __init__(self,gameStart=True):
        self.gameStart = gameStart

    def synonymCheck(self,inputVal):
        try:
            x = [target for target, syn in entitySyn.items() if inputVal in syn][0]
            return x #this returns the key of the entitySyn dictionary
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
              "[look <object>] to look at an object. This command should always be two words; e.g. 'look table'.\n"
              "[i] to show a list of items that are in your backpack."
              "[score] to display your current score\n"
              "[q] to quit")

    def walkInp(self): #Returns new room if valid direction input.
                    # return true/false is for checking if valid input given
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
            if inp.lower() == "go home": #this can only be selected from the "Outside" room
                Game.endGame()
            return True, currentRoom.enter()
        else:
            print(f"You cannot go that way.")
            return True,currentRoom

    def optionsInp(self): #various meta-options. Return true/false is for checking if valid input given
        if inp.lower() == "help":
            Game.helpMenu()
            return True

        if inp.lower() in ["coor","where","location"]:
            print(f"{currentRoom.shortT} Your coordinates are {coor}.")
            return True

        if inp.lower() in ["score","points"]:
            Player.prtScore()
            return True

        if inp.lower() in ["i","inv","inventory","backpack"]:
            Player.inventory()
            return True

        # an easter egg
        if inp.lower() in ["get points", "take points", "increase score",
                           "grab points", "cheat", "cheatcode", "cheat code"]:
            if Player.cheated == False:
                print("You grab some points.")
                Player.changeScore(5)
                Player.cheated = True
            else:
                print("Hey! Don't get greedy now!")
                Player.changeScore(-1)
            return True

    # looking around the room. Return true/false is for checking if valid input given
    def lookInp(self):
        # player did not type something that started with "look..."
        if inp.lower().startswith("look") is False:
            return False

        # player typed "look" or "look room" ==> give description of room
        if len(inp.split()) == 1 or inp.lower() == "look room":
            currentRoom.look()

        # player typed "look <something>"
        elif len(inp.split()) == 2:
            self.lookAt = inp.split()[1].lower()
            x = self.synonymCheck(self.lookAt)
            if x in currentRoom.lookL or self.lookAt in Player.inv:
                str_to_class(x).look()

            else:
                print("I don't know how to look at that.")

        # player typed more than 2 words, syntax incorrect
        else:
            print("You typed too many words. To look at something, type 'look <object>', e.g. 'look table'")

        return True

    def askInp(self):
        # player did not type something that started with "ask..."
        if inp.lower().startswith("ask") is False:
            return False

        if len(inp.split()) == 1:
            print("Who are you going to ask?")

        elif len(inp.split()) == 2:
            self.askPerson = inp.split()[1].lower()
            x = self.synonymCheck(self.askPerson)
            if x in currentRoom.askL:
                str_to_class(x).ask()
            else:
                print(f"{x.capitalize()} isn't feeling very talkative.")

        else:
            print("You typed too many words. To ask someone a question, type 'ask <person>', e.g. 'ask receptionist'")

        return True

    def invalidAction(self):
        print("I don't understand what you want to do. Type [help] for a list of basic commands.")

    def endGame(self):
        if Player.score < 0: #horrible ending
            print(f"You cannot bear this any longer. You run towards your bicycle and ride off as fast as you can.\n"
                  f"When you look behind you, you see the Syntra building disappear behind the horizon.\n"
                  f"You swear never to return again.")
        if 0 >= Player.score <= 10: #bad ending
            print(f"You sigh as walk towards your bicycle. You don't feel like you've learned much today.\n"
              "On the way home, you contemplate quitting the Python for beginners course.")
        if Player.score > 10: #good ending
            print(f"Satisfied, you walk towards your bicycle.\n"
              "On the way home, many ideas for your Python project come to mind.\n"
              "You jot them down on a piece of paper before you go to bed.")

        print(f"\n ~~You finished the game with a score of {Player.score}! Thanks for playing!")

        self.gameOver = True

        sys.exit()

Game = GameC()

while True:
    # setting up the very first room at the start of the game...
    if Game.gameStart == True:
        print("------------------------------------------------------------------------------------------------------")
        currentRoom = roomFromCoor(coor)
        print("A few weeks ago, you registered for the Syntra 'Python for Beginners' class.\n"
              "Full of excitement you enter the Syntra lobby. Classes start in 5 minutes.\n"
              "You should [look] around to find out where to go.")
        #currentRoom.enter()
    Game.gameStart = False
    inp = input("------------------------------------------------------------------------------------------------------"
            "\nWhat do you do? ___")
    #

    if inp.lower() in ["q","quit"]: break #quit the game

    #this block checks what input was given and performs the action
    validAction = []
    walkValidInp, currentRoom = Game.walkInp()
    validAction.append(walkValidInp)
    validAction.append(Game.lookInp())
    validAction.append(Game.askInp())
    validAction.append(Game.optionsInp())
    if True not in validAction: Game.invalidAction()