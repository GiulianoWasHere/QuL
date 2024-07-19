from .coolingUnitary import CoolingUnitary
from .utils.occupationProbabilitiesList import OccupationProbabilitiesList
from .utils.utils import *

class MirrorProtocol:
    """
    ## MirrorProtocol(numQubits)
    Class for the Mirror Protocol.

    Parameters:
        numQubits (int): Number of qubits.
    Return:
        Cooling Unitary (CoolingUnitary)
    """
    _numQubits = 3
    _probabilitiesList = []
    _swapList = []

    def __new__(cls,numQubits=_numQubits):
        cls._numQubits = numQubits
        cls._probabilitiesList = OccupationProbabilitiesList(cls._numQubits)
        _swapList = cls._algorithm(cls,cls._probabilitiesList)
        return CoolingUnitary(cls._numQubits,_swapList)
    
    def _algorithm(self,li):
        """
        Private: Algorithm for the Mirror Protocol.
        """
        k = self._numQubits/2
        numberOfStates = 2 ** self._numQubits
        swapList = []
    	#Index in the list of the state like 000, 001... 
        index = 0
        for i in range(0,int(numberOfStates/2)):
            if(k > countZeros(li[i][index])):
                swapList.append([li[i][index],invertState(li[i][index])])
        return swapList