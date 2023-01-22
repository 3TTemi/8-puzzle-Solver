
class nodeState: 
    
    def __init__(self , stateArray, level, parent, fVal, posBlank):
        self.stateArray = stateArray
        self.level = level 
        self.parent = parent 
        self.fVal = fVal
        self.posBlank = posBlank


    def printState(self): 
        for row in range(len(self.stateArray)):
            for col in range(len(self.stateArray[0])):
                print(self.stateArray[row][col], end =" ") 
            print()

def isGoal(testArray): 
    goalArray = [[1,2,3], [4,5,6], [7,8,0]]
    sameArray = True  
    for row in range(len(testArray)):
        for col in range(len(testArray[0])): 
            if testArray[row][col] != goalArray[row][col]:
                sameArray = False
    return sameArray 

def printArray(twoArray):
    for row in range(len(twoArray)):
        for col in range(len(twoArray[0])):
            print(twoArray[row][col], end =" ") 
        print()

def manhattanDistance(arrayState):
    goalArray = [[1,2,3], [4,5,6], [7,8,0]]
    goalDict = {} 
    for row in range(len(goalArray)):
        for col in range(len(goalArray[0])):
            goalDict[goalArray[row][col]] = (row,col)
    positionDistance = []
    for row in range(len(arrayState)):
        for col in range(len(arrayState[0])):
            data = arrayState[row][col]
            xgoal = goalDict[data][1]
            ygoal = goalDict[data][0]
            positionDistance.append(abs(col - xgoal) + abs(row - ygoal))
    return sum(positionDistance)
            
def sameArray(list1, list2): 
    if len(list1) != len(list2) or len(list1[0]) != len(list2[0]):
        return False
    for row in range(len(list1)):
        for col in range(len(list1[0])): 
            if list1[row][col] != list2[row][col]:
                return False
    return True

def findCanidates(arrayState):
    pos = ()
    canidateList = []
    for row in range(len(arrayState)):
        for col in range(len(arrayState[0])):
            if arrayState[row][col] == 0:
                pos = (row, col) 
    for row in range (pos[0] - 1, pos[0] + 2):
        for col in range(pos[1] - 1, pos[1] + 2):
            if (row < len(arrayState) and row >= 0) and (col < len(arrayState[0]) and col >= 0) and (row != pos[0] or col != pos[1]) and (row == pos[0] or col == pos[1]):
                canidateList.append((row,col))
    return canidateList

def moveArray(arr, posInit, posNew):
    temp = arr[posInit[0]][posInit[1]]
    arr[posInit[0]][posInit[1]] = arr[posNew[0]][posNew[1]] 
    arr[posNew[0]][posNew[1]] = temp 
    return arr

def generateNodes(movesList, currentNode, statesVisited, leavesList):
    gValue = currentNode.level + 1    
    for i in range (len(movesList)):
        isUnique = True
        copyArray = [item[:] for item in currentNode.stateArray]
        movedArray = moveArray(copyArray,currentNode.posBlank,movesList[i])
        for j in range(len(statesVisited)):
            if sameArray(movedArray, statesVisited[j]):
                isUnique = False
                break
        if isUnique == True:
            hValue = manhattanDistance(movedArray)
            newPuzzle = nodeState(movedArray, gValue, currentNode, gValue + hValue, movesList[i])
            leavesList.append(newPuzzle)
    return leavesList

def Astar(curPuzzle):
    goalFound = False
    if isGoal(curPuzzle.stateArray): 
        print ("Goal State is the Initial state") 
        print ("Number of moves: 0") 
        return
    else: 
        leavesList = []
        gValue = curPuzzle.level
        hValue = manhattanDistance(curPuzzle.stateArray)
        fValue = gValue + hValue 
        selectedState = curPuzzle
        curPuzzle.fVal = fValue 
        statesVisited = []
        statesVisited.append(selectedState.stateArray)
        while goalFound == False: 
            isSameArray = False
            moves = findCanidates(selectedState.stateArray)
            newLeaves = generateNodes(moves, selectedState, statesVisited, leavesList)
            newLeaves.sort(key = lambda leaf: leaf.fVal)
            selectedState = newLeaves[0]
            newLeaves.pop(0)
            if isGoal(selectedState.stateArray):
                goalFound = True 
            for j in range(len(statesVisited)):
                if sameArray(selectedState.stateArray, statesVisited[j]):
                    isSameArray = True
                    break
            if isSameArray == False:
                statesVisited.append(selectedState.stateArray)

        print ("---- Reached the Goal State ----")
        print("Number of moves: " + str(selectedState.level))
        finalMoveList = []
        while(selectedState.parent != None):
            stepDirect = None
            curPos = selectedState.posBlank 
            selectedState = selectedState.parent
            if selectedState.posBlank[0] == curPos[0] - 1 and selectedState.posBlank[1] == curPos[1]:
                stepDirect = "Down"
            elif selectedState.posBlank[0] == curPos[0] + 1 and selectedState.posBlank[1] == curPos[1]:
                stepDirect = "Up"
            elif selectedState.posBlank[0] == curPos[0] and selectedState.posBlank[1] == curPos[1] - 1:
                stepDirect = "Right"
            elif selectedState.posBlank[0] == curPos[0] and selectedState.posBlank[1] == curPos[1] + 1:
                stepDirect = "Left"
            finalMoveList.insert(0, stepDirect)
        print(finalMoveList)            

        
def main():
    initPuzzle = nodeState([[8,3,2],[4,7,1],[0,5,6]], 0, None, 0, (2,0))
    print("Current State: ")
    initPuzzle.printState()
    print("")
    Astar(initPuzzle)

main()

