from collections import Counter
import numpy as np

from coolingUnitary import CoolingUnitary
from occupationProbabilitiesList import OccupationProbabilitiesList
from utils import *

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

print(obj)
print(type(obj))
checkUnitary(obj)