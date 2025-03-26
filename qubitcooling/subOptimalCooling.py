from qiskit import QuantumRegister
from qiskit import QuantumCircuit
from .utils.utils import *
from .coolingCircuit import CoolingCircuit
from .coolingUnitary import checkInputMatrix
from .coolingUnitary import workCost
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
    _generatedCircuit = False
    def __init__(self,coolingUnitary=_coolingUnitary,rounds = _rounds,barriers=_barriers):
        self._numQubits,self._coolingUnitary = checkInputMatrix(coolingUnitary)
        self._rounds = rounds
        self._barriers = barriers
        if(self._rounds < 1 ):
            raise ValueError("Rounds have to be >= 1.")   

    def getCircuit(self):
        """
        ## getCircuit()
        Return:
            Cooling Circuit (QuantumCircuit)
        """
        if(self._generatedCircuit == False):
            self._circuit = self._buildCircuit(CoolingCircuit(self._numQubits,coolingUnitary=self._coolingUnitary,barriers=self._barriers),self._rounds)
            self._generatedCircuit = True
        return self._circuit
    
    def calculateFinalProbability(self,excitedStateProbability):
        """
        ## calculateFinalProbability(excitedState)
            Calculate the final probability after the application of the circuit.

        Parameters:
            excitedStateProbability (float): Probability of the excited state.
        Return:
            Final State Probability (float)
        """   
        numberOfStates = 2 ** self._numQubits
        if(not(isinstance(excitedStateProbability, list))):
            excitedStateProbability = self._numQubits * [excitedStateProbability]
        for j in range(self._rounds):
            initialVector = generateInitialVector(self._numQubits,excitedStateProbability)
            finalVector = initialVector.dot(self._coolingUnitary)
            finalprob = 1
            l = finalVector.tocoo().col
            for i in range(len(l)):
                if(l[i] < int(numberOfStates/2)):
                    finalprob -= finalVector[:, [l[i]]].data[0]
            excitedStateProbability = self._numQubits * [finalprob] 
        if finalprob > 0:
            return finalprob
        else:
            return 0
    
    def calculateFinalTemperature(self,temperature,f):
        """
        ## calculateFinalProbability(excitedState)
            Calculate the final temperature after the application of the circuit.

        Parameters:
            temperature (float): temperature of the target qubit in milliKelvin (mK)
            f (float): Standard resonant frequency of qubit (GHz)
        Return:
            Final Temperature (float) : final temperature in milliKelvin (mK)
        """  
        prob = temperatureToProbability(temperature,f)
        return probabilityToTemperature(self.calculateFinalProbability(prob),f)
    
    def calculateWorkCost(self,excitedStateProbability,f=1):
        """
        ## calculateWorkCost(excitedStateProbability,f)
            Calculate the work cost of the Unitary.

        Parameters:
            excitedStateProbability (float): Probability of the excited state for all qubits.
            OR
            excitedStateProbability (list): Probability of the excited state for each qubit.
            (Optional) f (float): Standard resonant frequency of qubit (GHz)
        Return:
            Work Cost (float)
        """      
        workcost = 0
        numberOfStates = 2 ** self._numQubits
        if(not(isinstance(excitedStateProbability, list))):
            excitedStateProbability = self._numQubits * [excitedStateProbability]
        for j in range(self._rounds):
            #for each round calcolate the work cost
            #We multiply the cost of the unitary for each round
            workcost += workCost(self._coolingUnitary,excitedStateProbability,f) * self._numQubits ** (self._rounds - j -1)
            initialVector = generateInitialVector(self._numQubits,excitedStateProbability)
            finalVector = initialVector.dot(self._coolingUnitary)
            finalprob = 1
            l = finalVector.tocoo().col
            for i in range(len(l)):
                if(l[i] < int(numberOfStates/2)):
                    finalprob -= finalVector[:, [l[i]]].data[0]
            excitedStateProbability = self._numQubits * [finalprob] 
        return workcost


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
