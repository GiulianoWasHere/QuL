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
The three protocols provided by QuL are `Partner Pairing Algorithm`, `Minimal Work` and the `Mirror Protocol`. The only required argument is the `number of qubits`, optionally the user can provide the `probability of the excited state` for each qubit. 

In this example a Cooling unitary is generated using the `Mirror Protocol`:



