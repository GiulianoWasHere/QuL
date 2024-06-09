from scipy.constants import Planck
from scipy.sparse import csr_array
import scipy 
from coolingCircuit import CoolingCircuit
from minimalWorkProtocol import MinimalWorkProtocolUnitary
import numpy as np
from utils import *
import math

class WorkCost:
    """
    ## WorkCost(coolingUnitary,w)
        Class to calculate the work cost.

    Parameters:
        coolingUnitary (scipy.sparse.csr_array,numpy.ndarray): Cooling unitary
        excitedStateProbability (float): Probability of the excited state.
        (Optional) w (float): Resonant frequency of qubit
    Return:
        Work Cost (float)
    """
    _w = 1
    _coolingUnitary = None
    _excitedStateProbability = 0.1
    def __new__(cls,coolingUnitary = _coolingUnitary,excitedStateProbability = _excitedStateProbability, w=_w):

        cls._w = w
        cls._coolingUnitary = coolingUnitary
        cls._excitedStateProbability = excitedStateProbability
        if(cls._coolingUnitary is not None):
            if(isinstance(cls._coolingUnitary,scipy.sparse.csr_array)):
                numQubits = int(math.log2(len(cls._coolingUnitary.indices)))
                return cls._calculate(cls,CoolingCircuit.compressedCoolingUnitaryToPermutationList(cls._coolingUnitary),cls._w,numQubits,cls._excitedStateProbability)
            if(type(cls._coolingUnitary) is np.ndarray):
                numQubits = int(math.log2(len(cls._coolingUnitary[0])))
                return cls._calculate(cls,CoolingCircuit.coolingUnitaryToPermutationList(cls._coolingUnitary),cls._w,numQubits,cls._excitedStateProbability)
            raise ValueError("Cooling Unitary is not a csr_array or a np.array")  
        raise ValueError("No CoolingUnitary in input")
    
    def _calculate(self,l,w,numQubits,excitedState):
        workcost = 0
        for i in range(len(l)):
            for j in range(len(l[i])):
                if(j != len(l[i])-1):
                    stateIn = integerToBinary(l[i][j],numQubits)
                    stateOut = integerToBinary(l[i][j+1],numQubits)
                else:
                    stateIn = integerToBinary(l[i][j],numQubits)
                    stateOut = integerToBinary(l[i][0],numQubits)

                stateInProb = countZeros(stateIn) * (1 - excitedState) + (numQubits - countZeros(stateIn) * excitedState)
                stateOutProb = countZeros(stateOut) * (1 - excitedState) + (numQubits - countZeros(stateOut) * excitedState)

                eigenvalue = Planck * w/2 * (numQubits - countZeros(stateIn)) - (countZeros(stateIn))

                workcost += eigenvalue * (stateOutProb - stateInProb)
        return workcost

