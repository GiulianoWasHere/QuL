from utils import *
import numpy as np
import math 
import scipy as sp

class TestUnitary:
    """
    ## TestUnitary(coolingUnitary,excitedStateProbability)

    Class for Testing an Unitary.

    Parameters:
        coolingUnitary (numpy.ndarray): Cooling Unitary.
        OPTIONAL:
        excitedStateProbability (float): Probability of the excited state.
        OR
        excitedStateProbability (list): List of probability of the excited state for each qubit.
    Return:
        True
    """
    #change of the probability thing 
    _coolingUnitary = None
    _excitedStateProbability = 0
    def __new__(cls,coolingUnitary=_coolingUnitary,excitedStateProbability=_excitedStateProbability):

        cls._coolingUnitary = coolingUnitary
        cls._excitedStateProbability = excitedStateProbability
        cls.checkUnitary(cls,cls._coolingUnitary,cls._excitedStateProbability)
        return True

    
    def checkUnitary(self,m,excitedStateProbability):
        """
        Check every state after the application of the unitary
        """
        # Check if the matrix is unitary
        if(type(m) is np.ndarray):   
            if(is_unitary(m) == False):
                raise ValueError("Not an unitary Matrix")
            numberOfStates = len(m) 
        else:
            x = m.conjugate().transpose().dot(m)
            y = sp.sparse.eye(x.shape[1]).tocsr()
            if(not(np.all(x.indices == y.indices) and np.all(x.indptr == y.indptr) and np.allclose(x.data, y.data))):
                raise ValueError("Not an unitary Matrix")
            numberOfStates = m.shape[0]

        numQubits = int(math.log2(numberOfStates))

        if(isinstance(excitedStateProbability, list)):
            if(len(excitedStateProbability) != numQubits):
                raise ValueError("Number of elements inside of the list is different than number of Qubits.")
        # 1 column with 2 ** NumQubits 
        state = np.zeros((numberOfStates,1))
        lowestTopHalf = 99
        highestTopHalf = 0
        lowestElement = 99
        highestElement = 0
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
            if(isinstance(excitedStateProbability, list)):
                numberInBinary = integerToBinary(outputState,numQubits)
                probability = 1
                for j in range(numQubits):
                    if(numberInBinary[j] == "1"):
                        probability *= excitedStateProbability[j]
                    else:
                        probability *= (1-excitedStateProbability[j])    
                probability = round(probability,numQubits+3)
            else:
                probability = (excitedStateProbability ** (numQubits - numberOfZeros)) * ((1 - excitedStateProbability)** numberOfZeros)

            if(lowestElement > probability):
                lowestElement = probability
            if(highestElement < probability):
                highestElement = probability
                #print(highestElement)
            numOfDigits = len(str(numberOfStates))
            if(outputState == i):
                if(excitedStateProbability == 0):
                    print(format(i).zfill(numOfDigits) + " | " + integerToBinary(i,numQubits) + " --> " + integerToBinary(outputState,numQubits))
                else:
                    print(format(i).zfill(numOfDigits) + " | " + integerToBinary(i,numQubits) + " --> " + integerToBinary(outputState,numQubits) + " | " + str(probability))
            else:
                if(excitedStateProbability == 0):
                    print(format(i).zfill(numOfDigits) + " | " + integerToBinary(i,numQubits) + " --> " + integerToBinary(outputState,numQubits) + " (*)")
                else:
                    print(format(i).zfill(numOfDigits) + " | " + integerToBinary(i,numQubits) + " --> " + integerToBinary(outputState,numQubits) + " | " + str(probability) + " (*)")
            if(i == (numberOfStates //2)-1):
                print("--------------------------")
                lowestTopHalf = lowestElement
                highestTopHalf = highestElement
                lowestElement = 99
                highestElement = 0
            #print(state)
            #print(matrix)

            # Return to all zero matrix
            state[i,0] = 0
        if(excitedStateProbability != 0):
            print("Lowest Element TOP LIST: " + str(lowestTopHalf))
            print("Highest Element TOP LIST: " + str(highestTopHalf))
            print("Lowest Element BOT LIST: " + str(lowestElement))
            print("Highest Element BOT LIST: " + str(highestElement))