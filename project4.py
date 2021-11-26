#CSCE 1035
#Connor Applegate
#CWA0033
#connorapplegate@my.unt.edu
#This is a battleship program that allows the player 20 turns to find and sink 2 ships on the board
import sys
import random
import os

carrierHitCount = 0
battleshipHitCount = 0
destroyerHitCount = 0
submarineHitCount = 0
sunkShips = 0
torpCount = 1

# a very rudimentary way to make a nested list
gameBoard = [ ['-','-','-','-','-','-','-','-'],
              ['-','-','-','-','-','-','-','-'],
              ['-','-','-','-','-','-','-','-'],
              ['-','-','-','-','-','-','-','-'],
              ['-','-','-','-','-','-','-','-'],
              ['-','-','-','-','-','-','-','-'],
              ['-','-','-','-','-','-','-','-'],
              ['-','-','-','-','-','-','-','-'] ]

shipBoard = [ ['-','-','-','-','-','-','-','-'],
              ['-','-','-','-','-','-','-','-'],
              ['-','-','-','-','-','-','-','-'],
              ['-','-','-','-','-','-','-','-'],
              ['-','-','-','-','-','-','-','-'],
              ['-','-','-','-','-','-','-','-'],
              ['-','-','-','-','-','-','-','-'],
              ['-','-','-','-','-','-','-','-'] ]

# Nested dictionary for all ship1 types
ship1 = {
        'Carrier': {
            'name': 'C',
            'length': 5,
            'orientation': 'None',
            },
        
        'Battleship': {
            'name': 'B',
            'length': 4,
            'orientation': 'None',
            }
}

# Nested dictionary for all ship2 types
ship2 = {
        'Submarine': {
            'name': 'S',
            'length': 3,
            'orientation': 'None',
            },
        
        'Destroyer': {
            'name': 'D',
            'length': 2,
            'orientation': 'None',
            }
}
# a print function to print the game board
def printBoard(gameBoard, shipBoard, revealBoard = False):
    rowMark = 65 
    print('    0 1 2 3 4 5 6 7')
    print('  +-----------------+')
    if revealBoard == False:
        for row in range(8):
            for pos, cell in enumerate(range(11)):
                if pos > 1 and pos < 10:
                    print(gameBoard[row][cell - 2], end = ' ')
                elif pos < 1:
                    print(chr(rowMark), end = ' ')
                    rowMark += 1
                elif pos == 1:
                    print('|', end=' ')
                else:
                    print('|')
        print('  +-----------------+')
    else:
        for row in range(8):
            for pos, cell in enumerate(range(11)):
                if pos > 1 and pos < 10:
                    print(shipBoard[row][cell - 2], end = ' ')
                elif pos < 1:
                    print(chr(rowMark), end = ' ')
                    rowMark += 1
                elif pos == 1:
                    print('|', end=' ')
                else:
                    print('|')
        print('  +-----------------+')

# checks validity of user input coordinates
def validShot(shotCoordinates):
    errorCode = 0
    if len(shotCoordinates) > 2 or len(shotCoordinates) < 2:
        errorCode = 1
    elif (ord(shotCoordinates[1]) - 48) > 7:
        errorCode = 1
    elif ord(shotCoordinates[0]) < 65 or ord(shotCoordinates[0]) > 73:
        errorCode = 2
    else:
        errorCode = 0
    return errorCode

# checks if randomly assigned boundary is valid
def checkBoundary(shipType, shipName, shipRow, shipCol, shipBoard):
    check = False
    shipLength = 0
    shipOrient = getOrientation(shipType, shipName)
    
    if shipType == 1:
        shipLength = ship1[shipName]['length']
    else:
        shipLength = ship2[shipName]['length']
    
    for i in range(1):
        # check if ship is out of boundary
        if shipOrient == 'Horizontal':
            if (shipCol + shipLength) > 8:
                check = False
                break
            else:
                check = True
        else:
            if (shipRow + shipLength) > 8:
                check = False
                break
            else:
                check = True
        # check if there is another ship placed there
        for j in range(shipLength):
            tempRow = shipRow
            tempCol = shipCol

            if shipBoard[tempRow][tempCol] == '-':
                check = True
            else:
                check = False
                break

            if shipOrient == 'Horizontal':
                tempCol += 1
            else:
                tempRow += 1
    return check

# function to set the ships orientation
def setOrientation(shipCat, shipName):
    shipOrient = 'None'
    binOrient = random.randint(0,1)
    if shipCat == 'ship1':
        if binOrient == 0:
            shipOrient = 'Horizontal'
        else:
            shipOrient = 'Vertical'
        ship1[shipName]['orientation'] = shipOrient
    else:
        if binOrient == 0:
            shipOrient = 'Horizontal'
        else:
            shipOrient = 'Vertical'
        ship2[shipName]['orientation'] = shipOrient

# function to get a ships orientation
def getOrientation(shipNum, shipName):
    shipOrient = 'None'

    if shipNum == 1:
        shipOrient = ship1[shipName]['orientation']
    else:
        shipOrient = ship2[shipName]['orientation']
    return shipOrient

# function to assign vessels to a random starting location
def assignVessel(shipBoard):
    ship1Pick = random.randint(1,2)
    ship2Pick = random.randint(1,2)
    vessel1 = 'None'
    vessel2 = 'None'
    ship1Col = random.randint(0,7)
    ship1Row = random.randint(0,7)
    ship2Col = random.randint(0,7)
    ship2Row = random.randint(0,7)

    if ship1Pick == 1:
        vessel1 = 'Carrier'
        setOrientation('ship1', vessel1)
    else:
        vessel1 = 'Battleship'
        setOrientation('ship1', vessel1)
    
    if ship2Pick == 1:
        vessel2 = 'Submarine'
        setOrientation('ship2',vessel2)
    else:
        vessel2 = 'Destroyer'
        setOrientation('ship2',vessel2)
    # this for loop is redundant but I didn't wanna spend the time on fixing it
    for i in range(1):
        # assigning 1st vessel
        while True:
            ship1Col = random.randint(0,7)
            ship1Row = random.randint(0,7)
            boolTest = checkBoundary(1, vessel1, ship1Row, ship1Col, shipBoard)
            
            if boolTest == True:
                shipLength = ship1[vessel1]['length']
                shipChar = ship1[vessel1]['name']
                shipOrient = getOrientation(1, vessel1)
                if shipOrient == 'Horizontal':
                    tempCol = ship1Col
                    for x in range(shipLength):
                        shipBoard[ship1Row][tempCol] = shipChar
                        tempCol += 1
                    break
                else:
                    tempRow = ship1Row
                    for x in range(shipLength):
                        shipBoard[tempRow][ship1Col] = shipChar
                        tempRow += 1
                    break
            else:
                continue
        # assigning 2nd vessel
        while True:
            ship2Col = random.randint(0,7)
            ship2Row = random.randint(0,7)
            boolTest = checkBoundary(2, vessel2, ship2Row, ship2Col, shipBoard)
            
            if boolTest == True:
                shipLength = ship2[vessel2]['length']
                shipChar = ship2[vessel2]['name']
                shipOrient = getOrientation(2, vessel2)
                if shipOrient == 'Horizontal':
                    tempCol = ship2Col
                    for x in range(shipLength):
                        shipBoard[ship2Row][tempCol] = shipChar
                        tempCol += 1
                    break
                else:
                    tempRow = ship2Row
                    for x in range(shipLength):
                        shipBoard[tempRow][ship2Col] = shipChar
                        tempRow += 1
                    break
            else:
                continue

# get the grid type
def getGridType(colCoord, rowCoord, shipBoard):
    gridChar = shipBoard[rowCoord][colCoord]
    return gridChar

# updates global hit count
def updateHitCount(gridChar):
    global carrierHitCount
    global battleshipHitCount
    global submarineHitCount
    global destroyerHitCount

    if gridChar == 'C':
        carrierHitCount += 1
    elif gridChar == 'B':
        battleshipHitCount += 1
    elif gridChar == 'S':
        submarineHitCount += 1
    elif gridChar == 'D':
        destroyerHitCount += 1

# checks if player has won
def hasWon():
    global carrierHitCount
    global battleshipHitCount
    global submarineHitCount
    global destroyerHitCount

    boolWin = False
    if (battleshipHitCount >= 4 or carrierHitCount >= 5) and (destroyerHitCount >= 2 or submarineHitCount >= 3):
        boolWin = True
    return boolWin

def hasSunk():
    global carrierHitCount
    global battleshipHitCount
    global submarineHitCount
    global destroyerHitCount

    if battleshipHitCount == 4:
        print('You sunk my BATTLESHIP!!')
        battleshipHitCount += 1
    elif carrierHitCount == 5:
        print('You sunk my CARRIER!!')
        carrierHitCount += 1
    if destroyerHitCount == 2:
        print('You sunk my DESTROYER!!')
        destroyerHitCount += 1
    elif submarineHitCount == 3:
        print('You sunk my SUBMARINE!!')
        submarineHitCount += 1

# checks to see if torpedo shot hit or missed a target
def torpedoShot(gameBoard, shipBoard, shotCoordinates):
    shotRow = ord(shotCoordinates[0]) - 65
    shotCol = ord(shotCoordinates[1]) - 48
    gridChar = getGridType(shotCol, shotRow, shipBoard)
    if gridChar == '-':
        shipBoard[shotRow][shotCol] = 'O'
        gameBoard[shotRow][shotCol] = 'O'
        print('Miss!')
    elif ((gridChar != 'O') and ( gridChar != 'X')):
        gameBoard[shotRow][shotCol] = 'X'
        shipBoard[shotRow][shotCol] = 'X'
        updateHitCount(gridChar)
        print('Hit!')
        hasSunk()
    else:
        print('Miss!')

#Save torpCount, shipsSunk, ship(s)HitCount, both boards, and dictionaries
def writeGame(shipBoard, gameBoard, torpCount, carrierHitCount, battleshipHitCount, destroyerHitCount, submarineHitCount):
    userFile = input('Enter filename to save game: ')
    with open(userFile, 'w') as write_file:
        write_file.write(str(torpCount))
        write_file.write('\n')
        write_file.write(str(carrierHitCount))
        write_file.write('\n')
        write_file.write(str(battleshipHitCount))
        write_file.write('\n')
        write_file.write(str(destroyerHitCount))
        write_file.write('\n')
        write_file.write(str(submarineHitCount))
        write_file.write('\n')
        for row in shipBoard:
            for col in row:
                write_file.write(str(col))
            write_file.write('\n')
        for row in gameBoard:
            for col in row:
                write_file.write(str(col))
            write_file.write('\n')



#Opens user file and assigns relevant data to file contents
def readGame(filePath):
    global shipBoard
    global torpCount
    global carrierHitCount
    global submarineHitCount
    global destroyerHitCount
    global battleshipHitCount
    fileContent = [] 
    with open(filePath, 'r') as read_file:
        fileContent = read_file.readlines()
    torpCount = int(fileContent[0])
    carrierHitCount = int(fileContent[1])
    battleshipHitCount = int(fileContent[2])
    destroyerHitCount = int(fileContent[3])
    submarineHitCount = int(fileContent[4])
    for row, i in enumerate(range(8)):
        shipBoard[row] = list(fileContent[i+5])
    for row, i in enumerate(range(8)):
        gameBoard[row] = list(fileContent[i+13])
        

print('CSCE 1035\nConnor Applegate\nCWA0033\nconnorapplegate@my.unt.edu\n\n')

if len(sys.argv) != 2:
    assignVessel(shipBoard)
elif len(sys.argv) == 2:
    if os.path.exists(sys.argv[1]):
        readGame(sys.argv[1])
    else:
        print('File does not exist: {}'.format(sys.argv[1]))
        userChoice = input('Do you want to start a new game? (Y/N): ')
        if userChoice == 'Y':
            assignVessel(shipBoard)
        else:
            print('User terminated program.... goodbye!')
            sys.exit()

while torpCount <= 20:
    printBoard(gameBoard, shipBoard)
    while True:
        print('Enter grid coordinates to fire torpedo #{} (e.g., B4): '.format(torpCount), end='')
        shotCoordinates = input()
        if shotCoordinates == 'SAVE':
            writeGame(shipBoard, gameBoard, torpCount, carrierHitCount, battleshipHitCount, destroyerHitCount, submarineHitCount)
            sys.exit()
        else:
            errorCode = validShot(shotCoordinates)
            if errorCode == 1:
                print('Invalid column type, please try again')
                continue
            elif errorCode == 2:
                print('Invalid row type, please try again')
                continue
            else:
                torpedoShot(gameBoard, shipBoard, shotCoordinates)
                torpCount += 1
                boolWin = hasWon()
                break
    if boolWin == True:
        print('You won, congratulations! You sank both ships in {} tries!'.format(torpCount - 1))
        break
if (boolWin == False) and (torpCount > 20):
    print('Sorry, you lost, better luck next time!')
    printBoard(gameBoard, shipBoard, True)
