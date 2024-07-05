from utils import *
import numpy as np
import math 
import scipy as sp

class TestUnitary:
    """
    ## CoolingCircuit(numQubits,permutationList,coolingUnitary)

    Class for a Cooling Circuit. Create a circuit from a Permutation List or a Cooling Unitary.

    Parameters:
        numQubits (int): Number of qubits.
        permutationList (list): List to describe the states to be swapped.
        coolingUnitary (numpy.ndarray): Cooling Unitary.
    Return:
        coolingCircuit (QuantumCircuit)
    """
    #change of the probability thing 
    _coolingUnitary = None
    _excitedStateProbability = 0
    def __new__(cls,coolingUnitary=_coolingUnitary,excitedStateProbability=_excitedStateProbability):

        cls._coolingUnitary = coolingUnitary
        cls._excitedStateProbability = excitedStateProbability
        if(type(cls._coolingUnitary) is np.ndarray):
            cls.checkUnitaryNumpy(cls,cls._coolingUnitary,cls._excitedStateProbability)
        else:
            cls.checkUnitaryCSR(cls,cls._coolingUnitary,cls._excitedStateProbability)

    
    def checkUnitaryNumpy(self,m,excitedStateProbability):
        """
        Check every state after the application of the unitary
        """
        # Check if the matrix is unitary
        if(is_unitary(m) == False):
            raise ValueError("Not an unitary Matrix")        

        numberOfStates = len(m)
        numQubits = int(math.log2(numberOfStates))

        if(isinstance(excitedStateProbability, list)):
            if(len(excitedStateProbability) != numQubits):
                raise ValueError("Number of elements inside of the list is different than number of Qubits.")
        # 1 column with 2 ** NumQubits 
        state = np.zeros((numberOfStates,1))
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
                print(format(i).zfill(numOfDigits) + " | " + integerToBinary(i,numQubits) + " --> " + integerToBinary(outputState,numQubits) + " | " + str(probability))
            else:
                print(format(i).zfill(numOfDigits) + " | " + integerToBinary(i,numQubits) + " --> " + integerToBinary(outputState,numQubits) + " | " + str(probability) + " (*)")
            if(i == (numberOfStates //2)-1):
                print("Lowest Element TOP LIST: " + str(lowestElement))
                highestElement = 0
            #print(state)
            #print(matrix)

            # Return to all zero matrix
            state[i,0] = 0
        print("Highest Element BOT LIST: " + str(highestElement))

    def checkUnitaryCSR(self,m,excitedStateProbability):
            """
            Check every state after the application of the unitary
            """
            # Check if the matrix is unitary
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
                    print(format(i).zfill(numOfDigits) + " | " + integerToBinary(i,numQubits) + " --> " + integerToBinary(outputState,numQubits) + " | " + str(probability))
                else:
                    print(format(i).zfill(numOfDigits) + " | " + integerToBinary(i,numQubits) + " --> " + integerToBinary(outputState,numQubits) + " | " + str(probability) + " (*)")
                if(i == (numberOfStates //2)-1):
                    print("Lowest Element TOP LIST: " + str(lowestElement))
                    highestElement = 0
                #print(state)
                #print(matrix)

                # Return to all zero matrix
                state[i,0] = 0
            print("Highest Element BOT LIST: " + str(highestElement))
