
from qiskit_aer.noise import NoiseModel, pauli_error, depolarizing_error, phase_damping_error, phase_amplitude_damping_error, QuantumError
import numpy as np
from my_ddd import *
from my_rem import *

from typing import List, Callable, Dict
import numpy as np
from matplotlib import pyplot as plt

import qiskit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService

from mitiq.interface.mitiq_qiskit import to_qiskit
from mitiq import ddd, QPROGRAM
from mitiq.ddd import insert_ddd_sequences

from qiskit import QuantumCircuit, transpile, assemble
from qiskit.visualization import plot_histogram

def get_combined_noise(error_meas: QuantumError = None, 
                       error_1q: QuantumError = None, 
                       error_2q: QuantumError = None):
    """Create a noise model with specified errors during measurement and operations."""
    
    noise_model = NoiseModel()
    
    # Add measurement error to all qubits if specified
    if error_meas is not None:
        noise_model.add_all_qubit_quantum_error(error_meas, "measure")
    
    # Add single-qubit depolarizing error to all single-qubit gates if specified
    if error_1q is not None:
        single_qubit_gates = [
            'u1', 'u2', 'u3', 'x', 'y', 'z', 'h', 's', 'sdg', 't', 'tdg'
        ]
        for gate in single_qubit_gates:
            noise_model.add_all_qubit_quantum_error(error_1q, gate)
    
    # Add two-qubit depolarizing error to all two-qubit gates if specified
    if error_2q is not None:
        noise_model.add_all_qubit_quantum_error(error_2q, 'cx')
    
    return noise_model



def apply_ddd_and_run(circuit, noise: NoiseModel = None, reps=1000, ddd=False, ddd_rule=None, output=False):
    """
    Apply DDD rules and run the circuit with optional noise model.

    Parameters:
    - circuit: The quantum circuit to modify and run.
    - noise: The noise model to apply to the circuit.
    - reps: Number of repetitions to run the circuit.
    - ddd: Boolean flag to apply DDD rules.
    - ddd_rule: The rule to apply for DDD (only needed if ddd is True).
    - output: Boolean flag to control the print statements.

    Returns:
    - counts: The counts from running the circuit.
    """
    new_circuit = circuit.copy()  # To leave circuit invariant after execution

    if ddd:
        if ddd_rule is None:
            raise ValueError("ddd_rule must be specified if ddd is True")
        
        if output:
            print("Original circuit")
            print(circuit)
            print("Inserting DDD sequences ... \n")
        new_circuit = insert_ddd_sequences(circuit, ddd_rule)
        if output:
            print(new_circuit)

    if output:
        print(f"Running the circuit ... for {reps} repetitions \n")
    simulator = AerSimulator(noise_model=noise)
    result = simulator.run(new_circuit, shots=reps).result()
    counts = result.get_counts(new_circuit)
    
    return counts



def apply_mitigator(counts, n_qubits, reps=1000, mitigator_instance=None, output=False):
    """
    Apply error mitigation to the counts obtained from running a circuit.

    Parameters:
    - counts: The counts from running the circuit.
    - n_qubits: Number of qubits for the mitigator.
    - mitigator_instance: Precomputed mitigator instance (None if no mitigation).
    - output: Boolean flag to control the print statements.

    Returns:
    - probabilities: The mitigated probabilities.
    """
    num_bit_strings = 2 ** n_qubits
    bit_strings = [format(i, '0{}b'.format(n_qubits)) for i in range(num_bit_strings)]
    
    # Initialize probabilities dictionary with all bit strings and initial probability 0.0
    probabilities = {bit_string: 0.0 for bit_string in bit_strings}
    
    # Update probabilities based on counts
    for k, v in counts.items():
        probabilities[k] = v / reps

    if mitigator_instance is not None:
        probability_vector = np.array([probability for state, probability in sorted(probabilities.items(), key=lambda x: int(x[0], 2))])
        mitigated_probabilities = np.dot(mitigator_instance, probability_vector)
        closest_probabilities = closest_positive_distribution(mitigated_probabilities)
        
        if output:
            print("Empirical probabilities:", probability_vector)
            print("Mitigated quasi-probabilities:", mitigated_probabilities)
            print("Closest positive probabilities:", closest_probabilities)
        
        probabilities = {state: prob for state, prob in zip(sorted(probabilities, key=lambda x: int(x, 2)), closest_probabilities)}

    if output:
        print(f"Final Probabilities={probabilities}")
        print("\n \n")
    
    return probabilities

def run_cases(circuit, noise: NoiseModel = None, reps = 1000, n_qubits = None, ddd_rule = None, mitigator_instance = None):
    """
    Runs the circuit for five cases and returns the results.

    Parameters:
    - circuit: The quantum circuit to modify.
    - noise: The noise model to apply to the circuit.
    - reps: Number of repetitions to run the circuit.
    - n_qubits: Number of qubits for the mitigator.
    - ddd_rule: The rule to apply for DDD.
    - mitigator_instance: Precomputed mitigator instance.

    Returns:
    - Results for each case.
    """
    
    # Case 1: No noise, no mitigation
    print("Running with no noise, no mitigation ... \n")
    counts_no_noise_no_mit = apply_ddd_and_run(circuit, noise=None, reps=reps, ddd=False, ddd_rule=None, output=False)
    result_no_noise_no_mit = apply_mitigator(counts_no_noise_no_mit, n_qubits, reps, mitigator_instance=None, output=True)
    
    # Case 2: Noise, no mitigation
    print("Running with noise, no mitigation ... \n")
    counts_noise_no_mit = apply_ddd_and_run(circuit, noise=noise, reps=reps, ddd=False, ddd_rule=None, output=False)
    result_noise_no_mit = apply_mitigator(counts_noise_no_mit, n_qubits, reps, mitigator_instance=None, output=False)
    
    # Case 3: Noise, mitigation True, DDD False
    print("Running with noise, mitigation True, DDD False ... \n")
    counts_noise_rem_no_ddd = apply_ddd_and_run(circuit, noise=noise, reps=reps, ddd=False, ddd_rule=None, output=False)
    result_noise_rem_no_ddd = apply_mitigator(counts_noise_rem_no_ddd, n_qubits, reps, mitigator_instance=mitigator_instance, output=False)
    
    # Case 4: Noise, mitigation False, DDD True
    print("Running with noise, mitigation False, DDD True ... \n")
    counts_noise_no_rem_ddd = apply_ddd_and_run(circuit, noise=noise, reps=reps, ddd=True, ddd_rule=ddd_rule, output=False)
    result_noise_no_rem_ddd = apply_mitigator(counts_noise_no_rem_ddd, n_qubits, reps, mitigator_instance=None, output=False)
    
    # Case 5: Noise, mitigation True, DDD True
    print("Running with noise, mitigation True, DDD True ... \n")
    counts_noise_rem_ddd = apply_ddd_and_run(circuit, noise=noise, reps=reps, ddd=True, ddd_rule=ddd_rule, output=False)
    result_noise_rem_ddd = apply_mitigator(counts_noise_rem_ddd, n_qubits, reps, mitigator_instance=mitigator_instance, output=False)
    
    return result_no_noise_no_mit, result_noise_no_mit, result_noise_rem_no_ddd, result_noise_no_rem_ddd, result_noise_rem_ddd

def distance(prob_dist_1: Dict[str, float], prob_dist_2: Dict[str, float]) -> np.float64:
    """Calculate the distance between two probability distributions given as dictionaries."""
    def extract_probabilities(result: Dict[str, float]) -> np.ndarray:
        """Extract the probabilities from the dictionary and convert to a NumPy array."""
        return np.array([result['00'], result['01'], result['10'], result['11']])
    
    prob_array_1 = extract_probabilities(prob_dist_1)
    prob_array_2 = extract_probabilities(prob_dist_2)
    
    return np.linalg.norm(prob_array_1 - prob_array_2)  # Calculate the Euclidean distance

def run_experiment(n: int, num_qubits: int, num_operations: int, idle_depth: int, noise, reps: int, shots: int, ddd_rule) -> List[np.float64]:
    avg_distances = np.zeros(4)

    for _ in range(n):
        print(f"Running experiment {_}... \n")
        circuit = create_random_circuit_with_idle_windows(num_qubits, num_operations, idle_depth)
        result_no_noise_no_mit, result_noise_no_mit, result_noise_rem_no_ddd, result_noise_no_rem_ddd, result_noise_rem_ddd = run_cases(
            circuit, noise=noise, reps=reps, n_qubits=num_qubits, ddd_rule=ddd_rule
        )

        distance_no_mit = distance(result_no_noise_no_mit, result_noise_no_mit)
        distance_rem_no_ddd = distance(result_no_noise_no_mit, result_noise_rem_no_ddd)
        distance_no_rem_ddd = distance(result_no_noise_no_mit, result_noise_no_rem_ddd)
        distance_rem_ddd = distance(result_no_noise_no_mit, result_noise_rem_ddd)

        avg_distances[0] += distance_no_mit
        avg_distances[1] += distance_rem_no_ddd
        avg_distances[2] += distance_no_rem_ddd
        avg_distances[3] += distance_rem_ddd

    avg_distances /= n

    return avg_distances