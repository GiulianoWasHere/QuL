from collections import Counter
import numpy as np

from coolingUnitary import CoolingUnitary
from occupationProbabilitiesList import OccupationProbabilitiesList
from utils import *

class PairingPartnerAlgorithm:
    """
    ## PairingPartnerAlgorithm(numQubits,excitedStateProbability)
    Class for the Pairing Partner Algorithm.

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
                    if(elementToCompare < elementToCompare2):
                        arrayToPop = vectDictionary[dictionaryIndex[probability]]
                    else:
                        arrayToPop = arrayAdded
                    element = arrayToPop.pop()

                    arrayAdded3 = vectAdded[dictionaryIndex[l[i][index]]]
                    elementToCompare3 = arrayAdded3[len(arrayAdded3)-1][1]

                    arrayAdded3.append([l[i][0],element[1]])

                    if(elementToCompare3 > element[1]):
                        vectAdded[dictionaryIndex[l[i][index]]].sort(key=lambda x: x[1])

                    swapListWithStates.append([l[i][0],element[0]])

                    #Swap in the list
                    temp = l[i]
                    l[i] = l[element[1]]
                    l[element[1]] = temp
                i +=1
        return swapListWithStates

    def _minSwapsAlgorithm4(self,li):
        """
        Private: Minimum swap algorithm.
        """
        #index of the list to compare, in this case in the list we have ["00",x^2, 0.8..]
        #so the third element is the one we want to compare
        swapListWithStates = []
        index = 1
        l = li.copy()
        #Creation of a copy of the list that is sort
        tempList = l.copy()
        tempList.sort(key=lambda x: x[index],reverse=True)

        
        #We compare the sorted list with the not sorted list to find the optimal swaps
        length = len(l)
        dictionary,dictionaryIndex = self._listOfIndexes(self,li,index,length)

        #print(dictionary)
        #print(dictionaryIndex)

        vectDictionary = []
        for element, indexes in dictionary.items():
            vectDictionary.append(indexes)

        vectAdded = []
        for i in range(len(vectDictionary)):
            vectAdded.append([["",-1]])
        
        #print(vectAdded)
        #print(vectDictionary)
        #self.printVector(vectDictionary)
        for i in range(length):
            if(l[i][index] != tempList[i][index]):
                
                arrayAdded = vectAdded[dictionaryIndex[tempList[i][index]]]
                elementToCompare = arrayAdded[len(arrayAdded)-1][1]

                #print(elementToCompare)
                arrayAdded2 = vectDictionary[dictionaryIndex[tempList[i][index]]]
                elementToCompare2 = arrayAdded2[len(arrayAdded2)-1][1]

                #print(elementToCompare,elementToCompare2)
                if(elementToCompare < elementToCompare2):
                    arrayToPop = vectDictionary[dictionaryIndex[tempList[i][index]]]
                else:
                    arrayToPop = arrayAdded
                element = arrayToPop.pop()
                """ print()
                print(l[i][index])
                print(element)
                print() """
                arrayAdded3 = vectAdded[dictionaryIndex[l[i][index]]]
                elementToCompare3 = arrayAdded3[len(arrayAdded3)-1][1]

                arrayAdded3.append([l[i][0],element[1]])

                #vectAdded[dictionaryIndex[l[i][index]]].append([l[i][0],element[1]])

                if(elementToCompare3 > element[1]):
                    vectAdded[dictionaryIndex[l[i][index]]].sort(key=lambda x: x[1])

                
                #print(arrayAdded)
                """ print(element)
                self.printVector(vectAdded)
                print() """

                #print(state,element[0])
                swapListWithStates.append([l[i][0],element[0]])
                #print(swapListWithStates)

                #Swap an element in the list
                #print(l[i],l[oldindex])
                temp = l[i]
                l[i] = l[element[1]]
                l[element[1]] = temp
                #return 1

        #print(swapListWithStates)
        return swapListWithStates

    def _minSwapsAlgorithm3(self,li):
        """
        Private: Minimum swap algorithm.
        """
        #index of the list to compare, in this case in the list we have ["00",x^2, 0.8..]
        #so the third element is the one we want to compare
        swapListWithStates = []
        index = 1
        l = li.copy()
        #Creation of a copy of the list that is sort
        tempList = l.copy()
        tempList.sort(key=lambda x: x[index],reverse=True)

        
        #We compare the sorted list with the not sorted list to find the optimal swaps
        length = len(l)
        dictionary,dictionaryIndex = self._listOfIndexes(self,li,index,length)

        #print(dictionary)
        #print(dictionaryIndex)

        vectDictionary = []
        for element, indexes in dictionary.items():
            vectDictionary.append(indexes)
        
        #self.printVector(vectDictionary)
        for i in range(length):
            if(l[i][index] != tempList[i][index]):
                

                arrayToPop = vectDictionary[dictionaryIndex[tempList[i][index]]]
                element = arrayToPop.pop()
                """ print()
                print(l[i][index])
                print(element)
                print() """
                array = vectDictionary[dictionaryIndex[l[i][index]]]
                oldindex = -1
                state = ""
                for k in range(len(array)):
                    #print(l[i][0] + "  "+ array[k][0])
                    if(l[i][0] == array[k][0]):
                        oldindex = element[1]
                        element[1] = array[k][1]
                        state = array[k][0]
                        del array[k]
                        break
                
                #print(len(arrayToPop)-1)
                if(element[1] > arrayToPop[len(arrayToPop)-1][1]):
                    arrayToPop.append(element)
                else:
                    for z in range(len(arrayToPop)):
                        if(element[1] < arrayToPop[z][1]):
                            arrayToPop.insert(z,element)
                            break

                if(oldindex > array[len(array)-1][1]):
                    array.append([state,oldindex])
                else:
                    for t in range(len(array)):
                        if(oldindex < array[t][1]):
                            array.insert(t,[state,oldindex])
                            break
                
                #self.printVector(vectDictionary)

                #print(state,element[0])
                swapListWithStates.append([state,element[0]])
                #print(swapListWithStates)

                #Swap an element in the list
                #print(l[i],l[oldindex])
                temp = l[i]
                l[i] = l[oldindex]
                l[oldindex] = temp
                #return 1

        #print(swapListWithStates)
        return swapListWithStates
    
    def _minSwapsAlgorithm2(self,li):
        """
        Private: Minimum swap algorithm.
        """
        #index of the list to compare, in this case in the list we have ["00",x^2, 0.8..]
        #so the third element is the one we want to compare
        swapListWithStates = []
        index = 1
        l = li.copy()
        #Creation of a copy of the list that is sort
        tempList = l.copy()
        tempList.sort(key=lambda x: x[index],reverse=True)

        
        #We compare the sorted list with the not sorted list to find the optimal swaps
        length = len(l)
        for i in range(length):
            if(l[i][index] != tempList[i][index]):
                element = -1 
                for j in range(length-1,-1,-1):
                    if (l[j][index] == tempList[i][index]):
                        element = j
                        break
                swapListWithStates.append([l[i][0],l[element][0]])

                #Swap an element in the list
                temp = l[i]
                l[i] = l[element]
                l[element] = temp

        #print(swapListWithStates)
        return swapListWithStates
    
#m = PairingPartnerAlgorithm(8)

#checkUnitary2(m.toarray(),0.1)

#Provare la nom Strat, magiare il primo elemento con un pop e poi inserire l'elemento nella lista piu in basso