import sys

print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
      "\n~~~~  Welcome to SyntraZork! Input 'help' for options  ~~~~\n"
      "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

coor = [0,0,0] #coordinates x,y,z
roomCoorD = {(0,0,0):"Lobby",
             (0,1,0):"Stairs0",
             (0,1,1):"Stairs1",
             (0,1,2):"Stairs2",
             (0,1,3):"Stairs3"}

def invalidAction():
    print("I don't understand what you want to do.")

def list2tuple(x):
    return tuple(x)

def str_to_class(str):
    return getattr(sys.modules[__name__], str)

def roomFromCoor(coor):
    roomCoorKeys = list(roomCoorD.keys())
    roomCoorVals = list(roomCoorD.values())
    position = roomCoorKeys.index(list2tuple(coor))
    currentRoom = str_to_class(roomCoorVals[position])
    return currentRoom

class Room:
    def __init__(self,roomName,shortT,longT,lookL,goL):
        self.roomName = roomName
        self.shortT = shortT
        self.longT = longT
        self.lookL = lookL
        self.goL = goL

    def inRoomCheck(self,ele,rList):
        return True if ele in rList else False

    def lookRoom(self):
        print(self.longT)

    def enterRoom(self): #enters the new room, prints the new room's name and looks around
        currentRoom = roomFromCoor(coor)
        print(currentRoom.shortT)
        print(currentRoom.longT)
        return currentRoom

class Stairs(Room):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

    def climbStairsExhaustion(self): #If you climb to many stairs, you will become tired
        global nStairsClimbed
        try:
            nStairsClimbed
        except:
            nStairsClimbed = 0
        nStairsClimbed+=1
        if nStairsClimbed == 2:
            print("You are starting to feel winded from walking up the stairs.") #TO-DOSCORE REDUCTION
        if nStairsClimbed == 3:
            print("Climbing the stairs is starting to make you sweat.") #TO-DOSCORE REDUCTION
        if nStairsClimbed > 3:
            print(f"You've climbed {nStairsClimbed} stairs... Your programmer's muscles ache.")#TO-DOSCORE REDUCTION

Lobby=Room(
    roomName = "Lobby",
    shortT = "You are in the lobby.",
    longT = " To your right is the reception desk.\n"
           " A large display is hanging up high.\n"
           " To the north is an ascending staircase to the first floor.\n"
           " To the south is the exit of the building.\n"
           " There is a bar to your west.",
    lookL = ["reception","bar","display"],
    goL = ["n","s","w"]
)

Stairs0=Stairs(
    roomName = "Stairs0",
    shortT = "You are in the stairwell on the ground floor.",
    longT = " To your south is the Lobby.\n"
            " The classrooms are upstairs.",
    lookL = [],
    goL = ["s","u"]
)

Stairs1=Stairs(
    roomName = "Stairs1",
    shortT = "You are near the stairs on the first floor.",
    longT = " The hallway to your east leads to the toilets.\n"
            " The hallway to your west has multiple classrooms.\n"
            " There are more classrooms upstairs.\n"
            " If you head down you will be in the ground floor stairwell which leads into the lobby.",
    lookL = [],
    goL = ["e","w","u","d"]
)

Stairs2=Stairs(
    roomName = "Stairs2",
    shortT = "You are near the stairs on the second floor.",
    longT = " The hallway to your west has multiple classrooms.\n"
            " There are more classrooms upstairs.\n"
            " You can take the steps back down to the first floor.",
    lookL = [],
    goL = ["w","u","d"]
)

Stairs3=Stairs(
    roomName = "Stairs3",
    shortT = "You are near the stairs on the third floor. This is the top floor.",
    longT = " The hallway to your west has multiple classrooms.\n"
            " You can take the steps back down to the second floor.",
    lookL = [],
    goL = ["w","d"]
)

def helpMenu():
    print("n to go North\n"
          "e to go East\n"
          "s to go South\n"
          "w to go West\n"
          "u to go Up\n"
          "d to go Down\n"
          "q to quit\n")

def walkInp():
    if inp not in ["n", "e", "s", "w", "u", "d"]:
        return False, currentRoom ##no valid "walk" input given
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
            currentRoom.climbStairsExhaustion() #==> invoegen wanneer speler is aangemaakt
        if inp.lower() == "d":
            coor[2] = coor[2]-1
        return True, currentRoom.enterRoom()
    else:
        print(f"You cannot go that way.")
        return True,currentRoom

def optionsInp():
    if inp.lower() == "help":
        helpMenu()
        return True

    if inp.lower() == "coor":
        print(currentRoom.roomName,coor)
        return True
    return False #no valid "options" input given

def lookInp():
    lookSyn = ["look", "l", "info", "room", roomFromCoor(coor)]
    if inp.lower() in lookSyn:
        currentRoom.lookRoom(),
        return True
    else:
        return False #no valid "look" input given

gameStart = True
while True:

    #setting up the very first room at the start of the game...
    if gameStart == True:
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