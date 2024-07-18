from collections import Counter
import numpy as np
import math 
import coolingUnitary as cu
import scipy as sp
from scipy.sparse import csr_array

#Utils

def printOccupationProbabilitiesList(list):
    finalProb = 0
    for i in range(len(list)):
        print(str(i), end=" | ")
        print(list[i])
        if(i == len(list)//2 - 1 ):
            print("-----------------")
        finalProb += list[i][1]
    print(finalProb)

def printOccupationProbabilitiesList2(list,t,j):
    for i in range(len(list)):
        print(str(i), end=" | ")
        print(list[i],end="")
        if(t == i):
            print("*",end="")
        if(i == j):
            print("*",end="")
        print()
        finalProb += list[i][1]
    print(finalProb)

def subSetsOfSwaps(l):
        """
        Creation of subsets of swaps by a list of swaps.
        """
        subsets = [[]]
        dictionary  = {}
        numOfSubsets = 0
        #We put every swap inside of a dictionary until we find a repeated state. 
        #When we find a repeated state we reset the dictionary and create a sublist
        for i in range(len(l)):
            reset = 0
            if l[i][0] not in dictionary:
                dictionary[l[i][0]] = 0
            else:
                reset = 1
            if l[i][1] not in dictionary:
                dictionary[l[i][1]] =  0
            else:
                reset = 1

            if(reset == 1):
                dictionary = {}
                dictionary[l[i][0]] = 0
                dictionary[l[i][1]] = 0
                numOfSubsets += 1
                subsets.append([])
            subsets[numOfSubsets].append(l[i])

        return subsets
###

def invertState(s):
    string = list(s)
    for i in range(len(string)):
        if(string[i] == '0'):
            string[i] = '1'
        else:
            string[i] = '0'
    s = "".join(string)
    return s
def countZeros(string):
    count = 0
    for i in range(len(string)):
        if(string[i]=="0"):
            count+=1
    return count

def integerToBinary(integer,numOfBits):
    if isinstance(integer, int):
        binaryNumber = format(integer, '0'+ str(numOfBits) +'b')
    else:
        binaryNumber = integer
    return binaryNumber

def listIntegerToBinary(lista,numOfBits):
    for i in range(len(lista)):
        lista[i] = integerToBinary(lista[i],numOfBits)
    return lista

def binaryToInteger(binary_string):
    if isinstance(binary_string, int):  
        return binary_string  
    return int(binary_string, 2)    

def is_unitary(m):
    """
    Check if matrix is unitary
    """
    return np.allclose(np.eye(m.shape[0]), m.conj(m).T.dot(m))

def generateInitialVector(numQubits, excitedStateProbability):
    usingList = False
    if(isinstance(excitedStateProbability, list)):
        usingList = True
        if(len(excitedStateProbability) != numQubits):
            raise ValueError("Number of elements inside of the list is different than number of Qubits.")
        
    numStates = 2 ** numQubits
    data = []
    col = numStates * [0]
    row = []
    for i in range(numStates):
        row.append(i)
        numberInBinary = integerToBinary(i,numQubits)
        if(usingList):
            probability = 1
            for j in range(numQubits):
                if(numberInBinary[j] == "1"):
                    probability *= excitedStateProbability[j]
                else:
                    probability *= (1-excitedStateProbability[j])    
            probability = round(probability,numQubits+3)
        else:
            numberOfZeros = countZeros(numberInBinary)
            probability = (excitedStateProbability ** (numQubits - numberOfZeros)) * ((1 - excitedStateProbability)** numberOfZeros)
        data.append(probability)
        
    return csr_array((data, (col, row)), shape=(1, numStates))

def checkInputMatrix(m):
        """
            Check if a Matrix is Unitary.
        Parameters:
            m (numpy.ndarray or sparse._csr.csr_array): Matrix.
        Return:
            Number Of Qubits (int)
        """
        # Check if the matrix is unitary
        if(type(m) is np.ndarray):   
            if(is_unitary(m) == False):
                raise ValueError("Not an unitary Matrix")
            numberOfStates = len(m) 
            return int(math.log2(numberOfStates)),m

        if(type(m) is sp.sparse._csr.csr_array):
            x = m.conjugate().transpose().dot(m)
            y = sp.sparse.eye(x.shape[1]).tocsr()
            if(not(np.all(x.indices == y.indices) and np.all(x.indptr == y.indptr) and np.allclose(x.data, y.data))):
                raise ValueError("Not an unitary Matrix")
            numberOfStates = m.shape[0]
            return int(math.log2(numberOfStates)),m
        
        if(type(m) is cu.CoolingUnitary):
            return m._numQubits,m.coolingUnitary

        raise ValueError("Matrix not a np.ndarray, a csr.array or a Cooling Unitary")
