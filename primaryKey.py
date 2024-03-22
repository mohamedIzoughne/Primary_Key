# to get the key we need to have all functional dependecies, try them

# first we need to check the element that does exist in the right hand side

# get every possibility

# now we have all the candidate keys

# check for minimal key

relationAttributes = input("Enter a relation please: ") 
relationAttributes = list(relationAttributes)
relationLength = len(relationAttributes)

functionalDependencies = input("please Enter functional dependencies separated by comma(for ex: AB: C, BC: D): ")
functionalDependencies = functionalDependencies.split(',') 
functionalDependenciesDict = {}

# AllPossibleKeysDict = {}


for fd in functionalDependencies:
    dependenciesList = fd.split(':')

    key = dependenciesList[0]
    value = dependenciesList[1]

    strippedKey = key.strip() 
    strippedValue = value.strip()
    functionalDependenciesDict[strippedKey] = strippedValue


# make all possible combinations
def getCombinations(targetSet, attr = '', index = 0):
    if len(attr) == relationLength:
        return
    
    newAttr = attr
    for i in range(index, relationLength): # Here we start from index because AB for example BA
        if  relationAttributes[i] not in newAttr:
            newAttr = attr + relationAttributes[i]
            sortedAttr = sorted(newAttr) ## returns a list
            sortedAttr = ''.join(sortedAttr)
            targetSet.add(sortedAttr)
        getCombinations(targetSet, newAttr, index + 1)
    return targetSet


def checkIfExists(attributes, attrToBeChecked): ## check if each attribute exist inside attrToCheck
    attrExists = True
    for part in attributes:
        if part not in attrToBeChecked:
            attrExists = False
            break
    
    return attrExists


def filterKeysByRHS(possibleKeys, rightHandSideAttributes):
    if(len(rightHandSideAttributes) == 0): return possibleKeys
    rightHandSideAttributes = ''.join(rightHandSideAttributes)
    filteredPossibleKeys = [] 

    for candidate in possibleKeys:
        if checkIfExists(rightHandSideAttributes, candidate):
            filteredPossibleKeys.append(candidate)
    
    return filteredPossibleKeys

def getRightHandSide():
    existRHS = functionalDependenciesDict.values()
    existRHS = ''.join(existRHS)

    nonExistentRHS = [] 

    for attr in relationAttributes: 
        if attr not in existRHS:
            nonExistentRHS.append(attr)
    
    return nonExistentRHS

## ---- now we should get all the keys after the closure
## first have all the keys of functional dependencies(LHS)
## if the LHS  of a certain functional dependency exist inside a possibility: 
# then take the RHS OF THAT LHS and put it into a set
# then after the iteration

def getPossibleValues(keyToBeComputed, LHSKeys):
    # initialLHSKeys = LHSKeys.copy()
    # initialPossibleValues = possibleValues.copy()
    possibleValues = set(keyToBeComputed)
    isChecked = False
    LHSKeys = list(LHSKeys) # to iterate
    notUsed = set(LHSKeys)
    ## for example if we used AB -> C, then we will not need to loop again and insert elements that do not exist
    
    i = 0
    while i < len(LHSKeys):
        key = LHSKeys[i]
        if key in notUsed and checkIfExists(key, possibleValues):
            possibleValues.update(list(functionalDependenciesDict[key]))
            notUsed.remove(key)
            isChecked = True
        
        if i == len(LHSKeys) - 1 and isChecked:
            i = 0
            isChecked = False
        else:
            i += 1

    return possibleValues

def computeClosure(keyToBeComputed):
    ## Mistakes I made in code:
    ## - we don't start for all the places
    ## - we should always check the other ones, I mean make new loops so that I check if I have another thing
    ## for this mission we should use a variable and then check if it is true or false, for example: isChecked
    LHSKeys = functionalDependenciesDict.keys() 

    computedClosureValues = getPossibleValues(keyToBeComputed, LHSKeys)

    return computedClosureValues


def getPrimaryKeys(allCombinations):
    primaryKeys = []
    for combination in allCombinations:
        computedValues = computeClosure(combination) 
        computedValuesSize = len(computedValues)

        if(computedValuesSize == relationLength):
            primaryKeys.append(combination)

    return primaryKeys

def turnIntoMinimal(keys):
    keys = list(keys) ## to iterate using index
    minimalKeys = keys.copy()

    def checkIfEveryPartExists(keyToCheck, keyToBeChecked):
        for part in keyToCheck:
            if part not in keyToBeChecked:
                return False
        return True
    
    for i in range(len(keys)):
        minimal = keys[i]
        for j in range(len(keys)):
            if j != i and checkIfEveryPartExists(keys[j], minimal):
                minimalKeys.remove(minimal)
                break
    
    return minimalKeys

AllPossibleKeys = set() 
combinations = getCombinations(AllPossibleKeys) 
rightHandSideValues = getRightHandSide() 
filteredCombinations = filterKeysByRHS(combinations, rightHandSideValues)

primaryKeys = getPrimaryKeys(filteredCombinations)
minimalKeys = turnIntoMinimal(primaryKeys)

print("---------------------------------------------")
print(f"Primary Keys: {primaryKeys}")
print('----------')
print(f"minimal Keys: {minimalKeys}")