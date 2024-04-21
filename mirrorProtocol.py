from collections import Counter
import numpy as np

from coolingUnitary import CoolingUnitary
from occupationProbabilitiesList import OccupationProbabilitiesList
from utils import *

class MirrorProtocol:

    _numQubits = 2
    _excitedStateProbability = 0.1
    _probabilitiesList = []
    _swapList = []

    def __new__(cls,numQubits=_numQubits,excitedStateProbability=_excitedStateProbability):
        cls._numQubits = numQubits
        cls._excitedStateProbability = excitedStateProbability
        cls._probabilitiesList = OccupationProbabilitiesList(cls._numQubits,cls._excitedStateProbability)
        _swapList = cls._algortithm(cls,cls._probabilitiesList)
        return CoolingUnitary(cls._numQubits,_swapList)
    
    def _algortithm(self,li):
        printOccupationProbabilitiesList(li)
        k = self._numQubits/2
        numberOfStates = 2 ** self._numQubits
        swapList = []
    	#Index of the state
        index = 0
        for i in range(0,int(numberOfStates/2)):
            if(k > countZeros(li[i][0])):
                swapList.append([li[i][0],invertState(li[i][0])])
                print(li[i][0])
        return swapList