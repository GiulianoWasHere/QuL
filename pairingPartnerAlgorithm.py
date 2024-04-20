from collections import Counter
import numpy as np

from coolingUnitary import CoolingUnitary
from occupationProbabilitiesList import OccupationProbabilitiesList
from utils import *

class PairingPartnerAlgorithm:

    _numQubits = 2
    _excitedStateProbability = 0.1
    _probabilitiesList = []
    _swapList = []

    def __new__(cls,numQubits=_numQubits,excitedStateProbability=_excitedStateProbability):
        cls._numQubits = numQubits
        cls._excitedStateProbability = excitedStateProbability
        cls._probabilitiesList = OccupationProbabilitiesList(cls._numQubits,cls._excitedStateProbability)
        #cls._algorithm(cls,cls._probabilitiesList)
        _swapList = cls._selectionSortWithMaxIndex(cls,cls._probabilitiesList)
        #Return the unitary 
        return 1
    

    #Selection Sort minimize the number of swaps, the standard one uses MinIndex to find the element to swap.
    #Using the Max Index we minimize even more the swaps since the bottom of the list is "kinda" ordered
    def _selectionSortWithMaxIndex(self,l):
        """
        Selection Sort.
        """
        #index of the list to compare, in this case in the list we have ["00",x^2, 0.8..]
        #so the third element is the one we want to compare
        index = 2
        printOccupationProbabilitiesList(l)
        swapListWithStates = []
        n = len(l)
        for i in range(n - 1):
            maxIndex = i
            for j in range(n-1 , i, -1):
                #print(j)
                if l[j][index] > l[maxIndex][index]:
                    maxIndex = j
            if maxIndex != i:
                swapListWithStates.append(l[i][0] + "->" + l[maxIndex][0])
                temp = l[i][index]
                l[i][index] = l[maxIndex][index]
                l[maxIndex][index] = temp
        print(swapListWithStates)
        printOccupationProbabilitiesList(l)
        return swapListWithStates

a = PairingPartnerAlgorithm(5,0.1)

