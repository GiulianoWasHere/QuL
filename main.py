from collections import Counter
import numpy as np
import time


from coolingUnitary import CoolingUnitary
from occupationProbabilitiesList import OccupationProbabilitiesList
from mirrorProtocol import MirrorProtocol
from pairingPartnerAlgorithm import PairingPartnerAlgorithm
from minimalWorkProtocol import MinimalWorkProtocol
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


lista = [[1,0,"010"],["100",7]]
obj = CoolingUnitary(3,lista)

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

n = 5
start_time = time.time()

m = MinimalWorkProtocol(n)

print(time.time() - start_time)

l = CoolingCircuit.coolingUnitaryToPermutationList(m)

print(time.time() - start_time)

circu = CoolingCircuit(n,l)

print(time.time() - start_time)

testCircuit(circu)