from collections import Counter
import numpy as np


from utils import *


class OccupationProbabilitiesList:
    """
    ## OccupationProbabilitiesList(numQubits,excitedStateProbability)
    Class for the list of occupation probabilities

    Parameters:
        numQubits (int): Number of qubits.
        excitedStateProbability (float): Probability of the excited state
    Return:
        occupationProbabilitiesList (List)
    """
    
    _numQubits = 2
    _excitedStateProbability = 0.1
    _List = []


    """ def __init__(self, numQubits=_numQubits,excitedStateProbability=_excitedStateProbability):
        self._numQubits = numQubits
        self._excitedStateProbability = excitedStateProbability
        self._List = self._createList(self,self._numQubits,self._excitedStateProbability) """

    def __new__(cls,numQubits=_numQubits,excitedStateProbability=_excitedStateProbability):
        cls._numQubits = numQubits
        cls._excitedStateProbability = excitedStateProbability
        return cls._createList(cls,cls._numQubits,cls._excitedStateProbability)
    
    

    def _createList(self,numQubits,excitedStateProbability):
        numberOfStates = 2 ** numQubits
        _List = []
        for i in range(numberOfStates):
            numberOfZeros = countZeros(integerToBinary(i,numQubits))

            #Create the string x(1-x)
            string = ""
            if(numQubits - numberOfZeros != 0):
                string += "x" 
                if(numQubits - numberOfZeros != 1):
                    string += "^" + str(numQubits - numberOfZeros)
            if(numberOfZeros != 0):
                string += "(1 - x)"
                if(numberOfZeros != 1):
                    string += "^" + str(numberOfZeros)
            #calculate the probability of x^..(1 - x)^.. for each state
            probability = (excitedStateProbability ** (numQubits - numberOfZeros)) * ((1 - excitedStateProbability)** numberOfZeros)
            #Put the element in the list
            _List.append([integerToBinary(i,numQubits),string,probability])
        return _List

print(type(OccupationProbabilitiesList(3,0.1)))