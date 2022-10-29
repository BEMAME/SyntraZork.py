from main import *

print("Welcome to SyntraZork! Input 'help' for options\n")

Lobby=Room(
    roomName = "Lobby",
    shortT = "You are in the lobby.",
    longT = "To your right is the reception desk."
           " A large display is hanging up high."
           "To the [n]orth is an ascending staircase to the first floor."
           "To the [s]outh is the exit of the building."
           "There is a bar to your [w]est.",
    lookL = ["reception","bar","display"],
    goL = ["n","s","w"]
)

Stairs0=Room(
    roomName = "Stairs0",
    shortT = "You are in the stairwell on the ground floor.",
    longT = "To your [s]outh is the Lobby."
            "There are classrooms are [u]pstairs.",
    lookL = [],
    goL = ["s","u"]
)

def walkInp():
    if currentRoom.inRoomCheck(inp,currentRoom.goL):
        if inp.lower() == "n":
            coor[1] = coor[1]+1
            return True
        if inp.lower() == "e":
            coor[0] = coor[0]+1
            return True
        if inp.lower() == "s":
            coor[1] = coor[1]-1
            return True
        if inp.lower() == "w":
            coor[0] = coor[0]-1
            return True
        if inp.lower() == "u":
            coor[2] = coor[2]+1
            return True
        if inp.lower() == "d":
            coor[2] = coor[2]-1
            return True
    else:
        return False

def optionsInp():
    if inp.lower() == "help":
        helpMenu()
        return True

    if inp.lower() == "coor":
        print(coor)
        return True

    return False

def lookInp():
    lookSyn = ["look", "l", "info", "room", roomFromCoor(coor)]
    if inp.lower() in lookSyn:
        currentRoom.lookRoom(),
        return True
    else:
        return False

currentRoom = roomFromCoor(coor)


while True:
    validAction = [False]
    currentRoom = roomFromCoor(coor)
    currentRoom.enterRoom()
    try:
        currentRoom = roomFromCoor(coor)
    except:
        print(f"ERROR! You somehow got into a place that does not exist. "
              f"You will be forever stuck at coordinates {coor}."
              f"Whoops!")

    inp = input("\nWhat do you do? ___")
    if inp.lower() == "q": break
    validAction.append(walkInp())
    validAction.append(optionsInp())
    validAction.append(lookInp())
    if True not in validAction: invalidAction()