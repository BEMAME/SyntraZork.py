print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
      "\n~~~~  Welcome to SyntraZork! Input 'help' for options  ~~~~\n"
      "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

from rooms import *



def helpMenu():
    print("n to go North\n"
          "e to go East\n"
          "s to go South\n"
          "w to go West\n"
          "u to go Up\n"
          "d to go Down\n"
          "look to look around the room\n"
          "score to display your current score\n"
          "q to quit\n")

def walkInp(): #Returns new room if valid direction input.
                # return true/false is for checking if valid input given
    if inp not in ["n", "e", "s", "w", "u", "d"]:
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
        return True, currentRoom.enterRoom()
    else:
        print(f"You cannot go that way.")
        return True,currentRoom

def optionsInp(): #various meta-options. Return true/false is for checking if valid input given
    if inp.lower() == "help":
        helpMenu()
        return True

    if inp.lower() in ["coor","where","room","location"]:
        print(f"{currentRoom.shortT} Your current coordinates are {coor}.")
        return True

    if inp.lower() in ["score","points"]:
        Player.prtScore()
        return True

    return False

def lookInp(): #looking around the room. Return true/false is for checking if valid input given
    lookSyn = ["look", "l", "info", "room", roomFromCoor(coor)]

    if inp.lower() in lookSyn:
        currentRoom.lookRoom(),
        return True
    else:
        return False

def invalidAction(): #this is called when player inputs nonsense
    print("I don't understand what you want to do.")

gameStart = True
while True:
    if gameStart == True:    #setting up the very first room at the start of the game...
        print("------------------------------------------------------------------------------------------------------")
        currentRoom = roomFromCoor(coor)
        currentRoom.enterRoom()
    gameStart = False
    inp = input("------------------------------------------------------------------------------------------------------"
            "\nWhat do you do? ___")

    if inp.lower() == "q": break #quit the game

    #this block checks what input was given and perform the action
    validAction = []
    walkValidInp, currentRoom = walkInp()
    validAction.append(walkValidInp)
    validAction.append(optionsInp())
    validAction.append(lookInp())
    if True not in validAction: invalidAction()