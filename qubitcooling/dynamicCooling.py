from .coolingCircuit import CoolingCircuit
from .coolingUnitary import checkInputMatrix
from .coolingUnitary import workCost
from .utils.utils import *

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
    _generatedCircuit = False
    def __init__(self,coolingUnitary=_coolingUnitary,barriers=_barriers):
        self._numQubits,self._coolingUnitary = checkInputMatrix(coolingUnitary)
        self._barriers = barriers

    def getCircuit(self):
        """
        ## getCircuit()
        Return:
            Cooling Circuit (QuantumCircuit)
        """
        if(self._generatedCircuit == False):
            self._circuit = CoolingCircuit(self._numQubits,coolingUnitary=self._coolingUnitary,barriers=self._barriers)
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
        initialVector = generateInitialVector(self._numQubits,excitedStateProbability)
        finalVector = initialVector.dot(self._coolingUnitary)
        finalprob = 1
        l = finalVector.tocoo().col
        for i in range(len(l)):
            if(l[i] < int(numberOfStates/2)):
                finalprob -= finalVector[:, [l[i]]].data[0]
        return finalprob
    
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
            Work Cost in micro-electonVolts(float)
        """      
        return workCost(self._coolingUnitary,excitedStateProbability,f)

    
    