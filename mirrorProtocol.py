from collections import Counter
import numpy as np

from coolingUnitary import CoolingUnitary
from occupationProbabilitiesList import OccupationProbabilitiesList
from utils import *
from coolingCircuit import CoolingCircuit

class MirrorProtocolUnitary:
    """
    ## MirrorProtocol(numQubits,excitedStateProbability)
    Class for the Mirror Protocol.

    Parameters:
        numQubits (int): Number of qubits.
        excitedStateProbability (float): Probability of the excited state.
    Return:
        Cooling Unitary (scipy.sparse.csr_array)
    Notes:
        Use the function .toarray() to get a numpy.ndarray.
    """
    _numQubits = 3
    _excitedStateProbability = 0.1
    _probabilitiesList = []
    _swapList = []

    def __new__(cls,numQubits=_numQubits,excitedStateProbability=_excitedStateProbability):
        cls._numQubits = numQubits
        cls._excitedStateProbability = excitedStateProbability
        cls._probabilitiesList = OccupationProbabilitiesList(cls._numQubits,cls._excitedStateProbability)
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
    
class MirrorProtocolCircuit:
    """
    ## MirrorProtocolCircuit(numQubits,excitedStateProbability)

    Create a circuit using the Mirror Protocol.

    Parameters:
        numQubits (int): Number of qubits.
        (Optional) excitedStateProbability (float): Probability of the excited state.
    Return:
        coolingCircuit (QuantumCircuit)
    Notes:
        The circuit cools the last qubit. 
    """
    _numQubits = 3
    _excitedStateProbability = 0.1
    
    def __new__(cls,numQubits=_numQubits,excitedStateProbability=_excitedStateProbability):

        cls._numQubits = numQubits
        cls._excitedStateProbability = excitedStateProbability
        permutations = CoolingCircuit.compressedCoolingUnitaryToPermutationList(MirrorProtocolUnitary(cls._numQubits,cls._excitedStateProbability))
        return CoolingCircuit(cls._numQubits,permutations)