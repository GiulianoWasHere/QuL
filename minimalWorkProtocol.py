from collections import Counter
import numpy as np

from coolingUnitary import CoolingUnitary
from occupationProbabilitiesList import OccupationProbabilitiesList
from utils import *

class MinimalWorkProtocol:
    """
    ## MinimalWorkProtocol(numQubits,excitedStateProbability)
    Class for the Minimal Work Protocol.

    Parameters:
        numQubits (int): Number of qubits.
        excitedStateProbability (float): Probability of the excited state.
    Return:
        Cooling Unitary (numpy.ndarray)
    """
    _numQubits = 2
    _excitedStateProbability = 0.1
    _probabilitiesList = []
    _swapList = []

    def __new__(cls,numQubits=_numQubits,excitedStateProbability=_excitedStateProbability):
        cls._numQubits = numQubits
        cls._excitedStateProbability = excitedStateProbability
        cls._probabilitiesList = OccupationProbabilitiesList(cls._numQubits,cls._excitedStateProbability)
        _swapList = cls._algorithm(cls,cls._probabilitiesList)
        #checkUnitary2(CoolingUnitary(cls._numQubits,_swapList),cls._excitedStateProbability)
        return 1
        #return CoolingUnitary(cls._numQubits,_swapList)
    
    def _elementsToBeSwapped(self,list,count,halfOfStates):
        swapList = []
        for i in range(len(list)):
            if(count[0] > halfOfStates):
                return swapList
            if(list[i] >= halfOfStates):
                swapList.append(list[i])
                stop = True
            count[0] += 1
            
        return swapList
    
    def _algorithm(self,li):
        #printOccupationProbabilitiesList(li)
        numberOfStates = 2 ** self._numQubits
    	#Index of the probabilities 
        index = 2
        halfOfStates = numberOfStates // 2
        dictionaryUpperHalf = {}
        dictionaryLowerHalf = {}
        #Creation of an index list for each probability 
        """ for i in range(numberOfStates):
            if li[i][index] not in dictionary:
                dictionary[li[i][index]] = [i]
            else:
                dictionary[li[i][index]].append(i) 

        count2 = [0]
        print(dictionary)
        vectDictionary = []
        for element, indexes in dictionary.items():
            vectDictionary.append(indexes)
        print(vectDictionary)
        """
        for i in range(numberOfStates):
            if i < halfOfStates:
                if li[i][index] not in dictionaryUpperHalf:
                    dictionaryUpperHalf[li[i][index]] = [i]
                else:
                    dictionaryUpperHalf[li[i][index]].append(i) 
            else:
                if li[i][index] not in dictionaryLowerHalf:
                    dictionaryLowerHalf[li[i][index]] = [i]
                else:
                    dictionaryLowerHalf[li[i][index]].append(i)    

        print(dictionaryUpperHalf)
        print(dictionaryLowerHalf)
        vectUpperHalf = []
        vectLowerHalf = []
        for element, indexes in dictionaryUpperHalf.items():
            vectUpperHalf.append(indexes)
        for element, indexes in dictionaryLowerHalf.items():
            vectLowerHalf.append(indexes)
        print(vectUpperHalf)
        print(vectLowerHalf)

        """ for element, indexes in dictionaryUpperHalf.items():
            if lastElement in dictionaryLowerHalf:
                print(dictionaryLowerHalf[lastElement])

            lastElement = element """
        

        swapList = []
        swapList2 = []
        
        """  count = 0
        for i in range(len(vectDictionary)):
            b = 0
            for j in range(len(vectDictionary[i])):
                if(vectDictionary[i][j] >= halfOfStates):
                    swapList.append([vectDictionary[i][j]])
                    b +=1

        print(swapList) 
        for element, indexes in dictionary.items():
            swapList.append(self._elementsToBeSwapped(self,indexes,count2,halfOfStates))
        count = 0
        for element, indexes in dictionary.items():
            if(count != 0):
                    for i in range(len(swapList[count-1])):
                        swapList2.append([swapList[count-1][i],indexes[i]])
            count +=1
        print(swapList)
        print(swapList2) """
        return 1

    

a = MinimalWorkProtocol(5,0.1)