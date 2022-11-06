import sys
from entities_objectives import *


coor = [0,0,0] #coordinates x,y,z
roomCoorD = {(0,0,0):"Lobby", #a dictionary with all the rooms in the game
             (0,1,0):"Stairs0", #this is used to determine which room the player is in based on the
             (0,1,1):"Stairs1", #coordinates
             (0,1,2):"Stairs2",
             (0,1,3):"Stairs3",
             (0,-1,0):"Outside",
             (-1,0,0):"Bar",
             (1,1,1):"Toilets"}

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
    def __init__(self,name,shortT,longT,lookL,exitsL,useL=[],askL=[],itemD={}):
        self.name = name
        self.shortT = shortT
        self.longT = longT
        self.lookL = lookL
        self.useL = useL
        self.askL = askL
        self.itemD = itemD
        self.exitsL = exitsL

    def checkIfPresent(self,ele,rList):
        return True if ele in rList else False

    def look(self):
        print(self.longT)
        if self.itemD:
            [print(values) for values in self.itemD.values()] #if there are valid items, will print description

    def enter(self): #enters the new room, prints the new room's name and looks around
        currentRoom = roomFromCoor(coor)
        print(currentRoom.shortT)
        print(currentRoom.longT)
        return currentRoom

class Stairs(Room):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

    def climbStairsExhaustion(self): #If you climb to many stairs, you will become tired
        Player.nStairsClimbed+=1
        if Player.nStairsClimbed > 2:
            manyStairsClimbed.complete()


Lobby = Room(
    name = "Lobby",
    shortT = "You are in the lobby.",
    longT = "Someone is manning the reception desk.\n"
           "A large display is hanging up high.\n"
           "To the north is an ascending staircase to the first floor.\n"
           "To the south is the exit of the building.\n"
           "There is a bar to your west.",
    lookL = ["receptionist","bar","exit","display"],
    askL = ["receptionist"],
    itemD = {"pen":"A Syntra-branded pen is laying on the reception desk."},
    exitsL = ["n","s","w"]
)

Toilets = Room(
    name = "toilets",
    shortT= "You enter the lavatory.",
    longT="You can [use] the toilets here."
          "To your west is the stairwell. It's the only exit.",
    lookL=[],
    exitsL = ["w"],
    useL=["toilet"]
)


Stairs0 = Stairs(
    name = "Stairs0",
    shortT = "You are in the stairwell on the ground floor.",
    longT = "To your south is the Lobby.\n"
            "The classrooms are upstairs.",
    lookL = [],
    exitsL = ["s","u"]
)

Stairs1=Stairs(
    name = "Stairs1",
    shortT = "You are near the stairs on the first floor.",
    longT = "The hallway to your east leads to the toilets.\n"
            "The hallway to your west has multiple classrooms.\n"
            "There are more classrooms upstairs.\n"
            "If you head down you will be in the ground floor stairwell which leads into the lobby.",
    lookL = [],
    exitsL = ["e","w","u","d"]
)

Stairs2=Stairs(
    name = "Stairs2",
    shortT = "You are near the stairs on the second floor.",
    longT = "The hallway to your west has multiple classrooms.\n"
            "There are more classrooms upstairs.\n"
            "You can take the steps back down to the first floor.",
    lookL = [],
    exitsL = ["w","u","d"]
)

Stairs3=Stairs(
    name = "Stairs3",
    shortT = "You are near the stairs on the third floor.",
    longT = "This is the top floor.\n"
            "The hallway to your west has multiple classrooms.\n"
            "You can take the steps back down to the second floor.",
    lookL = [],
    exitsL = ["w","d"]
)

Outside = Room(
    name="Outside",
    shortT="You exit the building.",
    longT="You breathe in the fresh air.\n"
          "To your north is the Syntra building.\n"
          "You contemplate if you should [go home]'.",
    lookL=[],
    exitsL=["n", "go home"]
)

Bar = Room(
    name="Bar",
    shortT="You are in a mostly empty bar.",
    longT="This is quite a spatious area. Its size accentuates its emptiness.\n"
          "A staff member is washing up behind the counter.\n"
          "To your east is the lobby.",
    lookL=["barista"],
    askL=["barista"],
    exitsL=["e"],
    itemD={"coffee": "There's a massive espresso machine in the back.",
           "beer": "A variety of beers are on display."}
)