from .coolingUnitary import CoolingUnitary
from .utils.occupationProbabilitiesList import OccupationProbabilitiesList
from .utils.utils import *

class MinimalWorkProtocol:
    """
    ## MinimalWorkProtocol(numQubits,excitedStateProbability)
    Class for the Minimal Work Protocol.

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
        _swapList = cls._algorithm(cls,cls._probabilitiesList)
        #The list of swaps is split in N subsets
        _ListSubSetOfSwaps  = subSetsOfSwaps(_swapList)
    
        #A matrix for every subset is created and multiplied into one
        _matrix = CoolingUnitary(cls._numQubits,_ListSubSetOfSwaps[0])
        for i in range(1,len(_ListSubSetOfSwaps)):
            _matrix = CoolingUnitary(cls._numQubits,_ListSubSetOfSwaps[i]).dot(_matrix)
        return _matrix
    
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
    
    def _checkIfMaxProbabilityIsOnTopHalfListVector(self,vector,halfOfStates):
        """
        Private: Returns true if the highest probabilites are on the top half of the list.
        """
        count  = 1
        found = False
        for i in range(len(vector)):
            for j in range(len(vector[i])):
                if(count > halfOfStates):
                    return True
                #If we find ...
                if(vector[i][j][1] >= halfOfStates):
                    found = True
                else:
                    count +=1

            if(found == True):
                if(count > halfOfStates):
                    return True
                return False

    def _algorithm(self,li):
        """
        Private: Algorithm for the Minimal Work Protocol.
        """
        numberOfStates = 2 ** self._numQubits
        #Index of the probabilities 
        index = 1
        halfOfStates = numberOfStates // 2

        swapList = []
        dictionary = self._listOfIndexes2(self,li,index,numberOfStates)
        #Transform the dictionary to an array, we make sure the vector is sorted by the probability 
        vectDictionary = []
        dictItems = sorted(dictionary.items(),reverse=True)
        for element, indexes in dictItems:
            vectDictionary.append(indexes)
        while True:
            #We have to iterate until all the highest probabilities states are in the top half
            statesToBeSwapped = []
            if(self._checkIfMaxProbabilityIsOnTopHalfListVector(self,vectDictionary,halfOfStates)):
                break

            #Find the states to be swapped, we start from the bottom of the list
            #and we search for the states on top of the list with the lowest probability
            for i in range(len(vectDictionary)-1,0,-1):  
                statesToBeSwapped = []
                for j in range(len(vectDictionary[i])-1,-1,-1):
                    if(vectDictionary[i][j][1] < halfOfStates):
                        #In this list we put ["[State,position in the list]","Position in the vector"]
                        statesToBeSwapped.append([vectDictionary[i][j],j])

                #The found states are swapped with the next list of probabilities (ES. states with prob 0.0081 with 0.0729)
                #only if the states to be swapped are in the lower half of the list.
                for j in range(len(vectDictionary[i-1])-1,-1,-1):
                    if(len(statesToBeSwapped) > 0):
                        if(vectDictionary[i-1][j][1] >= halfOfStates):
                            #We swap the element only if it is lower half of the list and the state we are swapping has less probability
                            element = statesToBeSwapped.pop()
                            swapList.append([element[0][0],vectDictionary[i-1][j][0]])

                            #Swap state in the vector
                            temp = vectDictionary[i-1][j][1]
                            vectDictionary[i-1][j][1] = vectDictionary[i][element[1]][1]
                            vectDictionary[i][element[1]][1] = temp
                    else:
                        break
        return swapList