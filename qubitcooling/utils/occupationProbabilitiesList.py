from .utils import *


class OccupationProbabilitiesList:
    """
    ## OccupationProbabilitiesList(numQubits,excitedStateProbability)
    Class for the list of occupation probabilities.

    Parameters:
        numQubits (int): Number of qubits.
        OPTIONAL:
        excitedStateProbability (float): Probability of the excited state.
        OR
        excitedStateProbability (list): List of probability of the excited state for each qubit.
    Return:
        occupationProbabilitiesList (List)
    """
    
    _numQubits = 3
    _excitedStateProbability = 0.1
    _List = []

    def __new__(cls,numQubits=_numQubits,excitedStateProbability=_excitedStateProbability):
        cls._numQubits = numQubits
        if(cls._numQubits < 3):
            raise ValueError("Number of qubits must be greater than 2.")
        cls._excitedStateProbability = excitedStateProbability
        if(isinstance(cls._excitedStateProbability, list)):
            if(len(cls._excitedStateProbability) != numQubits):
                raise ValueError("Number of elements inside of the list is different than number of Qubits.")
            for i in range(len(cls._excitedStateProbability)):
                if(cls._excitedStateProbability[i] <= 0 or cls._excitedStateProbability[i] >= 1):
                    raise ValueError("Probability must be greater than 0 and lower than 1.")  
            return cls._createListWithProbabilityList(cls,cls._numQubits,cls._excitedStateProbability)
        if(cls._excitedStateProbability <= 0 or cls._excitedStateProbability >= 1):
            raise ValueError("Probability must be greater than 0 and lower than 1.")  
        return cls._createList(cls,cls._numQubits,cls._excitedStateProbability)
    
    def _createListWithProbabilityList(self,numQubits,listProbability):
        """
        Private: Creation of the occupation list
        """
        numberOfStates = 2 ** numQubits
        _List = []
        #print(listProbability)
        for i in range(numberOfStates):
            numberInBinary = integerToBinary(i,numQubits)
            probability = 1
            for j in range(numQubits):
                if(numberInBinary[j] == "1"):
                    probability *= listProbability[j]
                else:
                    probability *= (1-listProbability[j])
            #Put the element in the list
            
            _List.append([numberInBinary,round(probability,numQubits+3)])
        return _List

    def _createList(self,numQubits,excitedStateProbability):
        """
        Private: Creation of the occupation list
        """
        numberOfStates = 2 ** numQubits
        _List = []
        for i in range(numberOfStates):
            numberOfZeros = countZeros(integerToBinary(i,numQubits))
            #calculate the probability of x^..(1 - x)^.. for each state
            probability = (excitedStateProbability ** (numQubits - numberOfZeros)) * ((1 - excitedStateProbability)** numberOfZeros)
            #Put the element in the list
            _List.append([integerToBinary(i,numQubits),probability])
        return _List
