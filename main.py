import sys

print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
      "\n~~~~  Welcome to SyntraZork! Input 'help' for options  ~~~~\n"
      "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

coor = [0,0,0] #coordinates x,y,z
roomCoorD = {(0,0,0):"Lobby", #a dictionary with all the rooms in the game
             (0,1,0):"Stairs0", #this is used to determine which room the player is in based on the
             (0,1,1):"Stairs1", #coordinates
             (0,1,2):"Stairs2",
             (0,1,3):"Stairs3"}

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

class Protagonist:
    def __init__(self,score=0,inv=()):
        self.score = score
        self.inv = inv

    def changeScore(self,points):
        self.score = self.score + points
        if points < 0:
            print(f"Your score decreased by {abs(points)} points.\n")
        else:
            print(f"Your score increased by {points} points.\n")

    def prtScore(self):
        print (f"Your score is {self.score}.")

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
            print("You are starting to feel winded from walking up the stairs.")
            Player.changeScore(-1)
        if nStairsClimbed == 3:
            print("Climbing the stairs is starting to make you sweat.")
            Player.changeScore(-5)
        if nStairsClimbed > 3:
            print(f"You've climbed {nStairsClimbed} stairs... Your programmer's muscles ache.")
            Player.changeScore(-10)

Player = Protagonist()

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
    shortT = "You are near the stairs on the third floor.",
    longT = " This is the top floor.\n"
            " The hallway to your west has multiple classrooms.\n"
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
          "look to look around the room\n"
          "score to display your current score\n"
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

def optionsInp(): #various meta-options
    if inp.lower() == "help":
        helpMenu()
        return True

    if inp.lower() in ["coor","where","room","location"]:
        print(f"{currentRoom.shortT}. Your current coordinates are {coor}.")
        return True

    if inp.lower() in ["score","points"]:
        Player.prtScore()
        return True

    return False

def lookInp(): #looking around the room
    lookSyn = ["look", "l", "info", "room", roomFromCoor(coor)]

    if inp.lower() in lookSyn:
        currentRoom.lookRoom(),
        return True
    else:
        return False #no valid "look" input given

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