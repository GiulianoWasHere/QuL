from qiskit import QuantumRegister
from qiskit import ClassicalRegister
from qiskit import QuantumCircuit
from utils.utils import *
from utils.coolingCircuit import CoolingCircuit

class SubOptimalCooling:
    """
    ## SubOptimalCooling(circuit,rounds,barriers)

    Class for the Sub Optimal Cooling circuit. 

    Parameters:
        circuit (QuantumCircuit): Cooling circuit.
        rounds (int): number of rounds of Sub Optimal Cooling
    Return:
        SubOptimalCooling (SubOptimalCooling)
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
        if(self._rounds < 1 ):
            raise ValueError("Rounds have to be >= 1.")   
        self._circuit = self._buildCircuit(CoolingCircuit(self._numQubits,coolingUnitary=self._coolingUnitary,barriers=self._barriers),self._rounds)

    def getCircuit(self):
        """
        ## getCircuit()
        Return:
            Cooling Circuit (QuantumCircuit)
        """
        return self._circuit
    
    def calculateFinalTemp(self,excitedStateProbability):
        numberOfStates = 2 ** self._numQubits
        if(not(isinstance(excitedStateProbability, list))):
            excitedStateProbability = self._numQubits * [excitedStateProbability]
        for j in range(self._rounds):
            initialVector = generateInitialVector(self._numQubits,excitedStateProbability)
            finalVector = initialVector.dot(self._coolingUnitary)
            finalprob = 1
            for i in range(int(numberOfStates/2)):
                finalprob -= finalVector[:, [i]].data[0]
            excitedStateProbability = self._numQubits * [finalprob] 
        return finalprob
    
    def _createList(self,i,j,numQubits):
        """
        Private: Create the list of the qubits.
        """
        l = []
        step = numQubits ** i
        if(i > 0):
            for k in range(numQubits):
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
        finalCircuit = QuantumCircuit(quantumRegisters)

        for i in range(times-1):
            for j in range(qubitsCircuit**(times-i-1)):
                finalCircuit.compose(circuit, qubits=self._createList(i,j,qubitsCircuit), inplace=True)
    
        finalCircuit.compose(circuit, qubits=self._createList(times-1,0,qubitsCircuit), inplace=True)
        
        return finalCircuit
