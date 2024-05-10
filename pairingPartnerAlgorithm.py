from collections import Counter
import numpy as np

from coolingUnitary import CoolingUnitary
from occupationProbabilitiesList import OccupationProbabilitiesList
from utils import *

class PairingPartnerAlgorithm:
    """
    ## PairingPartnerAlgorithm(numQubits,excitedStateProbability)
    Class for the Pairing Partner Algorithm.

    Parameters:
        numQubits (int): Number of qubits.
        excitedStateProbability (float): Probability of the excited state.
    Return:
        Cooling Unitary (numpy.ndarray)
    """
    _numQubits = 2
    _excitedStateProbability = 0.1
    _probabilitiesList = []
    _swapList = []

    def __new__(cls,numQubits=_numQubits,excitedStateProbability=_excitedStateProbability):
        cls._numQubits = numQubits
        cls._excitedStateProbability = excitedStateProbability
        cls._probabilitiesList = OccupationProbabilitiesList(cls._numQubits,cls._excitedStateProbability)

        #After the algorithm a list of swaps is returned
        _swapList2 = cls._minSwapsAlgorithm(cls,cls._probabilitiesList)

        #The list of swaps is split in N subsets
        _ListSubSetOfSwaps  = subSetsOfSwaps(_swapList2)

        #A matrix for every subset is created and multiplied into one
        _matrix = CoolingUnitary(cls._numQubits,_ListSubSetOfSwaps[0])
        for i in range(1,len(_ListSubSetOfSwaps)):
            _matrix = CoolingUnitary(cls._numQubits,_ListSubSetOfSwaps[i]).dot(_matrix)

        #checkUnitary2(_matrix,cls._excitedStateProbability)

        return _matrix
 
    def _minSwapsAlgorithm(self,li):
        """
        Private: Minimum swap algorithm.
        """
        #index of the list to compare, in this case in the list we have ["00",x^2, 0.8..]
        #so the third element is the one we want to compare
        swapListWithStates = []
        index = 1
        l = li.copy()
        #Creation of a copy of the list that is sort
        tempList = l.copy()
        tempList.sort(key=lambda x: x[index],reverse=True)

        
        #We compare the sorted list with the not sorted list to find the optimal swaps
        length = len(l)
        for i in range(length):
            if(l[i][index] != tempList[i][index]):
                element = -1 
                for j in range(length-1,-1,-1):
                    if (l[j][index] == tempList[i][index]):
                        element = j
                        break
                swapListWithStates.append([l[i][0],l[element][0]])

                #Swap an element in the list
                temp = l[i]
                l[i] = l[element]
                l[element] = temp

        return swapListWithStates