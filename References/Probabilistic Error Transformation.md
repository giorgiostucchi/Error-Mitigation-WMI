Probabilistic error cancellation (PEC) is an error mitigation technique in which ideal operations are represented as linear combinations of noisy operations. In PEC, unbiased estimates of expectation values are obtained by Monte Carlo averaging over different noisy circuits. 

PEC is therefore based on two steps:

- The first idea is to express ideal gates as linear combinations of implementable noisy gates. These linear combinations are called quasi-probability representations.
- The second idea is to probabilistically sample from the previous quasi-probability representations to approximate quantum expectation values via a Monte Carlo average.

## Quasi-probability representations

In PEC, each ideal gate $\mathcal G_i$ of a circuit of interest $\mathcal U = {\mathcal G}_t \circ  \dots \circ {\mathcal G}_2 \circ {\mathcal G}_1$ is represented as a linear combination of noisy implementable operations ${\mathcal O_{i, \alpha}}$ (i.e., operations that can be directly applied with a noisy backend):

$$\mathcal G_i = \sum_\alpha \eta_{i, \alpha} \mathcal O_{i, \alpha},
\quad  \eta_{i, \alpha} \in \mathbb R,$$

where the calligraphic symbols $\mathcal G_i$ stand for super-operators acting on the density matrix of the qubits as linear quantum channels.

The real coefficients $\eta_{i, \alpha}$ form a quasi-probability distribution with respect to the index 𝛼. Their sum is normalized but, differently from standard probabilities, they can take negative values:

$$\sum_\alpha \eta_{i,\alpha}=1,  \qquad  \gamma_i = \sum_\alpha |\eta_{i, \alpha}| \ge 1.$$

The constant $\gamma_i$ quantifies the negativity of the quasi-probability distribution which is directly related to the error mitigation cost associated to the gate $\mathcal G_i$.

## Error cancellation

The aim of PEC is estimating the ideal expectation value of some observable 𝐴=𝐴† with respect to the quantum state prepared by an ideal circuit of interest 𝑈 acting on some initial reference state $\rho_0$ (typically $\rho_0= |0\dots 0 \rangle \langle 0 \dots 0 |$).

Replacing each gate $\mathcal{G}_i$ with its noisy representation, we can express the ideal expectation value as a linear combination of noisy expectation values:

$$\langle A \rangle_{\rm ideal}= {\rm tr}[A \mathcal U (\rho_0)] =
\sum_{\vec{\alpha}} \eta_{\vec{\alpha}} \langle A_{\vec{\alpha}}\rangle_{\rm noisy}$$

where we introduced the multi-index $\vec{\alpha}=(\alpha_1, \alpha_2, \dots ,\alpha_t)$ and

$$\eta_{\vec{\alpha}} := \prod_{i=1}^t \eta_{i, \alpha_i},
\quad  \langle A_{\vec{\alpha}}\rangle_{\rm noisy} :=  {\rm tr}[A \Phi_{\vec{\alpha}}(\rho_0)],
\quad \Phi_{\vec{\alpha}} := \mathcal O_{t, \alpha_t} \circ \dots \circ \mathcal O_{2, \alpha_2} \circ \mathcal O_{1, \alpha_1}.$$

The coefficients $\{ \eta_{\vec{\alpha}} \}$ form a quasi-probability distribution for the global circuit over the noisy circuits. Indeed it is easy to check that, at the level of super-operators, we have:

$$\mathcal U =  \sum_{\vec{\alpha}} \eta_{\vec{\alpha}} \Phi_{\vec{\alpha}}.$$

The one-norm 𝛾 of the global quasi-probability distribution is the product of those of the gates:

$$\sum_{\vec \alpha} \eta_{\vec{\alpha}}=1,  \qquad  \gamma = \sum_{\vec{\alpha}} |\eta_{\vec \alpha}| = \prod_{i=1}^{t} \gamma_i.$$

All the noisy expectation values $\langle A_{\vec{\alpha}}\rangle_{\rm noisy}$ can be directly measured with a noisy backend since they only require circuits composed of implementable noisy operations. In principle, by combining all the noisy expectation values, one could compute the ideal result $\langle A \rangle_{\rm ideal}$. Unfortunately this approach requires executing a number of circuits which grows exponentially with the circuit depth and which is typically unfeasible.

An important fact at the basis of PEC is that, for weak noise, only a small number of noisy expectation values actually contribute to the linear combination because many of the coefficients $\eta_{\vec{\alpha}}$ are negligible. For this reason, it is more efficient to estimate $\langle A \rangle_{\rm ideal}$ using an importance-sampling Monte Carlo approach as described in the next section.

## Monte Carlo estimation

To apply a Monte Carlo estimation, we need to replace quasi-probabilities with positive probabilities. This can be achieved as follows:

$$\mathcal{G_i} = \sum_{\alpha} \eta_{i, \alpha} \mathcal{O}_{i, \alpha}
= \gamma_i \sum_{\alpha} p_i(\alpha) \, {\rm sgn}(\eta_{i, \alpha})\, \mathcal{O}_{i, \alpha},$$

where $p_{i}(\alpha)=|\eta_{i, \alpha}|/\gamma_i$ is a valid probability distribution with respect to 𝛼.

If for each gate $\mathcal{G}_i$ of the circuit we sample a value of 𝛼 from $p_i$(𝛼) and we apply the corresponding noisy operation $O_{i,\alpha}$ we are effectively sampling a noisy circuit $\Phi_{\vec{\alpha}}$ from the global probability distribution $p(\vec{\alpha})= |\eta_{\vec{\alpha}}| / \gamma$.

Therefore, at the level of quantum channels, we have:

$$\mathcal U = \gamma \mathbb E \left\{  {\rm sgn}(\eta_{i, \vec{\alpha}}) \Phi_{\vec{\alpha}} \right\},$$

where $\mathbb E$ is the sample average over many repetitions of the previous probabilistic procedure and ${\rm sgn}(\eta_{\vec{ \alpha}}) = \prod_i {\rm sgn}(\eta_{i, \alpha})$. As a direct consequence, we can express the ideal expectation value as follows:

$$\langle A \rangle_{\text{ideal}} = \gamma\,
\mathbb E \left\{  {\rm sgn}(\eta_{\vec{\alpha}}) \langle A_{\vec{\alpha}}\rangle_{\rm noisy} \right\}.$$

By averaging a finite number 𝑁 of samples we obtain an unbiased estimate of $\langle A \rangle_{\text{ideal}}$. Assuming a bounded observable |𝐴|≤1, the number of samples 𝑁 necessary to approximate $\langle A \rangle_{\text{ideal}}$ within an absolute error 𝛿, scales as:

$$N \propto \frac{\gamma^2}{\delta^2}.$$

The term $\delta^2$ in the denominator is due to the stochastic nature of quantum measurements and is present even when directly estimating an expectation value without error mitigation. The $\gamma^2$ factor instead represents the sampling overhead associated to PEC. For weak noise and short circuits, 𝛾 is typically small and PEC is applicable with a reasonable cost. On the contrary, if a circuit is too noisy or too deep, the value of 𝛾 can be so large that PEC becomes unfeasible.

To apply PEC, you must know how to represent _ideal operations_ as linear combinations of _noisy implementable operations_. 

- By _ideal operations_, we mean noiseless unitary gates applied to specific qubits.
- By _noisy implementable operations_, we mean those noisy gates that can be applied to specific qubits by a real backend.

Since real backends are not perfect, the noisy implementable operations do not have an ideal unitary effect and typically correspond to non-unitary quantum channels.


How can we obtain the quasi-probability representations that are appropriate for a given backend? There are two main alternative scenarios.

- **Case 1:** The noise of the backend can be approximated by a simple noise model, such that quasi-probability representations can be analytically computed. For example, this is possible for depolarizing or amplitude damping noise.
- **Case 2:** The noise of the backend is too complex and cannot be approximated by a simple noise model.

Depending on the previous two cases, the method to obtain quasi-probability representations is different.

- **Method for case 1:** A simple noise model (e.g. depolarizing or amplitude damping) is typically characterized by a single `noise_level` parameter (or a few parameters) that can be experimentally estimated. Possible techniques for estimating the noise level are randomized-benchmarking experiments or calibration experiments. Often, gate error probabilities are reported by hardware vendors and can be used to obtain a good guess for the `noise_level` without running any experiments. Given the noise model and the `noise_level`, one can apply known analytical expressions to compute the quasi-probability representations of arbitrary gates.
- **Method for case 2:** Assuming an over-simplified noise model may be a bad approximation. In this case, the suggested approach is to perform the complete process tomography of a basis set of implementable noisy operations (e.g. the native gate set of the backend). One could also use _gate set tomography_ (GST), a noise characterization technique which is robust to state-preparation and measurement errors. Given the superoperators of the noisy implementable operations, one can obtain the quasi-probability representations as solutions of numerical optimization problems.

## Advantages

The main advantage of PEC is that, under the assumption of perfect gate tomography, it provides an unbiased estimation of expectation values. This means that, in the limit of many samples, the error mitigated expectation values converge to the ideal expectation values.

## Disadvantages

PEC is a noise-aware technique that converges to the ideal noiseless results only if we have the full tomographic knowledge of the hardware gates. Indeed, in order to represent ideal gates as linear combination of noisy gates, one typically needs to know the super-operator matrix associated to each noisy gate.

Another practical problem of PEC is that it involves the execution of many different circuits. This typically requires more clock time compared to the repeated execution of equal circuits. Batched execution of circuits, if supported by the hardware provider, can alleviate this problem to some extent.

**Notes**: 
- The general workflow of PEC is similar to the workflow of ZNE. The main difference is that in ZNE the auxiliary circuits are obtained by noise scaling, while in PEC they are probabilistically generated. As a consequence, the final inference step is different too.

**Open Questions**:
 - [ ]  


### References
- [1612.02058](https://arxiv.org/abs/1612.02058) (yet to read)
- [1712.09271](https://arxiv.org/abs/1712.09271) (yet to read)
- [1905.10135](https://arxiv.org/abs/1905.10135) (yet to read)
- [What is the theory behind PEC? ](https://mitiq.readthedocs.io/en/latest/guide/pec-5-theory.html)