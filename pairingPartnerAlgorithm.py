from collections import Counter
import numpy as np

from coolingUnitary import CoolingUnitary
from occupationProbabilitiesList import OccupationProbabilitiesList
from utils import *

class PairingPartnerAlgorithm:

    _numQubits = 2
    _excitedStateProbability = 0.1
    _probabilitiesList = []
    _swapList = []

    def __new__(cls,numQubits=_numQubits,excitedStateProbability=_excitedStateProbability):
        cls._numQubits = numQubits
        cls._excitedStateProbability = excitedStateProbability
        cls._probabilitiesList = OccupationProbabilitiesList(cls._numQubits,cls._excitedStateProbability)
        #cls._algorithm(cls,cls._probabilitiesList)
        #_swapList = cls._selectionSortWithMaxIndex(cls,cls._probabilitiesList)
        #_swapList2 = cls._scoreAlgorithm(cls,cls._probabilitiesList)
        _swapList2 = cls._test(cls,cls._probabilitiesList)
        #for i in range(len(_swapList)):
        #    if(_swapList[i][0] == _swapList2[i][0]):
        #        print(str(i) + "| OK")
        #    else:
        #        print(str(i) + "| NOT OK")


        #Return the unitary, unitaries ? 
       
        return 1
    
    #Same cost as the other one
    def _scoreAlgorithm(self,li):
        #index of the list to compare, in this case in the list we have ["00",x^2, 0.8..]
        #so the third element is the one we want to compare
        index = 2

        l = li.copy()
        #printOccupationProbabilitiesList(l)
        swapListWithStates = []
        n = len(l)

        #we start from 1 instead of 0, the first state is always the max value
        for i in range(1,n - 1):
            maxIndex = i
            score = -1
            for j in range(n-1 , i+1, -1):
                #print(j)
                if l[j][index] > l[maxIndex][index]:
                    tempScore = 0
                    if(l[j+1][index] >= l[maxIndex][index]):
                        tempScore +=1
                    if(l[j-1][index] <= l[maxIndex][index]):
                        tempScore +=1
                    if(score < tempScore):
                        maxIndex = j
                        score = tempScore
            if maxIndex != i:
                swapListWithStates.append([l[i][0],l[maxIndex][0]])
                temp = l[i]
                l[i] = l[maxIndex]
                l[maxIndex] = temp
        print(swapListWithStates)
        printOccupationProbabilitiesList(l)
        return l

    #Selection Sort minimize the number of swaps, the standard one uses MinIndex to find the element to swap.
    #Using the Max Index we minimize even more the swaps since the list isn't "completely unordered" and swapping 
    #two close elements usually it isn't the right call. (Write this comment better) 
    def _selectionSortWithMaxIndex(self,li):
        """
        Selection Sort.
        """
        #index of the list to compare, in this case in the list we have ["00",x^2, 0.8..]
        #so the third element is the one we want to compare
        index = 2

        l = li.copy()
        #printOccupationProbabilitiesList(l)
        swapListWithStates = []
        n = len(l)
        for i in range(n - 1):
            maxIndex = i
            for j in range(n-1 , i, -1):
                #print(j)
                if l[j][index] > l[maxIndex][index]:
                    maxIndex = j
            if maxIndex != i:
                swapListWithStates.append([l[i][0],l[maxIndex][0]])
                temp = l[i]
                l[i] = l[maxIndex]
                l[maxIndex] = temp
                #printOccupationProbabilitiesList2(l,i,maxIndex)
        print(swapListWithStates)
        printOccupationProbabilitiesList(l)
        print()
        return l

    #Same cost it is possible to optmize it to run faster
    def _test(self,li):
        #index of the list to compare, in this case in the list we have ["00",x^2, 0.8..]
        #so the third element is the one we want to compare
        swapListWithStates = []
        index = 2
        l = li.copy()
        tempList = l.copy()
        tempList.sort(key=lambda x: x[index],reverse=True)
        #printOccupationProbabilitiesList(l)
        for i in range(len(l)):
            #print(l[i][0],tempList[i][0])
            if(l[i][index] != tempList[i][index]):
                element = -1 
                for j in range(len(l)):
                    if (l[j][index] == tempList[i][index]):
                        element = j
                #print(element)
                swapListWithStates.append([l[i][0],l[element][0]])
                temp = l[i]
                l[i] = l[element]
                l[element] = temp
        print(swapListWithStates)
        printOccupationProbabilitiesList(l)
        return l

a = PairingPartnerAlgorithm(5,0.1)