from collections import Counter
import numpy as np
import math 

##Not the right place to put this 

def printOccupationProbabilitiesList(list):
    for i in range(len(list)):
        print(str(i), end=" | ")
        print(list[i])
        if(i == len(list)//2 - 1 ):
            print("-----------------")

def printOccupationProbabilitiesList2(list,t,j):
    for i in range(len(list)):
        print(str(i), end=" | ")
        print(list[i],end="")
        if(t == i):
            print("*",end="")
        if(i == j):
            print("*",end="")
        print()

def subSetsOfSwaps(l):
        """
        Creation of subsets of swaps by a list of swaps.
        """
        subsets = [[]]
        dictionary  = {}
        numOfSubsets = 0
        #We put every swap inside of a dictionary until we find a repeated state. 
        #When we find a repeated state we reset the dictionary and create a sublist
        for i in range(len(l)):
            reset = 0
            if l[i][0] not in dictionary:
                dictionary[l[i][0]] = 0
            else:
                reset = 1
            if l[i][1] not in dictionary:
                dictionary[l[i][1]] =  0
            else:
                reset = 1

            if(reset == 1):
                dictionary = {}
                dictionary[l[i][0]] = 0
                dictionary[l[i][1]] = 0
                numOfSubsets += 1
                subsets.append([])
            subsets[numOfSubsets].append(l[i])

        return subsets
###

def invertState(s):
    string = list(s)
    for i in range(len(string)):
        if(string[i] == '0'):
            string[i] = '1'
        else:
            string[i] = '0'
    s = "".join(string)
    return s
def countZeros(string):
    count = 0
    for i in range(len(string)):
        if(string[i]=="0"):
            count+=1
    return count

def integerToBinary(integer,numOfBits):
    if isinstance(integer, int):
        binaryNumber = format(integer, '0'+ str(numOfBits) +'b')
    else:
        binaryNumber = integer
    return binaryNumber

def listIntegerToBinary(lista,numOfBits):
    for i in range(len(lista)):
        lista[i] = integerToBinary(lista[i],numOfBits)
    return lista

def binaryToInteger(binary_string):
    if isinstance(binary_string, int):  
        return binary_string  
    return int(binary_string, 2)    

def is_unitary(m):
    """
    Check if matrix is unitary
    """
    return np.allclose(np.eye(m.shape[0]), m.conj(m).T.dot(m))

def checkUnitary(m):
    """
    Check every state after the application of the unitary
    """

    # Check if the matrix is unitary
    if(is_unitary(m) == False):
        raise ValueError("Not an unitary Matrix")
    

    numberOfStates = len(m)
    numQubits = int(math.log2(numberOfStates))
    # 1 column with 2 ** NumQubits 
    state = np.zeros((numberOfStates,1))
    
    for i in range(numberOfStates):
        # i = 0,  State 00 = [1 0 0 0] 
        # i = 1,  State 01 = [0 1 0 0] 

        #Application of the unitary
        state[i,0] = 1 
        matrix = m.dot(state) 
        indices = np.where(matrix == 1)

        #Probably not necessary
        if len(indices[0]) > 1:
            raise ValueError("Error")
            
        outputState = int(indices[0][0])
        if(outputState == i):
            print(str(i) + " | " + integerToBinary(i,numQubits) + " --> " + integerToBinary(outputState,numQubits))
        else:
            print(str(i) + " | " + integerToBinary(i,numQubits) + " --> " + integerToBinary(outputState,numQubits) + " (*)") 
        if(i == (numberOfStates //2)-1):
            print("-------------------------")
        #print(state)
        #print(matrix)

        # Return to all zero matrix
        state[i,0] = 0 

def checkUnitary2(m,excitedStateProbability):
    """
    Check every state after the application of the unitary
    """

    # Check if the matrix is unitary
    if(is_unitary(m) == False):
        raise ValueError("Not an unitary Matrix")
    

    numberOfStates = len(m)
    numQubits = int(math.log2(numberOfStates))
    # 1 column with 2 ** NumQubits 
    state = np.zeros((numberOfStates,1))
    for i in range(numberOfStates):
        # i = 0,  State 00 = [1 0 0 0] 
        # i = 1,  State 01 = [0 1 0 0] 

        #Application of the unitary
        state[i,0] = 1 
        matrix = m.dot(state) 
        indices = np.where(matrix == 1)

        #Probably not necessary
        if len(indices[0]) > 1:
            raise ValueError("Error")
        
        
        outputState = int(indices[0][0])
        numberOfZeros = countZeros(integerToBinary(outputState,numQubits))
        probability = (excitedStateProbability ** (numQubits - numberOfZeros)) * ((1 - excitedStateProbability)** numberOfZeros)
        if(outputState == i):
            print(str(i) + " | " + integerToBinary(i,numQubits) + " --> " + integerToBinary(outputState,numQubits) + " | " + str(probability))
        else:
            print(str(i) + " | " + integerToBinary(i,numQubits) + " --> " + integerToBinary(outputState,numQubits) + " | " + str(probability) + " (*)")
        if(i == (numberOfStates //2)-1):
            print("-------------------------")
        #print(state)
        #print(matrix)

        # Return to all zero matrix
        state[i,0] = 0 
        