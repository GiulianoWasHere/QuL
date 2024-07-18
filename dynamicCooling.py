import numpy as np
import scipy as sp

from coolingUnitary import CoolingUnitary
from utils.coolingCircuit import CoolingCircuit
from utils.utils import *

#Qiskit
import qiskit as qk
from qiskit import QuantumRegister
from qiskit import ClassicalRegister
from qiskit import QuantumCircuit

class DynamicCooling():
    """
    ## DynamicCooling(circuit,rounds,barriers)

    Class for the Dynamic Cooling. 

    Parameters:
        coolingUnitary (numpy.ndarray or sparse._csr.csr_array): Cooling Unitary.
        rounds (int): number of rounds.
        OPTIONAL:
        barriers (bool): Barriers in the circuit.
    Return:
        DynamicCooling (DynamicCooling)
    Notes:
        The circuit cools the last qubit. 
    """
    _numQubits = None
    _coolingUnitary = None
    _barriers = False
    _circuit = None
    def __init__(self,coolingUnitary=_coolingUnitary,barriers=_barriers):
        self._numQubits,self._coolingUnitary = checkInputMatrix(coolingUnitary)
        self._barriers = barriers
        self._circuit = CoolingCircuit(self._numQubits,coolingUnitary=self._coolingUnitary,barriers=self._barriers)

    def getCircuit(self):
        """
        ## getCircuit()
        Return:
            Cooling Circuit (QuantumCircuit)
        """
        return self._circuit
    
    def calculateFinalTemp(self,excitedStateProbability):
        numberOfStates = 2 ** self._numQubits
        initialVector = generateInitialVector(self._numQubits,excitedStateProbability)
        finalVector = initialVector.dot(self._coolingUnitary)
        finalprob = 1
        for i in range(int(numberOfStates/2)):
            finalprob -= finalVector[:, [i]].data[0]
        return finalprob
    
    