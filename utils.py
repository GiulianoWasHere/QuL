from collections import Counter
import numpy as np
import math 

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
        print(integerToBinary(i,numQubits) + " --> " + integerToBinary(outputState,numQubits))
        #print(state)
        #print(matrix)

        # Return to all zero matrix
        state[i,0] = 0 