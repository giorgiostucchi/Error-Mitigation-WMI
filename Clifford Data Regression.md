Clifford data regression (CDR) is a learning-based quantum error mitigation technique in which an error mitigation model is trained with quantum circuits that _resemble_ the circuit of interest, but which are easier to classically simulate.

This error mitigation strategy is designed for application at the gate level and is relatively straightforward to apply on gate-based quantum computers. CDR primarily consists of creating a training data set $\{(X_{\phi_i}^{\text{error}}, X_{\phi_i}^{\text{exact}})\}$, where $X_{\phi_i}^{\text{error}}$ and   $X_{\phi_i}^{\text{exact}}$ are the expectation values of an observable 𝑋 for a state $|\phi_i\rangle$ under error and error-free conditions, respectively.

This method includes the following steps:

1. **Choose Near-Clifford Circuits for Training.** Near-Clifford circuits are selected due to their capability to be efficiently simulated classically, and are denoted by $S_\psi=\{|\phi_i\rangle\}_i$.
2. **Construct the Training Set.** The training set $\{(X_{\phi_i}^{\text{error}}, X_{\phi_i}^{\text{exact}})\}$ is constructed by calculating the expectation values of 𝑋 for each state  $|\phi_i\rangle$ in $S_\psi$, on both a quantum computer (to obtain$X_{\phi_i}^{\text{error}}$) and a classical computer (to obtain $X_{\phi_i}^{\text{exact}}$).
3. **Learn the Error Mitigation Model.** A model $f(X^{\text{error}}$, a) for $X^{exact}$ is defined and learned. Here, 𝑎 is the set of parameters to be determined. This is achieved by minimizing the distance between the training set, as expressed by the following optimization problem: $a_{opt} = \underset{a}{\text{argmin}} \sum_i \left| X_{\phi_i}^{\text{exact}} - f(X_{\phi_i}^{\text{error}},a) \right|^2$. In this expression, $𝑎_{opt}$ are the parameters that minimize the cost function.
4. **Apply the Error Mitigation Model.** Finally, the learned model $f(X^{\text{error}}, a_{opt})$ is used to correct the expectation values of 𝑋 for new quantum states, expressed as $X_\psi^{\text{exact}} = f(X_\psi^{\text{error}}, a_{opt})$.

The effectiveness of this method has been demonstrated on circuits with up to 64 qubits and for tasks such as estimating ground-state energies. However, its performance is dependent on the task, the system, the quality of the training data, and the choice of model.

![[Pasted image 20240610115227.png]]

Near-Clifford approximations of the actual circuit are simulated, without noise, on a classical simulator (circuits can be efficiently simulated classically) and executed on the noisy quantum computer (or a noisy simulator). These results are used as training data to infer the zero-noise expectation value of the error miitigated original circuit, that is finally run on the quantum computer (or noisy simulator).



## Problem setup

To use CDR, we call need four “ingredients”:

1. A quantum circuit to prepare a state 𝜌.
2. A quantum computer or noisy simulator to return a `mitiq.QuantumResult` from 𝜌.
3. An observable 𝑂 which specifies what we wish to compute via Tr(𝜌𝑂).
4. A near-Clifford (classical) circuit simulator.

The quantum circuit must be compiled into a gateset in which the only non-Clifford gates are single-qubit rotations around the 𝑍 axis: $R_Z(\theta)$.

The CDR method creates a set of “training circuits” which are related to the input circuit and are efficiently simulatable. These circuits are simulated on a classical (noiseless) simulator to collect data for regression.

To use CDR at scale, an efficient near-Clifford circuit simulator must be specified.


## Advantages

The main advantage of CDR is that it can be applied without knowing the specific details of the noise model. Indeed, in CDR, the effects of noise are indirectly _learned_ through the execution of an appropriate set of test circuits. In this way, the final error mitigation inference tends to be tuned to the used backend.

This self-tuning property is even stronger in the case of _variable-noise-CDR_, i.e., when using the `scale_factors` option in [`execute_with_cdr()`](https://mitiq.readthedocs.io/en/latest/apidoc.html#mitiq.cdr.cdr.execute_with_cdr "mitiq.cdr.cdr.execute_with_cdr"). In this case, the final error mitigated expectation value is obtained as a linear combination of noise-scaled expectation values. This is similar to [Zero-Noise Extrapolation](https://mitiq.readthedocs.io/en/latest/guide/zne-5-theory.html) but, in CDR, the coefficients of the linear combination are learned instead of being fixed by the extrapolation model.

## Disadvantages

The main disadvantage of CDR is that the learning process is performed on a suite of test circuits which only _resemble_ the original circuit of interest. Indeed, test circuits are _near-Clifford approximations_ of the original one. Only when the approximation is justified, the application of CDR can produce meaningful results. Increasing the `fraction_non_clifford` option in [`execute_with_cdr()`](https://mitiq.readthedocs.io/en/latest/apidoc.html#mitiq.cdr.cdr.execute_with_cdr "mitiq.cdr.cdr.execute_with_cdr") can alleviate this problem to some extent. Note that, the larger `fraction_non_clifford` is, the larger the classical computation overhead is.

Another relevant aspect to consider is that, to apply CDR in a scalable way, a valid near-Clifford simulator is necessary. Note that the computation cost of a valid near-Clifford simulator should scale with the number of non-Clifford gates, independently from the circuit depth. Only in this case, the learning phase of CDR can be applied efficiently.

**Notes**: 
- 

**Open Questions**:
 - [ ]  Check definition of Clifford Gates

### References
- [What is the theory behind CDR? ](https://mitiq.readthedocs.io/en/latest/guide/cdr-5-theory.html)
-  [Error mitigation with Clifford quantum-circuit data](https://quantum-journal.org/papers/q-2021-11-26-592/pdf/) (yet to read)
-  [Unified approach to data-driven quantum error mitigation](https://journals.aps.org/prresearch/pdf/10.1103/PhysRevResearch.3.033098) (yet to read)