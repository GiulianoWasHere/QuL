from .coolingUnitary import CoolingUnitary
from .utils.occupationProbabilitiesList import OccupationProbabilitiesList
from .utils.utils import *
import bisect 

class PartnerPairingAlgorithm:
    """
    ## PartnerPairingAlgorithm(numQubits,excitedStateProbability)
    Class for the Partner Pairing Algorithm.

    Parameters:
        numQubits (int): Number of qubits.
        OPTIONAL:
        excitedStateProbability (float): Probability of the excited state.
        OR
        excitedStateProbability (list): List of probability of the excited state for each qubit.
    Return:
        Cooling Unitary (CoolingUnitary)
    """
    _numQubits = 3
    _excitedStateProbability = 0.1
    _probabilitiesList = []
    _swapList = []

    def __new__(cls,numQubits=_numQubits,excitedStateProbability=_excitedStateProbability):
        cls._numQubits = numQubits
        cls._excitedStateProbability = excitedStateProbability
        cls._probabilitiesList = OccupationProbabilitiesList(cls._numQubits,cls._excitedStateProbability)
        #printOccupationProbabilitiesList(cls._probabilitiesList)
        #After the algorithm a list of swaps is returned
        _swapList2 = cls._minSwapsAlgorithm(cls,cls._probabilitiesList)

        #The list of swaps is split in N subsets
        _ListSubSetOfSwaps  = subSetsOfSwaps(_swapList2)

        #A matrix for every subset is created and multiplied into one
        _matrix = CoolingUnitary(cls._numQubits,_ListSubSetOfSwaps[0])
        for i in range(1,len(_ListSubSetOfSwaps)):
            _matrix = CoolingUnitary(cls._numQubits,_ListSubSetOfSwaps[i]).dot(_matrix)

        return _matrix
    
    def _listOfIndexes(self,li,index,numberOfStates):
        """
        Private: Creation of a dictionary with {Probability : [State, index]}
        """
        dictionary = {}
        for i in range(numberOfStates):
            if li[i][index] not in dictionary:
                dictionary[li[i][index]] = [[li[i][0],i]]
            else:
                dictionary[li[i][index]].append([li[i][0],i]) 
        return dictionary
    
    def _minSwapsAlgorithm(self,li):
        """
        Private: Minimum swap algorithm.
        """

        swapListWithStates = []
        index = 1
        l = li

        length = len(l)
        #A dictionary to store the position of every state in the list
        dictionary = self._listOfIndexes(self,li,index,length)

        #Transform the dictionary into a vector
        vectDictionary = []
        #A vector the store the states we swapped to increase efficency
        vectAdded = []
        #Vector that stores the number of states with X probability (Es. prob 0.01, 4 states)
        vectNumber = []
        dictItems = sorted(dictionary.items(),reverse=True)
        count = 0
        #Dictionary that translate probability to index of the array
        dictionaryIndex = {}
        for element, indexes in dictItems:
            vectDictionary.append(indexes)
            vectNumber.append([element,len(indexes)])
            vectAdded.append([["",-1]])
            dictionaryIndex[element] = count
            count +=1

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