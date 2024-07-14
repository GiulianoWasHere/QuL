import numpy as np
import scipy as sp

from coolingUnitary import CoolingUnitary
from coolingCircuit import CoolingCircuit
from utils import *

#Qiskit
import qiskit as qk
from qiskit import QuantumRegister
from qiskit import ClassicalRegister
from qiskit import QuantumCircuit

class DynamicCooling():
    """
    ## DynamicCooling(circuit,rounds)

    Class for the Dynamic Cooling. 

    Parameters:
        coolingUnitary (numpy.ndarray or sparse._csr.csr_array): Cooling Unitary.
        rounds (int): number of rounds.
        OPTIONAL:
        barriers (bool): Barriers in the circuit.
    Return:
        DynamicCooling (DynamicCooling)
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
        initialVector = generateInitialVector(self._coolingUnitary,excitedStateProbability)
        if(type(self._coolingUnitary) is np.ndarray):
            finalVector = initialVector.toarray().dot(self._coolingUnitary)
        else:
            finalVector = initialVector.dot(self._coolingUnitary)