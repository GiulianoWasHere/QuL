from collections import Counter
import numpy as np
import time

from scipy.sparse import bsr_array
from scipy.sparse import csr_array
from scipy.sparse import coo_array

from coolingUnitary import CoolingUnitary
from occupationProbabilitiesList import OccupationProbabilitiesList
from mirrorProtocol import MirrorProtocolUnitary
from mirrorProtocol import MirrorProtocolCircuit
from pairingPartnerAlgorithm import PartnerPairingAlgorithmUnitary
from pairingPartnerAlgorithm import PartnerPairingAlgorithmCircuit
from minimalWorkProtocol import MinimalWorkProtocolUnitary
from minimalWorkProtocol import MinimalWorkProtocolCircuit
from coolingCircuit import CoolingCircuit
from utils import *
from quantumUtils import *

from qiskit.circuit.library import UnitaryGate
#TEST
testMatrix = np.eye((4))


matrix_4x4 = np.array([[1, 0, 0, 0],   
                       [0, 0, 1, 0],   
                       [0, 1, 0, 0],   
                       [0, 0, 0, 1]])

matrix_4x4 = np.array([[0, 0, 1, 0],   
                       [0, 1, 0, 0],   
                       [1, 0, 0, 0],   
                       [0, 0, 0, 1]])


#obj = CoolingUnitary(numQubits=3,swapList=lista)


#lista = [[1,0,"010"],["100",7]]
#obj = CoolingUnitary(3,lista)

#print(obj)
#print(type(obj))
#checkUnitary(obj)

#a = PairingPartnerAlgorithm(5,0.1)
#checkUnitary2(a,0.05)
#a = MirrorProtocol(4,0.1)
#checkUnitary2(a,0.05)
#a = MinimalWorkProtocol(4,0.05)
#checkUnitary(a)
#print(a)



""" n = 5
start_time = time.time()

m = MinimalWorkProtocol(n)

print(time.time() - start_time)

l = CoolingCircuit.coolingUnitaryToPermutationList(m)

print(time.time() - start_time)

circu = CoolingCircuit(n,l)

print(time.time() - start_time)

testCircuit(circu) """

""" n= 5
a = MinimalWorkProtocol(5)



print(p) """


#matrix = bsr_array((3, 4), dtype=np.int8)
#print(matrix.toarray())

""" #print(m)
#print(m)
row = [0, 1, 2]
col = [2, 1, 0]
data = [1]*3
#print(data)
matrix = csr_array((data, (row, col)), shape=(3, 3))

matrix2 = csr_array((3, 3), dtype=np.int8)

#matrix = matrix.dot(matrix2)

#print(matrix.toarray()) """
n = 5

start_time = time.time()

m = PartnerPairingAlgorithmUnitary(n)
#m = MinimalWorkProtocolUnitary(n)
#p = CoolingCircuit.coolingUnitaryToPermutationList(m.toarray())
#CoolingCircuit(n,p)
#c = CoolingCircuit(n,m.toarray())
#print()
print(time.time() - start_time)

checkUnitary2(m.toarray(),0.1)

""" c.draw(filename="circuit.txt")

testCircuit(c) """
#checkUnitary2(m.toarray(),0.1)
""" a = CoolingCircuit.compressedCoolingUnitaryToPermutationList(m)

print(time.time() - start_time) """
""" a = CoolingCircuit.compressedCoolingUnitaryToPermutationList(m)
b = CoolingCircuit.coolingUnitaryToPermutationList(m.toarray())

print(a)
print(b)

c = CoolingUnitary(n,a)
checkUnitary2(c.toarray(),0.1)
print(time.time() - start_time) """

#checkUnitary2(m.toarray(),0.1)
#print(m.indices[1])


#print(m.toarray())
#m = MinimalWorkProtocol(n)
#checkUnitary2(m.toarray(),0.1)
""" #print(m)
p = CoolingCircuit.coolingUnitaryToPermutationList(m)
print("SPAZIO")
m = CoolingUnitary(n,p)
b = CoolingUnitary2(n,p)
#np.savetxt('text.txt',m,fmt='%.0f')
bM = b.toarray()
 """
#np.savetxt('text2.txt',b.toarray(),fmt='%.0f')
#print((m==b.toarray()).all())

""" N = 2**n
for i in range(N):
    stringa = ""
    for j in range(N):
        #stringa += str(int(m[i][j])) + " "
        #stringa += str(int(bM[i][j])) + " "
        if(bM[i][j] != m[i][j]):
            print("POSIZIONE: " + str(i) +","+ str(j))
    #print(stringa)
"""
#print((m==bM).all())

#circ = UnitaryGate(b.toarray())

#testCircuit(circ)