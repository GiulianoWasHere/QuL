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
        _swapList = cls._algorithm2(cls,cls._probabilitiesList)
        #printOccupationProbabilitiesList(cls._probabilitiesList)

        #The list of swaps is split in N subsets
        _ListSubSetOfSwaps  = cls._subSetsOfSwaps(cls,_swapList)

        #A matrix for every subset is created and multiplied into one
        _matrix = CoolingUnitary(cls._numQubits,_ListSubSetOfSwaps[0])
        for i in range(1,len(_ListSubSetOfSwaps)):
            _matrix = CoolingUnitary(cls._numQubits,_ListSubSetOfSwaps[i]).dot(_matrix)

        checkUnitary2(_matrix,cls._excitedStateProbability)
        return _matrix
        #return CoolingUnitary(cls._numQubits,_swapList)
    
    def _listOfIndexes(self,li,index,numberOfStates):
        """
        Private: Creation of a dictionary with {Probability : [index]}
        """
        dictionary = {}
        for i in range(numberOfStates):
            if li[i][index] not in dictionary:
                dictionary[li[i][index]] = [i]
            else:
                dictionary[li[i][index]].append(i) 
        return dictionary
    
    def _listOfIndexes2(self,li,index,numberOfStates):
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
    
    def _pop(self,li):
        """
        Private: Pop an element from the list.
        """
        element = li[len(li)-1]
        del li[len(li)-1]
        return element
    
    #very long name
    def _checkIfMaxProbabilityIsOnTopHalfList(self,dictionary,halfOfStates):
        """
        Private: Returns true if the highest probabilites are on the top half of the list.
        """
        count = 1
        for element, indexes in dictionary.items():
            for i in range(len(indexes)):
                if(count > halfOfStates):
                    print(indexes[i][1])
                    return True
                if(indexes[i][1] >= halfOfStates):
                    print(indexes[i][1])
                    return False
                count +=1

    def _subSetsOfSwaps(self,l):
        """
        Private: Creation of subsets of swaps by a list of swaps.
        """
        subsets = [[]]
        dictionary  = {}
        numOfSubsets = 0
        #subsets.append([])
        for i in range(len(l)):
            reset = 0
            if l[i][0] not in dictionary:
            #    dictionary[l[i][0]] = l[i][1] + " (" + str(i) + ")"
                dictionary[l[i][0]] = 0
            else:
                reset = 1
            if l[i][1] not in dictionary:
            #    dictionary[l[i][1]] = l[i][0] + " (" + str(i) + ")"
                dictionary[l[i][1]] =  0
            else:
                reset = 1
            if(reset == 1):
                dictionary = {}
                #dictionary[l[i][0]] = l[i][1] + " (" + str(i) + ")"
                #dictionary[l[i][1]] = l[i][0] + " (" + str(i) + ")"
                dictionary[l[i][0]] = 0
                dictionary[l[i][1]] = 0
                numOfSubsets += 1
                subsets.append([])
            subsets[numOfSubsets].append(l[i])
        #print()
        #print(subsets)
        #for key, value in dictionary.items():
        #    print(key, ":", value)
        return subsets
    
    def _algorithm2(self,li):
        """
        Private: Algorithm for the Minimal Work Protocol.
        """
        numberOfStates = 2 ** self._numQubits
    	#Index of the probabilities 
        index = 2
        halfOfStates = numberOfStates // 2

        swapList = []
        while True:
            #We have to iterate until all the highest probabilities states are in the top half
            dictionary = self._listOfIndexes2(self,li,index,numberOfStates)
            if(self._checkIfMaxProbabilityIsOnTopHalfList(self,dictionary,halfOfStates)):
                break

            #Transform the dictionary to a list
            vectDictionary = []
            for element, indexes in dictionary.items():
                vectDictionary.append(indexes)
            statesToBeSwapped = []

            #Find the states to be swapped, we start from the bottom of the list
            #and we search for the states on top of the list with the lowest probability
            for i in range(len(vectDictionary)-1,0,-1):  
                for j in range(len(vectDictionary[i])-1,-1,-1):
                    if(vectDictionary[i][j][1] < halfOfStates):
                        statesToBeSwapped.append(vectDictionary[i][j])

                #print(statesToBeSwapped)

                #The found states are swapped with the next list of probabilities (ES. states with prob 0.0081 with 0.0729)
                #only if the states to be swapped are in the lower half of the list.
                for j in range(len(vectDictionary[i-1])-1,-1,-1):
                    if(len(statesToBeSwapped) > 0):
                        if(vectDictionary[i-1][j][1] >= halfOfStates):
                            #We swap the element only if it is lower half of the list and the state we are swapping has less probability
                            element = self._pop(self,statesToBeSwapped)
                            swapList.append([element[0],vectDictionary[i-1][j][0]])

                            #Swap state in the list
                            temp = li[element[1]]
                            li[element[1]] = li[vectDictionary[i-1][j][1]]
                            li[vectDictionary[i-1][j][1]] = temp
                    else:
                        break

        #print(swapList)
        #printOccupationProbabilitiesList(li)
        #print(li)
        #print(dictionary)
        #dictionary = self._listOfIndexes2(self,li,index,numberOfStates)
        #print(dictionary)
        #print(self._checkIfMaxProbabilityIsOnTopHalfList(self,dictionary,halfOfStates))
        return swapList
    

a = MinimalWorkProtocol(5,0.1)