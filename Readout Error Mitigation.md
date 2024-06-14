
Readout Error Mitigation refers to mitigation of the noise occurring during final measurement. Namely, the output is obtained in a perfect and noiseless manner, and then noise subsequently causes this perfect output to be randomly perturbed. 
This type of error can also be considered as an intuitive interpretation of classical noise. Namely, the application of such noise is equivalent to the classical post-processing of the statistics that one would have obtained in an ideal scenario.
A simple version of readout error mitigation is *post-selection* of bitstrings (e.g. on the basis of symmetry preservation).
More elaborate: *confusion matrix*. We generate it for a specific device, compute its pseudoinverse **once**, apply it to raw measurement data. 
For example, one may consider the simplest noise model, which randomly flips each bit in an output with probability 𝑝. By defining the effect of the noise on the basis states, we obtain the *calibration* (also called *assignment* or *confusion*) *matrix* M $$ C_\text{noisy} = M ~ C_\text{ideal}$$where each $M_{i,j}$ is probability of obtaining $j$ if the correct outcome would be $i$. To obtain the matrix, one only needs to statistically count the outcomes and renormalize by the total number of samples. Then the matrix can be used for any other state, e.g. Bell States. In particular, we use $$C_\text{ideal} = M^{-1} C_\text{noisy}.$$to find the error mitigated version of the state. Of course the error fluctuations are statistical, so we cannot get the perfect output state as a result, but only a better version thereof.

Moreover, as relates to obtaining the correlation matrix, one needs to take two different cases into account: correlated and anticorrelated errors between the qubits, leading to either local or global mitigators.

A _Local readout mitigator_ works under the assumption that readout errors are mostly _local_, meaning readout errors for different qubits are independent of each other. In this case, the assignment matrix is the tensor product of 𝑛 2×2 matrices, one for each qubit, making it practical to store the assignment matrix in implicit form, by storing the individual 2×2 assignment matrices. A _Correlated readout mitigator_ uses the full $2^𝑛×2^𝑛$ assignment matrix, meaning it can only be used for small values of 𝑛.

Let's see this concretely.
The simplest noise model possible: one assumes that noise affects the measurement of each qubit independently and with the same confusion probabilities.
The 2×2 confusion matrix $A_1$ for the 1st qubit (and every other qubit) is then $$\begin{bmatrix}1-p_0 & p_1\\p_0 & 1-p_1\end{bmatrix}$$and the joint $2^𝑛×2^𝑛$ confusion matrix $A_1$ for all 𝑛 qubits is just 𝑛 copies of $A_1$ tensored together: 𝐴=$A_1$⊗⋯⊗$A_1$=$A_1^{\otimes n}$.

The same idea can be applied to any 𝑛-qubit confusion matrix 𝐴 which is factorized into the tensor product of 𝑘 smaller, local confusion matrices, one for each subset in a partition of the 𝑛 qubits into 𝑘 smaller subsets. The factorization encodes the assumption that there are 𝑘 independent/uncorrelated noise processes affecting the 𝑘 disjoint subsets of qubits (possibly of different sizes), but within each subset noise may be correlated between qubits in that subset.

**Notes:** 
- In practice the noise characteristics of devices tend to drift, which necessitates a recalibration effort that results in an updated confusion matrix.
- After applying the pseudoinverse matrix $A^{\textdagger}$ to our empirical probability distribution to obtain an adjusted _quasi_-probability distribution, $p'=A^{\textdagger}p$, which could possibly be non-positive. As such, we want to find the closest _positive_ probability distribution to our empirical probability distribution. So there could be a further step which consists in finding this positive distribution if $p'$ was negative.

**Advantages:** 
- Deals with errors that many other techniques do not handle 
- Can often be combined with existing workflows to produce better results
- Can also accept as much information as the user has about the measurement statistics
**Disadvantages:**
- Requires the preliminary characterization of the measurement errors associated to a specific backend 
- Confusion matrix and its estimation involves numerous state preparations and measurements in the computational basis. Its complete characterization scales exponentially in the number of qubits (can be simplified under the assumption that measurement errors are local with respect to individual qubits or group of qubits)

**Other Methods:**
Although the tensor product noise model is appealingly simple, it leaves aside cross-talk errors encountered in real-world setups. Cross-talk during readout can arise from the underlying qubit-qubit coupling, and spectral overlap of readout resonators with stray couplings or multiplexing. We can introduce a correlated noise model based on Continuous Time Markov Processes (CTMP). The corresponding noise matrix has the form $A=e^G$, where $G$ is a sum of local operators generating single and two-qubit readout errors such as $01 \rightarrow 10,11 \rightarrow 00$, etc. The model depends on $2 n^2$ error rates.
Define a CTMP noise model as a stochastic matrix A of size $2^n \times 2^n$ such that
$$
A=e^G, \quad G=\sum_{i=1}^{2 n^2} r_i G_i
$$
where $e^G=\sum_{p=0}^{\infty} G^p / p$ ! is the matrix exponential, $r_i \geq$ 0 are error rates, and $G_i$ are single-qubit or two-qubit operators from the following list

|                  Generator $G_i$                   |    Readout error    | Number of generators |
| :------------------------------------------------: | :-----------------: | :------------------: |
|   $\|1\rangle\langle 0\|-\| 0\rangle\langle 0\|$   |  $0 \rightarrow 1$  |         $n$          |
|   $\|0\rangle\langle 1\|-\| 1\rangle\langle 1\|$   |  $1 \rightarrow 0$  |         $n$          |
| $\|10\rangle\langle 01\|-\| 01\rangle\langle 01\|$ | $01 \rightarrow 10$ |       $n(n-1)$       |
| $\|11\rangle\langle 00\|-\| 00\rangle\langle 00\|$ | $00 \rightarrow 11$ |     $n(n-1) / 2$     |
| $\|00\rangle\langle 11\|-\| 11\rangle\langle 11\|$ | $11 \rightarrow 00$ |     $n(n-1) / 2$     |

Each operator $G_i$ generates a readout error on some bit or some pair of bits. The right column shows the number of ways to choose qubit(s) acted upon by a generator. The negative terms in $G_i$ ensure that $A$ is a stochastic matrix. The CTMP model depends on $2 n^2$ parameters $r_i$, as can be seen by counting the number of generators $G_i$ of each type. Furthermore, the tensor product model Eq. (5) is a special case of CTMP with $r_i=0$ for all two-qubit errors. This method yields better results compared to the simple confusion matrix approach.

### References
- [Confusion Matrix Theory](https://arxiv.org/abs/1907.08518)
- [CMTP Approach](https://arxiv.org/abs/2006.14044)
- [Readout Mitigation Qiskit Experiments](https://qiskit-extensions.github.io/qiskit-experiments/manuals/measurement/readout_mitigation.html#)
- [What is the theory behind REM?](https://mitiq.readthedocs.io/en/latest/guide/rem-5-theory.html)
- [measurement-error-mitigation.ipynb](https://github.com/Qiskit/textbook/blob/main/notebooks/quantum-hardware/measurement-error-mitigation.ipynb)


**Open Questions**:
 - [ ]  "This time we find a more interesting matrix, and one that we cannot use in the approach that we described earlier". Why not? Check link for code implementation on Qiskit. is it not using pseudoinverse
 - [ ] What does measurement filter do on qiskit?
 - [ ] Why *pseudo*inverse? references I checked, also papers, didn't explain