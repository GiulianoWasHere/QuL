from collections import Counter
from scipy.constants import Planck
import numpy as np
import scipy as sp
import math
from scipy.sparse import csr_array
from .utils.utils import *

class CoolingUnitary:
    """
    ## CoolingUnitary(numQubits,swapList)
    Class for a CoolingUnitary.

    Parameters:
        numQubits (int): Number of qubits.
        swapList (list): List to describe the states to be swapped.
    
    Notes:
        Use the function .getCoolingUnitary() to get a scipy.sparse.csr_array,
        the resulting matrix can be transformed in a numpy.ndarray with
        the function .toarray().
    EXAMPLES:

    - Single Swap: `[["000","001"]] 000 <---> 001`
    - Single Swap with integer: `[[0,1]] 000 (0) <---> 001 (1)`
    - Cycle of length 3: `[["000","001","010"]] 000 --> 001 --> 010 --> 000`
    - 2 Cycles of length 2: `[["000","001"], ["010","011"]] 000 <---> 001 , 010 <---> 011`
    
    """
    
    _swapList = [["000","001"]]
    _numQubits = 3
    coolingUnitary = None

    def __init__(self,numQubits=_numQubits,swapList=_swapList):
        self._checkInputParameters(numQubits,swapList)
        self._numQubits = numQubits
        self._swapList = swapList
        self._swapList = listIntegerToBinary(self._swapList,numQubits)
        self._makeMatrix()
    
    def getUnitary(self):
        """
        Returns the Cooling Unitary.
        """
        return self.coolingUnitary
    
    def calculateWorkCost(self,excitedStateProbability,f=1):
        """
        ## calculateWorkCost(excitedStateProbability,f)
            Calculate the work cost of the Unitary.

        Parameters:
            excitedStateProbability (float): Probability of the excited state for all qubits.
            OR
            excitedStateProbability (list): Probability of the excited state for each qubit.
            (Optional) f (float): Standard resonant frequency of qubit (GHz)
        Return:
            Work Cost in micro-electronVolts(float)
        """      
        return workCost(self.coolingUnitary,excitedStateProbability,f)
    
    def getPermutations(self):
        """
        Returns a permutation list from the Cooling Unitary.
        """
        if(type(self.coolingUnitary) is np.ndarray):
            return coolingUnitaryToPermutationList(self.coolingUnitary)
        else:
            return compressedCoolingUnitaryToPermutationList(self.coolingUnitary)
        
    def dot(self,m):
        """
        Dot product between two Cooling Unitaries.
        """
        self.coolingUnitary = self.coolingUnitary.dot(m.getUnitary())
        return self
    
    def testUnitary(self,excitedStateProbability=0):
        """ 
        Testing an Unitary.
        OPTIONAL Parameters:
            excitedStateProbability (float): Probability of the excited state.
            OR
            excitedStateProbability (list): List of probability of the excited state for each qubit. 
        """
        m = self.coolingUnitary
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

    def _checkInputParameters(self,numQubits,swapList):
        """
        Private: Check of the Input parameters.
        """
        if(numQubits < 3):
            raise ValueError("Number of qubits must be greater than 2.")       
        outputMessage = "The Input Parameters are not well formatted"
        maxPossibleValue = (2 ** numQubits)
        greaterInteger = -1
        listToCount = []
        if(len(swapList) == 0):
            raise ValueError("List is empty")
        for index in range(len(swapList)):
            for i in range(len(swapList[index])):
                #Saving the greater Integer found in the list
                if(greaterInteger < binaryToInteger(swapList[index][i])):
                    greaterInteger = binaryToInteger(swapList[index][i])
                if(binaryToInteger(swapList[index][i]) < 0):
                    ValueError("Negative integer")
                listToCount.append(binaryToInteger(swapList[index][i]))
        #If the variable is -1 then it is not a string or an integer.
        #If a value is greater than 2 ^ N then error
        if(greaterInteger == -1 or greaterInteger > maxPossibleValue-1):
            raise ValueError(outputMessage)
        
        #Check if a state is repeated two times
        counts = Counter(listToCount)
        for element,count in counts.items():
            if(count > 1):
                raise ValueError("A swap state is used more than 1 time")
       
    def _makeMatrix(self):
        """
        Private: Creation of the Unitary. 
        """ 
        numOfStates = 2**self._numQubits
        #self.coolingUnitary = np.eye((numOfStates))
        row = []
        col = []
        data = [1]*numOfStates
        v = [-1] * numOfStates
        for index in range(len(self._swapList)):
            for i in range(len(self._swapList[index])-1):
                
                element = binaryToInteger(self._swapList[index][i])
                succElement = binaryToInteger(self._swapList[index][i+1])

                #Insert in the vector the element we want to swap to
                v[element] = succElement

            #Same thing as above but last state in the cycle is matched with the first one
            element = binaryToInteger(self._swapList[index][len(self._swapList[index])-1])
            firstElement = binaryToInteger(self._swapList[index][0])
            
            v[element] = firstElement

        #Using the created vector we can create the matrix
        #If v[i] == -1 the state is matched with itself, otherwise we use the vector
        #To determinate the state to swap to
        for i in range(numOfStates):
            if(v[i] == -1):
                row.append(i) 
                col.append(i) 
            else:
                row.append(v[i])
                col.append(i)
        
        self.coolingUnitary = csr_array((data, (row, col)), shape=(numOfStates, numOfStates))

def workCost(m,excitedStateProbability,f):
    """
    ## workCost(excitedStateProbability,f)
        Calculate the work cost of the Unitary.

    Parameters:
        excitedStateProbability (float): Probability of the excited state for all qubits.
        OR
        excitedStateProbability (list): Probability of the excited state for each qubit.
        (Optional) f (float): Standard Resonant frequency of qubit (GHz)
    Return:
        Work Cost (float)
    """
    if(type(m) is np.ndarray):
        l = coolingUnitaryToPermutationList(m)
        numberOfStates = len(m) 
        numQubits = int(math.log2(numberOfStates))
    elif(type(m) is sp.sparse._csr.csr_array):
        l = compressedCoolingUnitaryToPermutationList(m)
        numberOfStates = m.shape[0]
        numQubits = int(math.log2(numberOfStates))
    else:
        ValueError("Matrix is not a np.ndarray or a csr array")
    usingList = False
    if(isinstance(excitedStateProbability, list)):
        usingList = True
        if(len(excitedStateProbability) != numQubits):
            raise ValueError("Number of elements inside of the list is different than number of Qubits.")
        for i in range(len(excitedStateProbability)):
                if(excitedStateProbability[i] <= 0 or excitedStateProbability[i] >= 1):
                    raise ValueError("Probability must be greater than 0 and lower than 1.")
    else:
        if(excitedStateProbability <= 0 or excitedStateProbability >= 1):
            raise ValueError("Probability must be greater than 0 and lower than 1.")  
    workcost = 0
    for i in range(len(l)):
        for j in range(len(l[i])):
            if(j != len(l[i])-1):
                stateIn = integerToBinary(l[i][j],numQubits)
                stateOut = integerToBinary(l[i][j+1],numQubits)
            else:
                stateIn = integerToBinary(l[i][j],numQubits)
                stateOut = integerToBinary(l[i][0],numQubits)

            if(usingList):
                stateInProb = probabilityFromList(numQubits,stateIn,excitedStateProbability)
                stateOutProb = probabilityFromList(numQubits,stateOut,excitedStateProbability)
            else:
                stateInProb = (excitedStateProbability ** (numQubits - countZeros(stateIn))) * ((1 - excitedStateProbability)** countZeros(stateIn))
                stateOutProb = (excitedStateProbability ** (numQubits - countZeros(stateOut))) * ((1 - excitedStateProbability)** countZeros(stateOut))
                
            h_ueV_GHz = Planck*6.241506363094e+24*10**9
            eigenvalue = h_ueV_GHz*(f/2) * (numQubits - countZeros(stateIn)) - (countZeros(stateIn))
            workcost += eigenvalue * (stateOutProb - stateInProb)
    return workcost

def coolingUnitaryToPermutationList(m):
    """
    Returns a Permutation list from a Cooling Unitary.

    Parameters:
        CoolingUnitary (numpy.ndarray)
    Return:
        Permutation List (list)
    """
    
    statesInSwapCycle = set()
    numberOfStates = len(m)
    permutationsList = []

    for i in range(numberOfStates):
        index = i
        #If the state is NOT swapped with itself
        if(m[index][index] != 1):
            #Check if the state is NOT already inside of a swap cycle
            if(index not in statesInSwapCycle):
                l = [index]
                statesInSwapCycle.add(index)
                nextIndex = -1

                #Find this state is swapped to
                for j in range(len(m[i])):
                    if(m[j][i] == 1):
                        nextIndex = j
                        break
                #Cycle until we return to the starting state
                while(index != nextIndex):
                    l.append(nextIndex)
                    statesInSwapCycle.add(nextIndex)
                    for j in range(len(m[nextIndex])):
                        if(m[j][nextIndex] == 1):
                            nextIndex = j
                            break 
                permutationsList.append(l)

    return permutationsList

def compressedCoolingUnitaryToPermutationList(ma):
        """
        Returns a Permutation list from a Compressed Cooling Unitary.

        Parameters:
            CoolingUnitary (numpy.ndarray)
        Return:
            Permutation List (list)
        """
        
        statesInSwapCycle = set()
        m = ma.indices
        numberOfStates = len(m)
        permutationsList = []
        for index in range(numberOfStates):

            if(index != m[index]):
                #Check if the state is NOT already inside of a swap cycle
                if(index not in statesInSwapCycle):
                    l = [int(index)]
                    statesInSwapCycle.add(index)
                    nextIndex = m[index]
                    l1 = []
                    #Cycle until we return to the starting state
                    while(index != nextIndex):
                        l1.append(int(nextIndex))
                        statesInSwapCycle.add(nextIndex)
                        nextIndex = m[nextIndex]
                    permutationsList.append(l + l1[::-1])
        return permutationsList

def checkInputMatrix(m):
        """
            Check if a Matrix is Unitary.
        Parameters:
            m (numpy.ndarray or sparse._csr.csr_array): Matrix.
        Return:
            Number Of Qubits (int)
        """
        # Check if the matrix is unitary
        if(type(m) is np.ndarray):   
            if(is_unitary(m) == False):
                raise ValueError("Not an unitary Matrix")
            numberOfStates = len(m) 
            return int(math.log2(numberOfStates)),m

        if(type(m) is sp.sparse._csr.csr_array):
            x = m.conjugate().transpose().dot(m)
            y = sp.sparse.eye(x.shape[1]).tocsr()
            if(not(np.all(x.indices == y.indices) and np.all(x.indptr == y.indptr) and np.allclose(x.data, y.data))):
                raise ValueError("Not an unitary Matrix")
            numberOfStates = m.shape[0]
            return int(math.log2(numberOfStates)),m
        
        if(type(m) is CoolingUnitary):
            return m._numQubits,m.coolingUnitary

        raise ValueError("Matrix not a np.ndarray, a csr.array or a Cooling Unitary")