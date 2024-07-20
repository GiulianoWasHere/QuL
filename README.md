# QuL

Description TODO

## Installation

The package can be installed via pip:

```
python3 -m pip install qubitcooling
```

## Generate a Cooling Unitary

There are two ways to generate a Cooling Unitary:

1. Using one of the three protocols provided by QuL.
2. A list of permutations provided by the user.

### Using a protocol
The three protocols provided by QuL are `Partner Pairing Algorithm`, `Minimal Work` and the `Mirror Protocol`. The only required argument is the number of qubits, optionally the user can provide the probability of the excited state for each qubit. 

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
from qubitcooling import MinimalWork

number_of_qubits = 5
probability_excited_state = 0.2
unitary = MinimalWork(number_of_qubits,probability_excited_state)

#Print the unitary
print(unitary.coolingUnitary.toarray())
```
Generate a Cooling Unitary using the `Partner Pairing Algorithm` using a different `probability of the excited state` for each qubit:
```python
from qubitcooling import PartnerPairingAlgorithm

number_of_qubits = 5
probability_excited_state = [0.1,0.2,0.05,0.2,0.1]
unitary = PartnerPairingAlgorithm(number_of_qubits,probability_excited_state)

#Print the unitary
print(unitary.coolingUnitary.toarray())
```




