Digital Dynamical Decoupling (DDD) is an error mitigation technique in which sequences of gates are applied to slack windows, i.e. single-qubit idle windows, in a quantum circuit. Such sequences of gates can reduce the coupling between the qubits and the environment, mitigating the effects of noise.

Dynamical decoupling is a technique that has been originally devised to shield a quantum system from quantum noise coming from an environment, using open-loop control techniques. The crucial idea behind dynamical decoupling is to intervene with control pulses on timescales that are faster than those of the system-environment interaction.

[What is the theory behind DDD?](https://mitiq.readthedocs.io/en/latest/guide/ddd-5-theory.html#digital-dynamical-decoupling)

The application of DD sequences can have two effects depending on the correlation time of the environment:

1. For Markovian noise, DD can make the overall quantum channel more symmetric (analogous to quantum twirling) but cannot actually decouple the system from the environment;
2. For non-Markovian noise, DD can effectively decouple the system from the environment. In theory, ideal sequences of infinitely quick and strong pulses, can result in complete noise suppression.

In practice, due to the finite frequency and finite amplitude of DD sequences, both effects are possible but only as imperfect approximations.

In the context of quantum computing, DD can be considered as an error mitigation method. With respect to other error mitigation techniques, DD has very peculiar features:

- It maps a noisy quantum computation to a _single_ error-mitigated computation (no need to take linear combinations of noisy results as in [ZNE](https://mitiq.readthedocs.io/en/latest/guide/zne-5-theory.html), [PEC](https://mitiq.readthedocs.io/en/latest/guide/pec-5-theory.html), and [CDR](https://mitiq.readthedocs.io/en/latest/guide/cdr-5-theory.html)).
- As a consequence of the previous point, there is not a fundamental error mitigation overhead or increase in statistical uncertainty in the final result.
- If noise is time-correlated, it can suppress real errors at the physical level instead of applying a virtual noise reduction via classical post-processing.


In a quantum computing device based on the circuit model, sequences of DD pulses can be mapped to sequences of discrete quantum gates (typically Pauli gates). We refer to this gate-level formulation as _digital dynamical decoupling_ (DDD) to distinguish it from the standard pulse-level formulation.

A significant advantage of DDD with respect to pulse-level DD is the possibility of defining it in a backend-independent way, via simple transformations of abstract quantum circuits.

### Common examples of DDD sequences

Common dynamical decoupling sequences are arrays of (evenly spaced) Pauli gates. In particular:

- The _XX_ sequence is typically appropriate for mitigating (time-correlated) dephasing noise;
- The _YY_ sequence is typically appropriate for mitigating (time-correlated) amplitude damping noise;
- The _XYXY_ sequence is typically appropriate for mitigating generic single-qubit noise.

In a practical scenario it is hard to characterize the noise model and the noise spectrum of a quantum device and the choice of the optimal sequence is not obvious _a priori_. A possible strategy is to run a few circuits whose noiseless results are theoretically known, such that one can empirically determine what sequence is optimal for a specific backend.

It may happen that, for some sequences, the final error of the quantum computation is actually increased. As with all other error-mitigation techniques, one should always take into account that an improvement of performances is not guaranteed.

DDD involves the generation and the execution of a _single_ modified circuit. For this reason, there is no need to combine the results of multiple circuits and the final inference step which is necessary for other techniques is instead trivial for DDD.

The grid structure of a circuit can be expressed as a _mask matrix_ with 1 entries in cells that are occupied by gates and 0 entries in empty cells. A slack window is an horizontal and contiguous sequence of zeros in the mask matrix, corresponding to a qubit which is idling for a finite amount of time. To analyze the structure of idle windows, it is more convenient to define a _slack matrix_, i.e., a matrix of positive integers that are placed at the beginning of each slack window and whose value represent the time length of that window. The DDD error mitigation technique consists of filling the slack windows of a circuit with DDD gate sequences.

### Advantages:
- Particularly effective against structured baths, colored noise or any type of noise with some level of memory effects.
- Effective for single-shot quantum computing algorithms, i.e., it finds application beyond algorithms that just require expectation values, like variational quantum algorithms.

### Disadvantages:
- Dynamical decoupling is generally applied at the pulse level. Mitiq provides it at the gate-level. For this reason, it may be difficult to know and control what decoupling sequences are actually run on the quantum processor.
- Cannot improve results against completely symmetric noise effects (symmetrical with respect to gates applied in the decoupling sequence). In particular, digital dynamical decoupling is ineffective against depolarizing Markovian noise.

**Notes**: 
-  "Slack window with a length of 4" means that 4 single-qubit gates can fit in that window
- DDD is designed to mitigate noise that has a finite correlation time. For Markovian noise, DDD can still have a non-trivial effect on the final error, but it is not always a positive effect.
- DDD gate sequences are inserted in idle windows

**Open Questions**:
- [ ] 

### Paper References (to read):
- https://arxiv.org/abs/quant-ph/9803057
- https://arxiv.org/abs/2011.01157