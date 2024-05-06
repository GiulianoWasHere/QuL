from collections import Counter
import numpy as np

from coolingUnitary import CoolingUnitary
from utils import *

#Qiskit
import qiskit as qk
from qiskit import QuantumCircuit



class CoolingCircuit:
    """
    ## CoolingCircuit(numQubits,permutationList,coolingUnitary)

    Class for a Cooling Circuit. Create a circuit from a Permutation List or a Cooling Unitary.

    Parameters:
        numQubits (int): Number of qubits.
        permutationList (list): List to describe the states to be swapped.
        coolingUnitary (numpy.ndarray): Cooling Unitary.
    Return:
        coolingCircuit (QuantumCircuit)
    """
    _numQubits = None
    _permutationList = None
    _coolingUnitary = None
    def __new__(cls,numQubits=_numQubits,permutationList=_permutationList,coolingUnitary=_coolingUnitary):

        cls._numQubits = numQubits
        cls._permutationList = permutationList
        cls._coolingUnitary = coolingUnitary

        if(cls._numQubits == None):
            raise ValueError("Specify number of qubits.")
        if(cls._permutationList == None and type(cls._coolingUnitary) is not np.ndarray):
            raise ValueError("Specify a Permutation List or a Cooling Matrix.")
        if(cls._permutationList != None):
            return cls.permutationListToCircuit(cls._permutationList,numQubits)

        return cls.permutationListToCircuit(cls.coolingUnitaryToPermutationList(cls._coolingUnitary),cls._numQubits)

    def permutationListToCircuit(l,numQubit):
        """
        Returns a circuit from a Permutation List.

        Parameters:
            Permutation List (list)
        Return:
            Cooling Circuit (QuantumCircuit)
        """
        CoolingUnitary._checkInputParameters(CoolingUnitary,numQubit,l)

        qreg_q = qk.QuantumRegister(numQubit, 'q')
        creg_c = qk.ClassicalRegister(numQubit, 'c')
        finalCircuit = QuantumCircuit(qreg_q, creg_c)
        finalCircuit.barrier()
        for i in range(len(l)):
            stateIn = integerToBinary(l[i][len(l[i])-2],numQubit)[::-1]
            stack = []
            for t in range(len(l[i])-2,-1,-1):
                for j in range(numQubit-1,-1,-1):
                    #The reason we use opposite is because how Qiskit handles the states
                    #The qubit we want to cool down is the n-th one
                    opposite = numQubit - j - 1            
                    circuit = QuantumCircuit(qreg_q)
                    if(integerToBinary(l[i][t],numQubit)[j] != integerToBinary(l[i][t-1],numQubit)[j]):
                        
                        #Add X gates when the qubit is in the state 0 so all control are in the 1 state
                        xList = []
                        for z in range(len(stateIn)):
                            if(z != opposite):
                                if(stateIn[z] == '0'):
                                    xList.append(z)
                        if xList:
                            circuit.x(xList)
                        
                        #MCX Gate with target in the (numQubit - j - 1) position and control in the rest of the qubits
                        rangeOfMCX = list(range(0,opposite)) + list(range(opposite + 1,numQubit))
                        circuit.mcx(list(rangeOfMCX),opposite)

                        #Add X gates when the qubit is in the state 0 so all control are in the 1 state
                        if xList:             
                            circuit.x(xList)

                        #Change the state in to match the state after applying the gate              
                        if(stateIn[opposite] == '0'):
                            stateIn = stateIn[:opposite] + '1' + stateIn[opposite + 1:]
                        else:
                            stateIn = stateIn[:opposite] + '0' + stateIn[opposite + 1:]


                        circuit.barrier()

                        stack.append(circuit)
                        finalCircuit = finalCircuit.compose(circuit)

                #Using the stack we create the uncomputation circuit
                #We discard the first element since we don't need it for the uncompuation
                stack.pop()
                while(len(stack)):
                    finalCircuit = finalCircuit.compose(stack.pop())

        return finalCircuit
    
    def coolingUnitaryToPermutationList(m):
        """
        Returns a Permutation list from a Cooling Unitary.

        Parameters:
            CoolingUnitary (numpy.ndarray)
        Return:
            Permutation List (list)
        """
        # Check if the matrix is unitary
        if(is_unitary(m) == False):
            raise ValueError("Not an unitary Matrix")
        
        statesInSwapCycle = set()
        numberOfStates = len(m)
        permutationsList = []

        for i in range(numberOfStates):
            index = i
            #If the state is NOT swapped with itself
            if(m[index][index] != 1):
                #Check if the state is NOT already inside of a swap cycle
                if(index not in statesInSwapCycle):
                    l = [index]
                    statesInSwapCycle.add(index)
                    nextIndex = -1

                    #Find this state is swapped to
                    for j in range(len(m[i])):
                        if(m[j][i] == 1):
                            nextIndex = j
                            break
                    #Cycle until we return to the starting state
                    while(index != nextIndex):
                        l.append(nextIndex)
                        statesInSwapCycle.add(nextIndex)
                        for j in range(len(m[nextIndex])):
                            if(m[j][nextIndex] == 1):
                                nextIndex = j
                                break 
                    permutationsList.append(l)

        return permutationsList



