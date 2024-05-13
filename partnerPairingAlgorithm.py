from collections import Counter
import numpy as np

from coolingUnitary import CoolingUnitary
from occupationProbabilitiesList import OccupationProbabilitiesList
from utils import *
import bisect 
from coolingCircuit import CoolingCircuit

class PartnerPairingAlgorithmUnitary:
    """
    ## PartnerPairingAlgorithmUnitary(numQubits,excitedStateProbability)
    Class for the Partner Pairing Algorithm.

    Parameters:
        numQubits (int): Number of qubits.
        (Optional) excitedStateProbability (float): Probability of the excited state.
    Return:
        Cooling Unitary (scipy.sparse.csr_array)
    Notes:
        Use the function .toarray() to get a numpy.ndarray.
    """
    _numQubits = 2
    _excitedStateProbability = 0.1
    _probabilitiesList = []
    _swapList = []

    def __new__(cls,numQubits=_numQubits,excitedStateProbability=_excitedStateProbability):
        cls._numQubits = numQubits
        cls._excitedStateProbability = excitedStateProbability
        cls._probabilitiesList = OccupationProbabilitiesList(cls._numQubits,cls._excitedStateProbability)

        #After the algorithm a list of swaps is returned
        _swapList2 = cls._minSwapsAlgorithm(cls,cls._probabilitiesList)

        #The list of swaps is split in N subsets
        _ListSubSetOfSwaps  = subSetsOfSwaps(_swapList2)

        #A matrix for every subset is created and multiplied into one
        _matrix = CoolingUnitary(cls._numQubits,_ListSubSetOfSwaps[0])
        for i in range(1,len(_ListSubSetOfSwaps)):
            _matrix = CoolingUnitary(cls._numQubits,_ListSubSetOfSwaps[i]).dot(_matrix)

        #checkUnitary2(_matrix,cls._excitedStateProbability)

        return _matrix
    
    def _listOfIndexes(self,li,index,numberOfStates):
        """
        Private: Creation of a dictionary with {Probability : [State, index]}
        """
        count = 0
        dictionary = {}
        dictionaryIndex = {}
        for i in range(numberOfStates):
            if li[i][index] not in dictionary:
                dictionary[li[i][index]] = [[li[i][0],i]]
                dictionaryIndex[li[i][index]] = count
                count +=1
            else:
                dictionary[li[i][index]].append([li[i][0],i]) 
        return dictionary,dictionaryIndex
    
    def printVector(vec):
        for i in range(len(vec)):
            print(vec[i])

    def _minSwapsAlgorithm(self,li):
        """
        Private: Minimum swap algorithm.
        """

        swapListWithStates = []
        index = 1
        l = li

        length = len(l)
        #A dictionary to store the position of every state in the list
        dictionary,dictionaryIndex = self._listOfIndexes(self,li,index,length)

        #Transform the dictionary into a vector
        vectDictionary = []
        #A vector the store the states we swapped to increase efficency
        vectAdded = []
        #Vector that stores the number of states with X probability (Es. prob 0.01, 4 states)
        vectNumber = []
        for element, indexes in dictionary.items():
            vectDictionary.append(indexes)
            vectNumber.append([element,len(indexes)])
            vectAdded.append([["",-1]])

        i = 0
        #For every probability: Es(0.4,0.2....)
        for k in range(len(vectNumber)):
            probability = vectNumber[k][0]
            #For the number of states with that probability
            for j in range(vectNumber[k][1]):
                #We check if in the list the element i has the correct probabilty
                if(l[i][index] != vectNumber[k][0]):
                    
                    arrayAdded = vectAdded[dictionaryIndex[probability]]
                    elementToCompare = arrayAdded[len(arrayAdded)-1][1]

                    arrayAdded2 = vectDictionary[dictionaryIndex[probability]]
                    elementToCompare2 = arrayAdded2[len(arrayAdded2)-1][1]

                    #We have two vectors to get the state the swap,
                    #The first one is created at the beginning
                    #The second one every state that is swapped is insert into it
                    #We check if the state at the lowest point in the list is in the
                    #first vector or in the second one
                    if(elementToCompare < elementToCompare2):
                        arrayToPop = vectDictionary[dictionaryIndex[probability]]
                    else:
                        arrayToPop = arrayAdded
                    element = arrayToPop.pop()

                    #insert the element we swapped in the second vector
                    arrayAdded3 = vectAdded[dictionaryIndex[l[i][index]]]
                    bisect.insort(arrayAdded3,[l[i][0],element[1]],key=lambda x: x[1])

                    swapListWithStates.append([l[i][0],element[0]])

                    #Swap in the list
                    temp = l[i]
                    l[i] = l[element[1]]
                    l[element[1]] = temp
                i +=1
                
        return swapListWithStates
    
class PartnerPairingAlgorithmCircuit:
    """
    ## PartnerPairingAlgorithmCircuit(numQubits,excitedStateProbability)

    Create a circuit using the Partner Pairing Algorithm.

    Parameters:
        numQubits (int): Number of qubits.
        (Optional) excitedStateProbability (float): Probability of the excited state.
    Return:
        coolingCircuit (QuantumCircuit)
    """
    _numQubits = 3
    _excitedStateProbability = 0.1
    
    def __new__(cls,numQubits=_numQubits,excitedStateProbability=_excitedStateProbability):

        cls._numQubits = numQubits
        cls._excitedStateProbability = excitedStateProbability
        permutations = CoolingCircuit.compressedCoolingUnitaryToPermutationList(PartnerPairingAlgorithmUnitary(cls._numQubits,cls._excitedStateProbability))
        return CoolingCircuit(cls._numQubits,permutations)