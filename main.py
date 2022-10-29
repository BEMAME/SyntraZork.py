print("Welcome to SyntraZork! Input 'help' for options")

coor = [0,0,0] #coordinates x,y,z
roomCoorD = {(0,0,0):"Lobby",(0,0,1):"Stairs0to1"}

def list2tuple(x):
    return tuple(x)

def checkIn(ele,target):
    return True if list2tuple(ele) in target else False

def roomFromCoor(coor):
    roomCoorKeys = list(roomCoorD.keys())
    roomCoorVals = list(roomCoorD.values())
    position = roomCoorKeys.index(coor)
    currentRoom = roomCoorVals[position]
    return currentRoom

class Room:
    def __init__(self,roomName,roomCoor,shortT,longT,lookL,goL):
        self.roomName = roomName
        self.roomCoor = roomCoor
        self.longT = longT
        self.shortT = shortT
        self.lookL = lookL
        self.goL = goL

    def inRoomCheck(self,ele,rList):
        if ele not in rList:
            print(f"There is no {ele} in the {self.roomName}")

    def testThis(self):
        print("test successful")

Lobby=Room(
    roomName = "Lobby",
    roomCoor = [0,0,0],
    shortT = "You are in the lobby.",
    longT = "To your right is the reception desk."
           " A large display is hanging up high."
           "There is an ascending staircase to the first floor."
           "The exit of the building is to your south."
           "There is a bar to your west.",
    lookL = ["reception","bar","display"],
    goL = ["u","s","w"]
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
#    print(currentRoom.inRoomCheck(ele=))
    if currentRoom.inRoomCheck(inp,currentRoom.goL):
        if inp.lower() == "n": coor[1] = coor[1]+1
        if inp.lower() == "e": coor[0] = coor[0]+1
        if inp.lower() == "s": coor[1] = coor[1]-1
        if inp.lower() == "w": coor[0] = coor[0]-1
        if inp.lower() == "u": coor[2] = coor[2]+1
        if inp.lower() == "d": coor[2] = coor[2]-1
    else: pass

def optionsInp():
    if inp.lower() == "help": helpMenu()
    if inp.lower() == "coor": print(coor)

   # if inp.lower() == "l": printIniT()

while True:
    print(checkIn(coor,roomCoorD))
    try:
        currentRoom = roomFromCoor(list2tuple(coor))
    except:
        print(f"ERROR! You somehow entered a place that does not exist. Whoops! Coor = {coor}")
    print("currentroom= ",currentRoom)

    inp = input("\nWhat do you do? ___")
    print("inp = ",inp)
    print(Lobby.testThis())
    print(type(currentRoom))
    print(currentRoom.testThis())
    if inp.lower() == "q": break
    walkInp()
    optionsInp()
