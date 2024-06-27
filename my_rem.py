# my_rem.py

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer.noise import NoiseModel, pauli_error
from qiskit_aer.backends import AerSimulator
import scipy.linalg as la
import scipy.optimize
import numpy.typing as npt
from typing import List

def get_readout_noise(p):
    """Create a noise model with a bit-flip error during measurement."""
    error_meas = pauli_error([('X', p), ('I', 1 - p)])
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(error_meas, "measure")
    return noise_model

def initialize(n_qubits):
    """Initialize the states and confusion matrix."""
    total_states = 2**n_qubits
    states = [format(i, f'0{n_qubits}b') for i in range(total_states)]
    confusion_matrix = np.zeros((total_states, total_states))
    return states, confusion_matrix

def generate_mitigator(n_qubits, shots, noise_model):
    """Generate the mitigator matrix based on the noise model."""
    states, confusion_matrix = initialize(n_qubits)

    print("States:")
    print(states)

    for i, state in enumerate(states):
        qc = QuantumCircuit(n_qubits, n_qubits)
        for q in range(n_qubits):
            if state[q] == '1':
                qc.x(n_qubits - q - 1)  # Apply X gate to the appropriate qubit
        qc.measure(qc.qregs[0], qc.cregs[0])

        simulator = AerSimulator(noise_model=noise_model)
        counts = simulator.run(qc, shots=shots).result().get_counts(qc)
        print(f"{state} becomes {counts}")

        # Update the confusion matrix
        for measured_state, count in counts.items():
            j = states.index(measured_state)
            confusion_matrix[i, j] += count

    # Normalize the confusion matrix
    confusion_matrix /= shots    

    np.set_printoptions(formatter={'float': '{:0.6f}'.format})

    print("\nConfusion Matrix:")
    print(confusion_matrix, "\n")

    # Calculate the mitigator
    mitigator = la.inv(confusion_matrix)

    print("Mitigator:")
    print(mitigator)  

    return mitigator


def closest_positive_distribution(
    quasi_probabilities: npt.NDArray[np.float64],
) -> npt.NDArray[np.float64]:
    """Given the input quasi-probability distribution returns the closest
    positive probability distribution (with respect to the total variation
    distance).

    Args:
        quasi_probabilities: The input array of real coefficients.

    Returns:
        The closest probability distribution.
    """
    quasi_probabilities = np.array(quasi_probabilities, dtype=np.float64)
    init_guess = quasi_probabilities.clip(min=0)
    init_guess /= np.sum(init_guess)

    def distance(probabilities: npt.NDArray[np.float64]) -> np.float64:
        return np.linalg.norm(probabilities - quasi_probabilities)

    num_vars = len(init_guess)
    bounds = scipy.optimize.Bounds(np.zeros(num_vars), np.ones(num_vars))
    normalization = scipy.optimize.LinearConstraint(np.ones(num_vars).T, 1, 1)
    result = scipy.optimize.minimize(
        distance,
        init_guess,
        bounds=bounds,
        constraints=normalization,
    )
    if not result.success:
        raise ValueError(
            "REM failed to determine the closest positive distribution."
        )
    return result.x

def sample_probability_vector(
    probability_vector: npt.NDArray[np.float64], samples: int
) -> List[List[int]]:
    """Generate a number of samples from a probability distribution as
    bitstrings.

    Args:
        probability_vector: A probability vector.
        samples: Number of samples to generate.

    Returns:
        A list of sampled bitstrings.
    """
    # sample using the probability distribution given
    num_values = len(probability_vector)
    choices = np.random.choice(num_values, size=samples, p=probability_vector)

    # convert samples to binary strings
    bit_width = int(np.log2(num_values))
    binary_repr_vec = np.vectorize(np.binary_repr)
    binary_strings = binary_repr_vec(choices, width=bit_width)

    # convert binary strings to lists of integers
    bitstrings = [list(map(int, list(bs))) for bs in binary_strings]

    return bitstrings
