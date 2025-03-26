import numpy as np
from scipy.sparse import csr_array
from scipy.constants import Planck
from scipy.constants import Boltzmann
import numpy as np

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
        for i in range(len(excitedStateProbability)):
            if(excitedStateProbability[i] <= 0 or excitedStateProbability[i] >= 1):
                raise ValueError("Probability must be greater than 0 and lower than 1.")
    else:
        if(excitedStateProbability <= 0 or excitedStateProbability >= 1):
            raise ValueError("Probability must be greater than 0 and lower than 1.")        
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

def temperatureToProbability(temperature,f):
    h_ueV_GHz = Planck*6.241506363094e+24*10**9
    hf = h_ueV_GHz*f
    kb = Boltzmann*6.241506363094e+24/1000
    return 1/(np.exp(hf/(kb*temperature))+ 1)

def probabilityToTemperature(probability,f):
    h_ueV_GHz = Planck*6.241506363094e+24*10**9
    hf = h_ueV_GHz*f
    kb = Boltzmann*6.241506363094e+24/1000
    return hf/(kb*np.log(1/probability -1))

def probabilityFromList(numQubits,numberInBinary,excitedStateProbability):
    probability = 1
    for j in range(numQubits):
        if(numberInBinary[j] == "1"):
            probability *= excitedStateProbability[j]
        else:
            probability *= (1-excitedStateProbability[j])    
    return round(probability,numQubits+3)