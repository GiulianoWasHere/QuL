from collections import Counter
import numpy as np
from utils import *

class CoolingUnitary:
    """
    ## CoolingUnitary(numQubits,swapList)
    Class for a CoolingUnitary.

    Parameters:
        numQubits (int): Number of qubits.
        swapList (list): List to describe the states to be swapped.
            EXAMPLE Single Swap: [["000","001"]] 000 <---> 001
            EXAMPLE Single Swap with integer: [[0,1]] 000 (0) <---> 001 (1)
            EXAMPLE Cycle of length 3: [["000","001","010"]] 000 --> 001 --> 010 --> 000
            EXAMPLE 2 Cycles of length 2: [["000","001"], ["010","011"]] 000 <---> 001 , 010 <---> 011
    Return:
        coolingUnitary (numpy.ndarray)
    """
    
    _swapList = [["000","001"]]
    _numQubits = 3
    coolingUnitary = None

    def __new__(cls,numQubits=_numQubits,swapList=_swapList):
        """
        Parameters:
        numQubits (int): Number of qubits.
        swapList (list): List to describe the states to be swapped.
            EXAMPLE Single Swap: [["000","001"]] 000 <---> 001
            EXAMPLE Single Swap with integer: [[0,1]] 000 (0) <---> 001 (1)
            EXAMPLE Cycle of length 3: [["000","001","010"]] 000 --> 001 --> 010 --> 000
            EXAMPLE 2 Cycles of length 2: [["000","001"], ["010","011"]] 000 <---> 001 , 010 <---> 011
        """
        cls._checkInputParameters(cls,numQubits,swapList)
        cls._numQubits = numQubits
        cls._swapList = swapList
        cls._swapList = listIntegerToBinary(cls._swapList,numQubits)
        cls._makeMatrix(cls)
        return cls.coolingUnitary
    
    def _checkInputParameters(self,numQubits,swapList):
        """
        Private: Check of the Input parameters.
        """   
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
    
    def printSwapList(self):
        """
        Print swap list
        """
        print(len(self._swapList))
        for index in range(len(self._swapList)):
            stringa = ""
            for i in range(len(self._swapList[index])):
                stringa = stringa + self._swapList[index][i][-self._numQubits:] + "->"
            print( stringa + self._swapList[index][0])
            
            print("")
       

    def _makeMatrix(self):
        """
        Private: Creation of the Unitary. 
        """ 
        numOfStates = 2**self._numQubits
        self.coolingUnitary = np.eye((numOfStates))

        for index in range(len(self._swapList)):
            for i in range(len(self._swapList[index])-1):
                
                element = binaryToInteger(self._swapList[index][i])
                succElement = binaryToInteger(self._swapList[index][i+1])
                #print(element)
                #print(succElement)

                #Remove the 1 in the diagonal
                self.coolingUnitary[element,element] = 0
                #Insert the 1 in the column of the state and row of the state to swap 
                self.coolingUnitary[succElement,element] = 1

            #Same thing as above but last state in the cycle is matched with the first one
            element = binaryToInteger(self._swapList[index][len(self._swapList[index])-1])
            firstElement = binaryToInteger(self._swapList[index][0])
            
            self.coolingUnitary[element,element] = 0
            self.coolingUnitary[firstElement,element] = 1
            #print(i)     
