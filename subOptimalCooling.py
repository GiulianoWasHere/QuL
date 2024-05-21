from qiskit import QuantumRegister
from qiskit import ClassicalRegister
from qiskit import QuantumCircuit

class SubOptimalCoolingCircuit:
    """
    ## SubOptimalCoolingCircuit(circuit,rounds)

    Class for the Sub Optimal Cooling circuit. 

    Parameters:
        circuit (QuantumCircuit): Cooling circuit.
        rounds (int): number of rounds of Sub Optimal Cooling
    Return:
        coolingCircuit (QuantumCircuit)
    Notes:
        The circuit cools the last qubit. 
    """
    _circuit = None
    _rounds = 1
    def __new__(cls,circuit=_circuit,rounds = _rounds):

        cls._circuit = circuit
        cls._rounds = rounds

        if(isinstance(cls._circuit,QuantumCircuit)):
            return cls._buildCircuit(cls,cls._circuit,cls._rounds)
        else:
            raise ValueError("Input is not a circuit.")
    
    def _createList(i,j,numQubits):
        """
        Private: Create the list of the qubits.
        """
        l = []
        step = numQubits ** i
        if(i > 0):
            for k in range(numQubits):
                #l.append(k* step + j * numQubits * step + i*(numQubits)-1)
                l.append(k* step + j * numQubits * step + numQubits ** i - 1)
        else:
            for k in range(numQubits):
                l.append(k* step + j * numQubits * step)
        return l
    
    def _buildCircuit(self,circuit,times):
        """
        Private: Build the circuit.
        """
        #Number of qubits in the input circuit
        qubitsCircuit = circuit.num_qubits
        #Number of qubits in the final circuit
        numberOfQubits = qubitsCircuit ** times
        quantumRegisters = QuantumRegister(numberOfQubits,"q")
        #classicalRegisters = ClassicalRegister(1,"c")
        finalCircuit = QuantumCircuit(quantumRegisters)

        for i in range(times-1):
            for j in range(qubitsCircuit**(times-i-1)):
                finalCircuit.compose(circuit, qubits=self._createList(i,j,qubitsCircuit), inplace=True)
    
        finalCircuit.compose(circuit, qubits=self._createList(times-1,0,qubitsCircuit), inplace=True)
        
        return finalCircuit
