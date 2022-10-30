print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
      "\n~~~~  Welcome to SyntraZork! Input 'help' for options  ~~~~\n"
      "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

from rooms import *

class GameC:
    gameOver = False

    def __init__(self,gameStart=True):
        self.gameStart = gameStart

    def helpMenu(self):
        print("n to go North\n"
              "e to go East\n"
              "s to go South\n"
              "w to go West\n"
              "u to go Up\n"
              "d to go Down\n"
              "look to look around the room\n"
              "score to display your current score\n"
              "q to quit\n")

    def walkInp(self): #Returns new room if valid direction input.
                    # return true/false is for checking if valid input given
        if inp not in ["n", "e", "s", "w", "u", "d", "go home"]:
            return False, currentRoom
        if currentRoom.inRoomCheck(inp,currentRoom.goL):
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
            return True, currentRoom.enterRoom()
        else:
            print(f"You cannot go that way.")
            return True,currentRoom

    def optionsInp(self): #various meta-options. Return true/false is for checking if valid input given
        if inp.lower() == "help":
            Game.helpMenu()
            return True

        if inp.lower() in ["coor","where","room","location"]:
            print(f"{currentRoom.shortT} Your current coordinates are {coor}.")
            return True

        if inp.lower() in ["score","points"]:
            Player.prtScore()
            return True

        if inp.lower() in ["get points", "take points", "increase score",
                           "grab points", "cheat", "cheatcode", "cheat code"]: #an easter egg
            if Player.cheated == False:
                print("You grab some points.")
                Player.changeScore(5)
                Player.cheated = True
            else:
                print("Hey! Don't get greedy now!")
                Player.changeScore(-1)
            return True

    def lookInp(self): #looking around the room. Return true/false is for checking if valid input given
        lookSyn = ["look", "l", "info", "room", roomFromCoor(coor)]

        if inp.lower() in lookSyn:
            currentRoom.lookRoom(),
            return True
        else:
            return False

    def invalidAction(self): #this is called when player inputs nonsense
        print("I don't understand what you want to do.")


    def endGame(self):
        if Player.score < 0: #horrible ending
            print(f"You cannot bear this any longer. You make a bolt for your bicycle and ride off as fast as you can.\n"
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
    if Game.gameStart == True:    #setting up the very first room at the start of the game...
        print("------------------------------------------------------------------------------------------------------")
        currentRoom = roomFromCoor(coor)
        currentRoom.enterRoom()
    Game.gameStart = False
    inp = input("------------------------------------------------------------------------------------------------------"
            "\nWhat do you do? ___")

    if inp.lower() in ["q","quit"]: break #quit the game

    #this block checks what input was given and performs the action
    validAction = []
    walkValidInp, currentRoom = Game.walkInp()
    validAction.append(walkValidInp)
    validAction.append(Game.optionsInp())
    validAction.append(Game.lookInp())
    if True not in validAction: Game.invalidAction()
