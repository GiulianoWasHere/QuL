import qiskit as qk
from qiskit import QuantumCircuit
#from qiskit import Aer

from qiskit_aer import AerSimulator

def testCircuit2(circuit):
    n = circuit.num_qubits
    num_circs = 2**n
    circuits = []
    q_regs = qk.QuantumRegister(n, 'q')
    c_regs = qk.ClassicalRegister(n, 'c')
    #make circuits
    for i in range(num_circs):
        total_circ = QuantumCircuit(q_regs, c_regs)
        #prepare initial state
        bitstring = format(i,'b').zfill(n)
        idx = 0
        for bit in bitstring[::-1]:
        #for bit in bitstring:
            if (bit == '1'):
                total_circ.x(idx)
            idx += 1
        total_circ.barrier()
        #add cooling circuits
        #total_circ.compose(circuit, qubits=[q_regs[2],q_regs[1],q_regs[0]], inplace=True)
        total_circ.compose(circuit,inplace=True)
        #total_circ.compose(cooling_circuit, qubits=[q_regs[0],q_regs[1],q_regs[2],q_regs[3],q_regs[4]], inplace=True)
        #add measurement
        total_circ.barrier()
        total_circ.measure(list(range(n)), c_regs)
        #total_circ.measure(0, c_regs)
        #transpiledCircuit = qk.transpile(total_circ, backend=sim_backend,optimization_level=3)
        circuits.append(total_circ)
    

    qasm_sim = AerSimulator()

    counts = []
    numOfDigits = len(str(num_circs))
    print(format(0).zfill(numOfDigits) + " | ",end="")
    for i in range(n-1,0,-1):
        print(i,end="")
    print(0)
    print("---------------------")
    for i in range(num_circs):
        result = qasm_sim.run(circuits[i],shots = 1).result()
        counts.append(result.get_counts())
        #print(i, list(counts[i])[0])
        if(format(i,'b').zfill(n) == list(counts[i])[0]):
            print(format(i).zfill(numOfDigits) + " | " + format(i,'b').zfill(n) + " --> " + str(list(counts[i])[0]))
        else:
            print(format(i).zfill(numOfDigits) + " | " + format(i,'b').zfill(n) + " --> " + str(list(counts[i])[0]) + " (*)")


def testCircuit(circuit):

    n = circuit.num_qubits
    num_circs = 2**n
    q_regs = qk.QuantumRegister(n, 'q')
    c_regs = qk.ClassicalRegister(n, 'c')

    qasm_sim = AerSimulator()
    numOfDigits = len(str(num_circs))
    print(format(0).zfill(numOfDigits) + " | ",end="")
    for i in range(n-1,0,-1):
        print(i,end="")
    print(0)
    print("---------------------")

    #make circuits
    for i in range(num_circs):
        total_circ = QuantumCircuit(q_regs, c_regs)
        #prepare initial state
        bitstring = format(i,'b').zfill(n)
        idx = 0
        for bit in bitstring[::-1]:
        #for bit in bitstring:
            if (bit == '1'):
                total_circ.x(idx)
            idx += 1
        total_circ.barrier()
        #add cooling circuits
        #total_circ.compose(circuit, qubits=[q_regs[2],q_regs[1],q_regs[0]], inplace=True)
        total_circ.compose(circuit,inplace=True)
        #total_circ.compose(cooling_circuit, qubits=[q_regs[0],q_regs[1],q_regs[2],q_regs[3],q_regs[4]], inplace=True)
        #add measurement
        total_circ.barrier()
        total_circ.measure(list(range(n)), c_regs)
        #total_circ.measure(0, c_regs)
        #transpiledCircuit = qk.transpile(total_circ, backend=sim_backend,optimization_level=3)
        result = qasm_sim.run(total_circ,shots = 1).result()
        counts = result.get_counts()
        if(format(i,'b').zfill(n) == list(counts)[0]):
            print(format(i).zfill(numOfDigits) + " | " + format(i,'b').zfill(n) + " --> " + str(list(counts)[0]))
        else:
            print(format(i).zfill(numOfDigits) + " | " + format(i,'b').zfill(n) + " --> " + str(list(counts)[0]) + " (*)")
        if(i == (num_circs //2)-1):
            print("-------------------------")
        