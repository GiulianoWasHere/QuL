from collections import Counter
import numpy as np

#GLOBAL METHODS MOVE THEM SOMEWHERE
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

def checkUnitary(m,numQubits):
    """
    Check every state after the application of the unitary
    """

    # Check if the matrix is unitary
    if(is_unitary(m) == False):
        raise ValueError("Not an unitary Matrix")
    

    numberOfStates = 2 ** numQubits 
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


class CoolingUnitary:
    """
    # CoolingUnitary(numQubits,swapList)
    numQubits: Number of qubits.
    swapList: List to describe the states to be swapped.
    EXAMPLE Single Swap: [["000","001"]] 000 <---> 001
    EXAMPLE Single Swap with integer: [[0,1]] 000 (0) <---> 001 (1)
    EXAMPLE Cycle of length 3: [["000","001","010"]] 000 --> 001 --> 010 --> 000
    EXAMPLE 2 Cycles of length 2: [["000","001"], ["010","011"]] 000 <---> 001 , 010 <---> 011
    """
    
    _swapList = [["000","001"]]
    _numQubits = 3
    coolingUnitary = None

    #def __init__(self, numQubits=_numQubits,swapList=_swapList):
    #    """
    #    numQubits: Number of qubits.
    #    swapList: List to describe the states to be swapped.
    #    EXAMPLE Single Swap: [["000","001"]] 000 <---> 001
    #    EXAMPLE Single Swap with integer: [[0,1]] 000 (0) <---> 001 (1)
    #    EXAMPLE Cycle of length 3: [["000","001","010"]] 000 --> 001 --> 010 --> 000
    #    EXAMPLE 2 Cycles of length 2: [["000","001"], ["010","011"]] 000 <---> 001 , 010 <---> 011
    #    """
    #    self._checkInputParameters(numQubits,swapList)
    #    self._numQubits = numQubits
    #    self._swapList = swapList
    #    self._swapList = listIntegerToBinary(self._swapList,numQubits)
    #    self._makeMatrix()

    def __new__(cls,numQubits=_numQubits,swapList=_swapList):
        """
        numQubits: Number of qubits.
        swapList: List to describe the states to be swapped.
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
              
    def show(self):
        """
        Print the Unitary.
        """
        print(self.coolingUnitary)

    def getMatrix(self):
        return self.coolingUnitary



lista = [["0000","1000"]]


obj = CoolingUnitary(numQubits=4,swapList=lista)


print(obj)
testMatrix = np.eye((4))


matrix_4x4 = np.array([[1, 0, 0, 0],   
                       [0, 0, 1, 0],   
                       [0, 1, 0, 0],   
                       [0, 0, 0, 1]])

matrix_4x4 = np.array([[0, 0, 1, 0],   
                       [0, 1, 0, 0],   
                       [1, 0, 0, 0],   
                       [0, 0, 0, 1]])

#finalMatrix = obj.getMatrix()

checkUnitary(obj,4)
#checkUnitary(matrix_4x4,2)
#print(testMatrix)


#obj.printSwapList()
#obj.show()
