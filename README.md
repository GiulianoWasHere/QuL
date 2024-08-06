# QuL

QuL is a python package to generate, analyze and test quantum circuits for various computational cooling protocols. 

## Installation

The package can be installed via pip:

```
python3 -m pip install qubitcooling
```
## Cooling Unitary
A Cooling Unitary is a generalized permutation matrix which can perform an arbitrary number of permutations of arbitrary lengths on the quantum states. The class `CoolingUnitary` efficently stores the matrix using a `scipy.sparse.csr_array`, the matrix can be accessed by the method `getCoolingUnitary()`. The class can calculate the work cost of the Unitary with the method `calculateWorkCost()`.

### Generate a Cooling Unitary using a protocol
It is possibile to generate a Cooling Unitary using one of the three protocols provided by QuL which are the `Partner Pairing Algorithm`, `Minimal Work` and the `Mirror Protocol`. The only required argument is the number of qubits, optionally the user can provide the probability of the excited state for each qubit. 

In this example a Cooling unitary is generated using the `Mirror Protocol`:
```python
from qubitcooling import MirrorProtocol

number_of_qubits = 5
unitary = MirrorProtocol(number_of_qubits)

#Print the unitary
print(unitary.coolingUnitary.toarray())
```

A Cooling Unitary generated using the `Minimal Work` using the optional `probability of the excited state`:
```python
from qubitcooling import MinimalWorkProtocol

number_of_qubits = 5
probability_excited_state = 0.2
unitary = MinimalWorkProtocol(number_of_qubits,probability_excited_state)
```
Generate a Cooling Unitary using the `Partner Pairing Algorithm` using a different `probability of the excited state` for each qubit:
```python
from qubitcooling import PartnerPairingAlgorithm

number_of_qubits = 5
probability_excited_state = [0.1,0.2,0.05,0.2,0.1]
unitary = PartnerPairingAlgorithm(number_of_qubits,probability_excited_state)
```

### Generate a Cooling Unitary using a list of permutations
It is possible to generate a Cooling Unitary using a list of permutations using the class `CoolingUnitary`. The required arguments are the number of qubits and the list of permutations. An example where the state `000` is swapped with the state `001`:
```python
from qubitcooling import CoolingUnitary

number_of_qubits = 3
#1 Swaps: 000 <-> 001
permutations = [["000","001"]] 
unitary = CoolingUnitary(number_of_qubits,permutations)
```
It is possible to create cycles with length greater than 2:
```python
from qubitcooling import CoolingUnitary

number_of_qubits = 3
#1 Cycle is 000 -> 001 -> 100 -> 000
#2 Cycle is 010 <-> 011
permutations = [[0,1,"100"],["010","011"]] 
unitary = CoolingUnitary(number_of_qubits,permutations)
```

## Generate a Cooling Circuit

Given a Cooling Unitary, QuL provides four classes to create a Cooling Circuit. In each class the method `getCircuit()` returns a QuantumCircuit by the package `Qiskit`. 

### Dynamic Cooling
Dynamic Cooling is implemented using the class `DynamicCooling`, the only required argument is a Cooling Unitary. An example:
```python
from qubitcooling import DynamicCooling
from qubitcooling import MinimalWorkProtocol

number_of_qubits = 5
unitary = MinimalWorkProtocol(number_of_qubits)
#The True as the second argument is to show the barriers in the QuantumCircuit
circuit = DynamicCooling(unitary,True)

#Print the circuit
print(circuit.getCircuit().draw())
```

### Heat-Bath Algorithmic Cooling
Heat-Bath Algorithmic Cooling is implemented using the class `HeatBathCooling`, the required arguments are a Cooling Unitary and the number of rounds. 

### Sub-Optimal Dynamic Cooling
Sub-Optimal Dynamic Cooling is implemented using the class `SubOptimalCooling`, the required arguments are a Cooling Unitary and the number of rounds. 

### Semi-Open Dynamic Cooling
Semi-Open Dynamic Cooling is implemented using the class `SemiOpenCooling`, the required arguments are a Cooling Unitary and the number of rounds. 

Example:
```python
from qubitcooling import HeatBathCooling
from qubitcooling import MinimalWorkProtocol

number_of_qubits = 5
unitary = MinimalWorkProtocol(number_of_qubits)
rounds = 3
circuit = HeatBathCooling(unitary,rounds,False)
```

## Calculate work cost and final temperature

After generating a quantum circuit with the method `calculateFinalTemperature()` it is possible to calculate the theorical final temperature of the target qubit. The work cost is calculated with the method `calculateWorkCost()`.

Example:
```python
from qubitcooling import DynamicCooling
from qubitcooling import MinimalWorkProtocol

number_of_qubits = 5
unitary = MinimalWorkProtocol(number_of_qubits)
dynamic = DynamicCooling(unitary)

#Probability of target qubit to be in the state |1⟩
probabilityExcitedState = 0.1

dynamic.calculateFinalProbability(probabilityExcitedState)
dynamic.calculateWorkCost(probabilityExcitedState)

#Temperature in milliKelvin (mK)
temperature = 3.4763
#Resonant frequency of qubit (GHz)
w = 1

dynamic.calculateFinalTemperature(temperature,w)
```







