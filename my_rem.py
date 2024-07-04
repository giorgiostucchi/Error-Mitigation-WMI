# my_rem.py

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer.noise import NoiseModel, pauli_error
from qiskit_aer.backends import AerSimulator
import scipy.linalg as la
import scipy.optimize
import numpy.typing as npt
from typing import List

# Define a function to create a noise model with a bit-flip error during measurement
def get_readout_noise(p):
    """Create a noise model with a bit-flip error during measurement.
    
    Args:
        p: The probability of a bit-flip error during measurement.
        
    Returns:
        The noise model with the specified error.
    """
    error_meas = pauli_error([('X', p), ('I', 1 - p)])  # Create a bit-flip error
    noise_model = NoiseModel()  # Create an empty noise model
    noise_model.add_all_qubit_quantum_error(error_meas, "measure")  # Add the error to all qubits during measurement
    return noise_model

# Define a function to initialize the states and confusion matrix
def initialize(n_qubits):
    """Initialize the states and confusion matrix.
    
    Args:
        n_qubits: The number of qubits.
        
    Returns:
        The list of states and the confusion matrix.
    """
    total_states = 2**n_qubits  # Calculate the total number of states
    states = [format(i, f'0{n_qubits}b') for i in range(total_states)]  # Generate all possible states
    confusion_matrix = np.zeros((total_states, total_states))  # Initialize the confusion matrix with zeros
    return states, confusion_matrix

def generate_mitigator(n_qubits, shots, noise_model):
    """Generate the mitigator matrix based on the noise model."""
    states, confusion_matrix = initialize(n_qubits)

    # Print the list of states
    print("States:")
    print(states)

    # Iterate over each state and perform measurements
    for i, state in enumerate(states):
        qc = QuantumCircuit(n_qubits, n_qubits)
        for q in range(n_qubits):
            if state[q] == '1':
                qc.x(n_qubits - q - 1)  # Apply X gate to the appropriate qubit
        qc.measure(qc.qregs[0], qc.cregs[0])

        # Simulate the circuit with the noise model
        simulator = AerSimulator(noise_model=noise_model)
        counts = simulator.run(qc, shots=shots).result().get_counts(qc)
        print(f"{state} becomes {counts}")

        # Update the confusion matrix
        for measured_state, count in counts.items():
            j = states.index(measured_state)
            confusion_matrix[i, j] += count

    # Normalize the confusion matrix
    confusion_matrix /= shots    

    condition_number =  np.linalg.cond(confusion_matrix)
    print("\nCondition_number:")
    print(condition_number, "\n")
    if condition_number > 10:
        raise ArithmeticError('Condition number > 10, confusion matrix not invertible')
    

    # Set the print options for the confusion matrix
    np.set_printoptions(formatter={'float': '{:0.6f}'.format})

    # Print the confusion matrix
    print("\nConfusion Matrix:")
    print(confusion_matrix, "\n")

    # Calculate the mitigator
    mitigator = la.inv(confusion_matrix)

    # Print the mitigator
    print("Mitigator:")
    print(mitigator)  

    return mitigator


# Commented code
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
    quasi_probabilities = np.array(quasi_probabilities, dtype=np.float64)  # Convert input to numpy array
    init_guess = quasi_probabilities.clip(min=0)  # Clip negative values to 0
    init_guess /= np.sum(init_guess)  # Normalize the initial guess

    def distance(probabilities: npt.NDArray[np.float64]) -> np.float64:
        """Calculate the distance between two probability distributions."""
        return np.linalg.norm(probabilities - quasi_probabilities)  # Calculate the Euclidean distance

    num_vars = len(init_guess)  # Number of variables
    bounds = scipy.optimize.Bounds(np.zeros(num_vars), np.ones(num_vars))  # Set the bounds for optimization
    normalization = scipy.optimize.LinearConstraint(np.ones(num_vars).T, 1, 1)  # Set the constraint for normalization
    result = scipy.optimize.minimize(
        distance,
        init_guess,
        bounds=bounds,
        constraints=normalization,
    )  # Perform the optimization
    if not result.success:
        raise ValueError(
            "REM failed to determine the closest positive distribution."
        )  # Raise an error if optimization fails
    return result.x  # Return the closest positive distribution

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
