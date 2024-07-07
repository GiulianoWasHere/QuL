from collections import Counter
import numpy as np
import math 
import scipy as sp

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


def solve(A, B,n):
    XOR = A ^ B
    count = 0
    # Check for 1's in the binary form using
    # Brian Kernighan's Algorithm
    print(integerToBinary(A,n))
    print(integerToBinary(B,n))
    print(integerToBinary(XOR,n))
    print(XOR >> 1)
    li = []
    while (XOR):
        if(XOR % 2):
            li.append(count)
        XOR = XOR >> 1
        count += 1
    print(li)
    return count
