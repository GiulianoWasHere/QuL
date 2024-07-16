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

class HeatBathCooling():
    """
    ## HeatBathCooling(circuit,rounds,barriers)

    Class for the Heat Bath Cooling. 

    Parameters:
        coolingUnitary (numpy.ndarray or sparse._csr.csr_array): Cooling Unitary.
        rounds (int): number of rounds.
        OPTIONAL:
        barriers (bool): Barriers in the circuit.
    Return:
        HeatBathCooling (HeatBathCooling)
    Notes:
        The circuit cools the last qubit. 
    """
    _numQubits = None
    _coolingUnitary = None
    _barriers = False
    _rounds = 1
    _circuit = None
    def __init__(self,coolingUnitary=_coolingUnitary,rounds = _rounds,barriers=_barriers):
        self._numQubits,self._coolingUnitary = checkInputMatrix(coolingUnitary)
        self._rounds = rounds
        self._barriers = barriers
        self._circuit = self._buildCircuit(CoolingCircuit(self._numQubits,coolingUnitary=self._coolingUnitary,barriers=self._barriers),self._rounds)

    def getCircuit(self):
        """
        ## getCircuit()
        Return:
            Cooling Circuit (QuantumCircuit)
        """
        return self._circuit
    
    def _buildCircuit(self,circuit,times):
        """
        Private: Build the circuit.
        """
        qubitsCircuit = circuit.num_qubits
        quantumRegisters = QuantumRegister(qubitsCircuit,"q")
        classicalRegisters = ClassicalRegister(1,"c")
        finalCircuit = QuantumCircuit(quantumRegisters,classicalRegisters)
        finalCircuit.compose(circuit, inplace=True)
        finalCircuit.reset(range(qubitsCircuit-1)) 
        for i in range(times-1):

            finalCircuit.compose(circuit, inplace=True)
            finalCircuit.reset(range(qubitsCircuit-1)) 
            
        return finalCircuit