import numpy as np
import scipy as sp

from .coolingUnitary import CoolingUnitary
from .utils.utils import *

#Qiskit
import qiskit as qk
from qiskit import QuantumCircuit

class CoolingCircuit:
    """
    ## CoolingCircuit(numQubits,permutationList,coolingUnitary,barriers)

    Class for a Cooling Circuit. Create a circuit from a Permutation List or a Cooling Unitary.

    Parameters:
        numQubits (int): Number of qubits.
        permutationList (list): List to describe the states to be swapped.
        OR
        coolingUnitary (numpy.ndarray): Cooling Unitary.
        OPTIONAL:
        barriers (bool): Barriers in the circuit.
    Return:
        coolingCircuit (QuantumCircuit)
    """
    _numQubits = None
    _permutationList = None
    _coolingUnitary = None
    _barriers = False
    def __new__(cls,numQubits=_numQubits,permutationList=_permutationList,coolingUnitary=_coolingUnitary,barriers=_barriers):

        cls._numQubits = numQubits
        cls._permutationList = permutationList
        cls._coolingUnitary = coolingUnitary
        cls._barriers = barriers

        if(cls._numQubits == None):
            raise ValueError("Specify number of qubits.")
        if(cls._permutationList is None and cls._coolingUnitary is None):
            raise ValueError("Specify a Permutation List or a Cooling Matrix.")
        if(isinstance(cls._permutationList, list)):
            return cls.permutationListToCircuit(cls._permutationList,numQubits,barriers=cls._barriers)
        
        if(type(cls._permutationList) is np.ndarray):
            return cls.permutationListToCircuit(cls.coolingUnitaryToPermutationList(cls._permutationList),cls._numQubits,cls._barriers)
        if(type(cls._coolingUnitary) is np.ndarray):
            return cls.permutationListToCircuit(cls.coolingUnitaryToPermutationList(cls._coolingUnitary),cls._numQubits,cls._barriers)
        
        if(type(cls._permutationList) is sp.sparse._csr.csr_array):
            return cls.permutationListToCircuit(cls.compressedCoolingUnitaryToPermutationList(cls._permutationList),cls._numQubits,cls._barriers)
        if(type(cls._coolingUnitary) is sp.sparse._csr.csr_array):
            return cls.permutationListToCircuit(cls.compressedCoolingUnitaryToPermutationList(cls._coolingUnitary),cls._numQubits,cls._barriers)
        
        raise ValueError("Input neither a list of permutations or an np.ndarray.")

    def is_numpy_array(matrix):
        return isinstance(matrix[0], np.ndarray)
    
    def permutationListToCircuit(l,numQubit,barriers):
        """
        Returns a circuit from a Permutation List.

        Parameters:
            Permutation List (list)
        Return:
            Cooling Circuit (QuantumCircuit)
        """
        CoolingUnitary._checkInputParameters(CoolingUnitary,numQubit,l)
        qreg_q = qk.QuantumRegister(numQubit, 'q')
        finalCircuit = QuantumCircuit(qreg_q)
        finalCircuitNumberOfGates = 0
        if(barriers == True):
            finalCircuit.barrier()
            finalCircuitNumberOfGates +=1

        #XGates contains the Instruction of the circuit for the Xgate in position i
        tempCirc = QuantumCircuit(numQubit)
        xGates = []
        for i in range(numQubit):
            tempCirc.x(i)
            xGates.append(tempCirc.data.pop())

        #MCXGates contains the Instruction of the circuit for the MCXgate in position i
        rangeMCX = list(range(1,numQubit))
        mcxGates = []
        circtemp = QuantumCircuit(numQubit)
        circtemp.mcx(rangeMCX,0)
        mcxGates.append(circtemp.data.pop())
        for i in range(numQubit-1):
            rangeMCX[i] = i
            circtemp.mcx(rangeMCX,i+1)
            mcxGates.append(circtemp.data.pop())

        
        for i in range(len(l)):
            stateIn = integerToBinary(l[i][len(l[i])-2],numQubit)[::-1]
            stack = []
            for t in range(len(l[i])-2,-1,-1):
                #XOR to find where the state 1 differ from the state 2
                #the resulting list will be used to create the circuit
                XOR = l[i][t] ^ l[i][t-1]
                count = 0
                lenList = 0
                li = []
                while (XOR):
                    if(XOR % 2):
                        li.append(count)
                        lenList +=1
                    XOR = XOR >> 1
                    count += 1 
                numberOfGatesBeforeList = finalCircuitNumberOfGates
                for j in range(lenList):
                    stateNumberOfGates = 0
                    opposite = li[j]          
                    #Add X gates when the qubit is in the state 0 so all control are in the 1 state                   
                    for z in range(len(stateIn)):
                        if(z != opposite):
                            if(stateIn[z] == '0'):
                                finalCircuit._data.append(xGates[z])
                                stateNumberOfGates +=1

                    #Add the MCX gate          
                    finalCircuit._data.append(mcxGates[opposite])
                    
                    #Add X gates when the qubit is in the state 0 so all control are in the 1 state                 
                    for z in range(stateNumberOfGates):
                        finalCircuit._data.append(finalCircuit[finalCircuitNumberOfGates + z])
                        stateNumberOfGates +=1

                    stateNumberOfGates +=1

                    #Change the state in to match the state after applying the gate              
                    if(stateIn[opposite] == '0'):
                        stateIn = stateIn[:opposite] + '1' + stateIn[opposite + 1:]
                    else:
                        stateIn = stateIn[:opposite] + '0' + stateIn[opposite + 1:]

                    if(barriers == True):
                        finalCircuit.barrier()
                        stateNumberOfGates +=1
                    
                    finalCircuitNumberOfGates += stateNumberOfGates

                #finalCircuitNumberOfGates-stateNumberOfGates-2 so we avoid putting the last subCircuit we added since
                #it is not needed for uncomputation
                if(barriers == True):
                    for p in range(finalCircuitNumberOfGates-stateNumberOfGates-2,numberOfGatesBeforeList-2,-1):
                        finalCircuit._data.append(finalCircuit[p])
                        finalCircuitNumberOfGates += 1
                else:
                    for p in range(finalCircuitNumberOfGates-stateNumberOfGates-1,numberOfGatesBeforeList-1,-1):
                        finalCircuit._data.append(finalCircuit[p])
                        finalCircuitNumberOfGates += 1
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
    
    def compressedCoolingUnitaryToPermutationList(ma):
        """
        Returns a Permutation list from a Compressed Cooling Unitary.

        Parameters:
            CoolingUnitary (numpy.ndarray)
        Return:
            Permutation List (list)
        """
        
        statesInSwapCycle = set()
        m = ma.indices
        numberOfStates = len(m)
        permutationsList = []
        for index in range(numberOfStates):

            if(index != m[index]):
                #Check if the state is NOT already inside of a swap cycle
                if(index not in statesInSwapCycle):
                    l = [int(index)]
                    statesInSwapCycle.add(index)
                    nextIndex = m[index]
                    l1 = []
                    #Cycle until we return to the starting state
                    while(index != nextIndex):
                        l1.append(int(nextIndex))
                        statesInSwapCycle.add(nextIndex)
                        nextIndex = m[nextIndex]
                    permutationsList.append(l + l1[::-1])
        return permutationsList



