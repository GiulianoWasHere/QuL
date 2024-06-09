from qiskit import QuantumRegister
from qiskit import ClassicalRegister
from qiskit import QuantumCircuit

class HeatBathAlgorithmicCoolingCircuit:
    """
    ## HeatBathAlgorithmicCoolingCircuit(circuit,rounds)

    Class for the [TO DECIDE]. 

    Parameters:
        circuit (QuantumCircuit): Cooling circuit.
        rounds (int): number of rounds of [TO DECIDE]
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