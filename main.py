import sys

print("Welcome to SyntraZork! Input 'help' for options\n")

coor = [0,0,0] #coordinates x,y,z
roomCoorD = {(0,0,0):"Lobby",(0,0,1):"Stairs0to1"}

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
        self.longT = longT
        self.shortT = shortT
        self.lookL = lookL
        self.goL = goL

    def inRoomCheck(self,ele,rList):
        return True if ele in rList else False

    def testThis(self):
        print("test successful")

Lobby=Room(
    roomName = "Lobby",
    shortT = "You are in the lobby.",
    longT = "To your right is the reception desk."
           " A large display is hanging up high."
           "There is an ascending staircase to the first floor."
           "The exit of the building is to your south."
           "There is a bar to your west.",
    lookL = ["reception","bar","display"],
    goL = ["u","s","w"]
)

Stairs0to1=Room(
    roomName = "Stairs0to1",
    shortT = "You are in the stairwell on the first floor.",
    longT = "STILL HAVE TO WRITE THIS DESCRIPTION",
    lookL = [],
    goL = ["d"]
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
    if currentRoom.inRoomCheck(inp,currentRoom.goL):
        print("'ill doo it")
        if inp.lower() == "n": coor[1] = coor[1]+1
        if inp.lower() == "e": coor[0] = coor[0]+1
        if inp.lower() == "s": coor[1] = coor[1]-1
        if inp.lower() == "w": coor[0] = coor[0]-1
        if inp.lower() == "u": coor[2] = coor[2]+1
        if inp.lower() == "d": coor[2] = coor[2]-1
        print("it was succesful, coor=",coor)
    else: print("fuckdat",currentRoom.inRoomCheck(inp,currentRoom.goL))

def optionsInp():
    if inp.lower() == "help": helpMenu()
    if inp.lower() == "coor": print(coor)

   # if inp.lower() == "l": printIniT()

while True:
    currentRoom = roomFromCoor(coor)
    try:
        currentRoom = roomFromCoor(coor)
    except:
        print(f"ERROR! You somehow got into a place that does not exist. "
              f"You will be forever stuck at coordinates {coor}."
              f"Whoops!")

    print("currentroom= ",currentRoom.roomName)

    inp = input("\nWhat do you do? ___")
    if inp.lower() == "q": break
    walkInp()
    optionsInp()