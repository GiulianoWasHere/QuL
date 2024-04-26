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
    

    def _listOfIndexes(self,li,index,numberOfStates):
        dictionary = {}
        for i in range(numberOfStates):
            if li[i][index] not in dictionary:
                dictionary[li[i][index]] = [i]
            else:
                dictionary[li[i][index]].append(i) 
        return dictionary
    
    def _listOfIndexes2(self,li,index,numberOfStates):
        dictionary = {}
        for i in range(numberOfStates):
            if li[i][index] not in dictionary:
                dictionary[li[i][index]] = [[li[i][0],i]]
            else:
                dictionary[li[i][index]].append([li[i][0],i]) 
        return dictionary
    
    def _pop(self,li):
        element = li[len(li)-1]
        del li[len(li)-1]
        return element
    
    #very long name
    def _checkIfMaxProbabilityIsOnTopHalfList(self,dictionary,halfOfStates):
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
    def _algorithm2(self,li):
        a = 0

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
            vectDictionary = []
            for element, indexes in dictionary.items():
                vectDictionary.append(indexes)
            statesToBeSwapped = []
            for i in range(len(vectDictionary)-1,0,-1):
                #print(i)
                
                for j in range(len(vectDictionary[i])-1,-1,-1):
                    #print(vectDictionary[i][j][1])
                    if(vectDictionary[i][j][1] < halfOfStates):
                        statesToBeSwapped.append(vectDictionary[i][j])

                print(statesToBeSwapped)

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
                #statesToBeSwapped = []
            

            
       
        print(swapList)
        printOccupationProbabilitiesList(li)
        #print(li)
        #print(dictionary)
        dictionary = self._listOfIndexes2(self,li,index,numberOfStates)
        #print(dictionary)
        #print(self._checkIfMaxProbabilityIsOnTopHalfList(self,dictionary,halfOfStates))
        return swapList

    def _algorithm(self,li):
        #printOccupationProbabilitiesList(li)
        numberOfStates = 2 ** self._numQubits
    	#Index of the probabilities 
        index = 2
        halfOfStates = numberOfStates // 2
        dictionaryUpperHalf = {}
        dictionaryLowerHalf = {}
        
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

        #Creation of an index list for each probability 
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


        #Dictionaries to two vectors
        print(dictionaryUpperHalf)
        print(dictionaryLowerHalf)
        vectUpperHalf = []
        vectLowerHalf = []
        vectLowerHalf.append([])
        for element, indexes in dictionaryUpperHalf.items():
            vectUpperHalf.append(indexes)
        for element, indexes in dictionaryLowerHalf.items():
            vectLowerHalf.append(indexes)
        vectUpperHalf.append([])
        
        print(vectUpperHalf)
        print(vectLowerHalf)


        lista = [0,1,2,3,4]
        lista = lista[2:]
        print(lista)
        numOfElements = len(vectUpperHalf[0])
        for i in range(1,len(vectUpperHalf)-2):
            
            if(len(vectUpperHalf[i]) > 0):
                swaps = []
                a = 0
                for j in range(len(vectLowerHalf[i-1])):
                    vectUpperHalf[i-1].append(vectLowerHalf[i-1][j])
                    #vectLowerHalf[i].append(vectUpperHalf[i][j])
                    
                    if(len(vectUpperHalf[i]) > j):
                        vectLowerHalf[i].append(vectUpperHalf[i-1][j])
                        swaps.append([vectLowerHalf[i-1][j],vectUpperHalf[i][j]])
                    else:
                        #print(i)
                        #print(vectUpperHalf)
                        #print(vectLowerHalf)
                        vectLowerHalf[i].append(vectUpperHalf[i+1][j-len(vectUpperHalf[i])])
                        swaps.append([vectLowerHalf[i-1][j],vectUpperHalf[i+1][j-len(vectUpperHalf[i])]])
                    
                    a = j
                    #del vectLowerHalf[i-1][j]
                    #print(j,len(vectLowerHalf[i-1])
                print(a+1)
                a = a + 1
                vectUpperHalf[i+1] =  vectUpperHalf[i+1][a:]
                vectLowerHalf[i] =  vectLowerHalf[i][a:]
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

    

a = MinimalWorkProtocol(7,0.1)