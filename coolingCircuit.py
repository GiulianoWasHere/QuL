from collections import Counter
import numpy as np
import scipy as sp

from coolingUnitary import CoolingUnitary
from utils import *

#Qiskit
import qiskit as qk
from qiskit import QuantumCircuit
from qiskit.circuit.library import XGate

import bisect
from contextlib import suppress


class CoolingCircuit:
    """
    ## CoolingCircuit(numQubits,permutationList,coolingUnitary,barriers)

    Class for a Cooling Circuit. Create a circuit from a Permutation List or a Cooling Unitary.

    Parameters:
        numQubits (int): Number of qubits.
        permutationList (list): List to describe the states to be swapped.
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

    def permutationListToCircuitNO(l,numQubit):
        """
        Returns a circuit from a Permutation List.

        Parameters:
            Permutation List (list)
        Return:
            Cooling Circuit (QuantumCircuit)
        """
        CoolingUnitary._checkInputParameters(CoolingUnitary,numQubit,l)
        #print(l)
        qreg_q = qk.QuantumRegister(numQubit, 'q')
        #creg_c = qk.ClassicalRegister(numQubit, 'c')
        finalCircuit = QuantumCircuit(qreg_q)
        finalCircuit.barrier()
        for i in range(len(l)):
            stateIn = integerToBinary(l[i][len(l[i])-2],numQubit)[::-1]
            #print(stateIn)
            stack = []
            for t in range(len(l[i])-2,-1,-1):
                for j in range(numQubit-1,-1,-1):
                    #The reason we use opposite is because how Qiskit handles the states
                    #The qubit we want to cool down is the n-th one
                    
                    opposite = numQubit - j - 1            
                    circuit = QuantumCircuit(qreg_q)
                    if(integerToBinary(l[i][t],numQubit)[j] != integerToBinary(l[i][t-1],numQubit)[j]):
                        #print(integerToBinary(l[i][t],numQubit))
                        #print(integerToBinary(l[i][t-1],numQubit))
                        #Add X gates when the qubit is in the state 0 so all control are in the 1 state
                        xList = []
                        rangeList = []
                        for z in range(len(stateIn)):
                            if(z != opposite):
                                if(stateIn[z] == '0'):
                                    xList.append(z)
                                rangeList.append(z)
                        if xList:
                            circuit.x(xList) 

                        #MCX Gate with target in the (numQubit - j - 1) position and control in the rest of the qubits
                        #rangeOfMCX = list(range(0,opposite)) + list(range(opposite + 1,numQubit))
                        circuit.mcx(rangeList,opposite)

                        #Add X gates when the qubit is in the state 0 so all control are in the 1 state
                        if xList:             
                            circuit.x(xList)


                        print("FIRST " + stateIn)
                      
                        #Change the state in to match the state after applying the gate              
                        if(stateIn[opposite] == '0'):
                            stateIn = stateIn[:opposite] + '1' + stateIn[opposite + 1:]
                        else:
                            stateIn = stateIn[:opposite] + '0' + stateIn[opposite + 1:]

                        print("AFTER " + stateIn)
                        circuit.barrier()

                        stack.append(circuit)
                        finalCircuit.compose(circuit,inplace=True)

                #Using the stack we create the uncomputation circuit
                #We discard the first element since we don't need it for the uncompuation
                stack.pop()
                while(len(stack)):
                    finalCircuit.compose(stack.pop(),inplace=True)

        return finalCircuit
    
    #XOR
    def permutationListToCircuitXOR(l,numQubit):
        """
        Returns a circuit from a Permutation List.

        Parameters:
            Permutation List (list)
        Return:
            Cooling Circuit (QuantumCircuit)
        """
        CoolingUnitary._checkInputParameters(CoolingUnitary,numQubit,l)
        #print(l)
        qreg_q = qk.QuantumRegister(numQubit, 'q')
        #creg_c = qk.ClassicalRegister(numQubit, 'c')
        finalCircuit = QuantumCircuit(qreg_q)
        finalCircuit.barrier()
        allOnesBinaryNumber = 2 ** numQubit - 1
        for i in range(len(l)):
            #stateIn = binaryToInteger(integerToBinary(l[i][len(l[i])-2],numQubit)[::-1])
            stateIn = l[i][len(l[i])-2]
            #print("START " + integerToBinary(l[i][len(l[i])-2],numQubit) + " END " + stateIn)
            #print(stateIn)
            stack = []
            for t in range(len(l[i])-2,-1,-1):
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
                for j in range(lenList):
                #for j in range(lenList-1,-1,-1):
                    opposite = li[j]  
                    #print(opposite)          
                    circuit = QuantumCircuit(qreg_q)
                    #Add X gates when the qubit is in the state 0 so all control are in the 1 state
                    xList = []
                    rangeList = []
                    
                    XOR = stateIn ^ allOnesBinaryNumber
                    print("XOR " + integerToBinary(XOR,numQubit))
                    position = 0
                    while (XOR):
                        if(position != opposite):
                            if(XOR % 2):
                                xList.append(position)
                            rangeList.append(position)
                        XOR = XOR >> 1
                        position += 1

                    """ for z in range(len(stateIn)):
                        if(z != opposite):
                            if(stateIn[z] == '0'):
                                xList.append(z)
                            rangeList.append(z) #in case doesnt work remove this and add back #rangeOFMCX """
                    if xList:             
                        circuit.x(xList)
                    #MCX Gate with target in the (numQubit - j - 1) position and control in the rest of the qubits
                    #rangeOfMCX = list(range(0,opposite)) + list(range(opposite + 1,numQubit))
                    #circuit.mcx(rangeOfMCX,opposite)
                    circuit.mcx(rangeList,opposite)

                    #Add X gates when the qubit is in the state 0 so all control are in the 1 state
                    if xList:             
                        circuit.x(xList)

                    #Change the state in to match the state after applying the gate              
                    """ if(stateIn[opposite] == '0'):
                        stateIn = stateIn[:opposite] + '1' + stateIn[opposite + 1:]
                    else:
                        stateIn = stateIn[:opposite] + '0' + stateIn[opposite + 1:] """
                    
                    print("FIRST " + integerToBinary(stateIn,numQubit))
                    stateIn = stateIn ^ (1 << (opposite))
                    print("AFTER " + integerToBinary(stateIn,numQubit))


                    circuit.barrier()

                    stack.append(circuit)
                    finalCircuit.compose(circuit,inplace=True)

                #Using the stack we create the uncomputation circuit
                #We discard the first element since we don't need it for the uncompuation
                stack.pop()
                while(len(stack)):
                    finalCircuit.compose(stack.pop(),inplace=True)

        return finalCircuit
    
    #NEW NEW
    def permutationListToCircuit444(l,numQubit,barriers):
        """
        Returns a circuit from a Permutation List.

        Parameters:
            Permutation List (list)
        Return:
            Cooling Circuit (QuantumCircuit)
        """
        CoolingUnitary._checkInputParameters(CoolingUnitary,numQubit,l)
        #print(l)
        qreg_q = qk.QuantumRegister(numQubit, 'q')
        #creg_c = qk.ClassicalRegister(numQubit, 'c')
        finalCircuit = QuantumCircuit(qreg_q)
        if(barriers == True):
            finalCircuit.barrier()

        rangeMCX = list(range(1,numQubit))
        mcxGates = []
        mcxGates.append(QuantumCircuit(qreg_q))
        mcxGates[0].mcx(rangeMCX,0)
        for i in range(numQubit-1):
            rangeMCX[i] = i
            mcxGates.append(QuantumCircuit(qreg_q))
            mcxGates[i+1].mcx(rangeMCX,i+1)

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

                for j in range(lenList):
                    opposite = li[j]          
                    circuit = QuantumCircuit(qreg_q)
                    #Add X gates when the qubit is in the state 0 so all control are in the 1 state 
                    xList = []
                    for z in range(len(stateIn)):
                        if(z != opposite):
                            if(stateIn[z] == '0'):
                                xList.append(z)
                    if xList:
                        circuit.x(xList) 

                    circuit.compose(mcxGates[opposite],inplace=True)
                    
                    #Add X gates when the qubit is in the state 0 so all control are in the 1 state
                    if xList:
                        circuit.x(xList) 

                    #Change the state in to match the state after applying the gate              
                    if(stateIn[opposite] == '0'):
                        stateIn = stateIn[:opposite] + '1' + stateIn[opposite + 1:]
                    else:
                        stateIn = stateIn[:opposite] + '0' + stateIn[opposite + 1:]

                    if(barriers == True):
                        circuit.barrier()

                    stack.append(circuit)
                    finalCircuit.compose(circuit,inplace=True)

                #Using the stack we create the uncomputation circuit
                #We discard the first element since we don't need it for the uncompuation
                stack.pop()
                while(len(stack)):
                    finalCircuit.compose(stack.pop(),inplace=True)

        return finalCircuit
    
    #NEW NEW TEST 2
    def permutationListToCircuit33(l,numQubit,barriers):
        """
        Returns a circuit from a Permutation List.

        Parameters:
            Permutation List (list)
        Return:
            Cooling Circuit (QuantumCircuit)
        """
        CoolingUnitary._checkInputParameters(CoolingUnitary,numQubit,l)
        #print(l)
        qreg_q = qk.QuantumRegister(numQubit, 'q')
        #creg_c = qk.ClassicalRegister(numQubit, 'c')
        finalCircuit = QuantumCircuit(qreg_q)
        if(barriers == True):
            finalCircuit.barrier()

        rangeMCX = list(range(1,numQubit))
        mcxGates = []
        mcxGates.append(QuantumCircuit(qreg_q))
        mcxGates[0].mcx(rangeMCX,0)
        for i in range(numQubit-1):
            rangeMCX[i] = i
            mcxGates.append(QuantumCircuit(qreg_q))
            mcxGates[i+1].mcx(rangeMCX,i+1)

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

                for j in range(lenList):
                    opposite = li[j]          
                    circuit = QuantumCircuit(qreg_q)
                    #Add X gates when the qubit is in the state 0 so all control are in the 1 state 
                    xList = []
                    for z in range(len(stateIn)):
                        if(z != opposite):
                            if(stateIn[z] == '0'):
                                xList.append(z)
                    if xList:
                        circuit.x(xList) 

                    circuit.compose(mcxGates[opposite],inplace=True)
                    
                    #Add X gates when the qubit is in the state 0 so all control are in the 1 state
                    if xList:
                        circuit.x(xList) 

                    #Change the state in to match the state after applying the gate              
                    if(stateIn[opposite] == '0'):
                        stateIn = stateIn[:opposite] + '1' + stateIn[opposite + 1:]
                    else:
                        stateIn = stateIn[:opposite] + '0' + stateIn[opposite + 1:]

                    if(barriers == True):
                        circuit.barrier()

                    if(j != lenList-1):
                        stack.append(circuit)
                    #stack.append(circuit)
                    finalCircuit.compose(circuit,inplace=True)

            #Using the stack we create the uncomputation circuit
            #We discard the first element since we don't need it for the uncompuation
            #stack.pop()
            while(len(stack)):
                finalCircuit.compose(stack.pop(),inplace=True)
            #finalCircuit.compose(stack,inplace=True)

        return finalCircuit
    
    #NEW NEW
    def permutationListToCircuit(l,numQubit,barriers):
        """
        Returns a circuit from a Permutation List.

        Parameters:
            Permutation List (list)
        Return:
            Cooling Circuit (QuantumCircuit)
        """
        CoolingUnitary._checkInputParameters(CoolingUnitary,numQubit,l)
        #print(l)
        qreg_q = qk.QuantumRegister(numQubit, 'q')
        #creg_c = qk.ClassicalRegister(numQubit, 'c')
        finalCircuit = QuantumCircuit(qreg_q)
        if(barriers == True):
            finalCircuit.barrier()

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

                for j in range(lenList):
                    opposite = li[j]          
                    circuit = QuantumCircuit(qreg_q)
                    #Add X gates when the qubit is in the state 0 so all control are in the 1 state 
                    xList = []
                    for z in range(len(stateIn)):
                        if(z != opposite):
                            if(stateIn[z] == '0'):
                                xList.append(z)
                    if xList:
                        circuit.x(xList)
                                    
                    #circuit.compose(mcxGates[opposite],inplace=True)
                    circuit.data.append(mcxGates[opposite])
                    #Add X gates when the qubit is in the state 0 so all control are in the 1 state
                    if xList:
                        circuit.x(xList) 

                    #Change the state in to match the state after applying the gate              
                    if(stateIn[opposite] == '0'):
                        stateIn = stateIn[:opposite] + '1' + stateIn[opposite + 1:]
                    else:
                        stateIn = stateIn[:opposite] + '0' + stateIn[opposite + 1:]

                    if(barriers == True):
                        circuit.barrier()

                    if(j != lenList-1):
                        stack.append(circuit)
                    #stack.append(circuit)
                    finalCircuit.compose(circuit,inplace=True)

            #Using the stack we create the uncomputation circuit
            #We discard the first element since we don't need it for the uncompuation
            #stack.pop()
            while(len(stack)):
                finalCircuit.compose(stack.pop(),inplace=True)
            #finalCircuit.compose(stack,inplace=True)

        return finalCircuit
    
    #NEW NEW NEW NEW NEW NEW
    def permutationListToCircuit(l,numQubit,barriers):
        """
        Returns a circuit from a Permutation List.

        Parameters:
            Permutation List (list)
        Return:
            Cooling Circuit (QuantumCircuit)
        """
        CoolingUnitary._checkInputParameters(CoolingUnitary,numQubit,l)
        #print(l)
        qreg_q = qk.QuantumRegister(numQubit, 'q')
        #creg_c = qk.ClassicalRegister(numQubit, 'c')
        finalCircuit = QuantumCircuit(qreg_q)
        if(barriers == True):
            finalCircuit.barrier()

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
                circuits = []
                for j in range(lenList):
                    opposite = li[j]          
                    circuits.append(QuantumCircuit(qreg_q))
                    #Add X gates when the qubit is in the state 0 so all control are in the 1 state 
                    xList = []
                    for z in range(len(stateIn)):
                        if(z != opposite):
                            if(stateIn[z] == '0'):
                                xList.append(z)
                    if xList:
                        circuits[j].x(xList)
                                    
                    circuits[j].data.append(mcxGates[opposite])
                    #Add X gates when the qubit is in the state 0 so all control are in the 1 state
                    if xList:
                        circuits[j].x(xList) 

                    #Change the state in to match the state after applying the gate              
                    if(stateIn[opposite] == '0'):
                        stateIn = stateIn[:opposite] + '1' + stateIn[opposite + 1:]
                    else:
                        stateIn = stateIn[:opposite] + '0' + stateIn[opposite + 1:]

                    if(barriers == True):
                        circuits[j].barrier()

                    finalCircuit.compose(circuits[j],inplace=True)

                #using the circuits to do the uncomputation
                for p in range(lenList-2,-1,-1):
                    finalCircuit.compose(circuits[p],inplace=True)

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



