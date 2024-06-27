# ddd.py

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer.noise import NoiseModel, pauli_error
from qiskit_aer.backends import AerSimulator
import scipy.linalg as la
import scipy.optimize
import numpy.typing as npt
from typing import List
import random

def create_random_circuit_with_idle_windows(num_qubits, num_operations, idle_depth):
    circuit = QuantumCircuit(num_qubits, num_qubits)
    
    for _ in range(num_operations):
        # Randomly choose a qubit for the operation
        qubit = random.randint(0, num_qubits - 1)
        
        # Randomly choose an operation to apply
        operation = random.choice(['h', 'x', 'cx', 'id'])
        
        if operation == 'h':
            circuit.h(qubit)
        elif operation == 'x':
            circuit.x(qubit)
        elif operation == 'cx':
            # For CX, choose a control and a target qubit
            target = random.randint(0, num_qubits - 1)
            # Ensure target is not the same as control
            while target == qubit:
                target = random.randint(0, num_qubits - 1)
            circuit.cx(qubit, target)
        elif operation == 'id':
            # Apply idle operation (identity gate) to a random qubit
            circuit.id(qubit)
    
    # Add idle windows at random positions
    for _ in range(idle_depth):
        qubit = random.randint(0, num_qubits - 1)
        circuit.id(qubit)  # Apply idle operation
    
    # Optionally, add measurement to all qubits
    circuit.measure(range(num_qubits), range(num_qubits))
    
    return circuit