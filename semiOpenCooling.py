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

class SemiOpenCooling:
    """
    ## SemiOpenCooling(coolingUnitary,rounds,barriers)

    Class for the Semi Open Cooling.

    Parameters:
        coolingUnitary (numpy.ndarray or sparse._csr.csr_array): Cooling Unitary.
        rounds (int): number of rounds.
        OPTIONAL:
        barriers (bool): Barriers in the circuit.
    Return:
        SemiOpenCooling (SemiOpenCooling)
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
        return self._circuit
    
    def _buildCircuit(self,circuit,times):
        """
        Private: Build the circuit.
        """
        qubitsCircuit = circuit.num_qubits
        numberOfQubits = (qubitsCircuit-1) * times + 1
        quantumRegisters = QuantumRegister(numberOfQubits,"q")
        classicalRegisters = ClassicalRegister(1,"c")
        finalCircuit = QuantumCircuit(quantumRegisters,classicalRegisters)
        qubitSmall = qubitsCircuit -1

        for i in range(times):
            #Create a list from [0....numQubits -1] .... [numQubits-1 * times ..... CircuitQubits-2]
            lista = list(range(i*qubitSmall,i*qubitSmall + qubitSmall))
            #Add the qubit we want to cool at the end
            lista.append(numberOfQubits-1)
            finalCircuit.compose(circuit,lista, inplace=True)
            
        return finalCircuit
        

