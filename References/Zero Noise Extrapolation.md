Zero-noise extrapolation (ZNE) is an error mitigation technique in which an expectation value is computed at different noise levels and, as a second step, the ideal (i.e. *noiseless*) expectation value is inferred by extrapolating the measured results to the zero-noise limit.

The two steps are:

- **Step 1: Intentionally scale noise**. This can be done with different methods. _Pulse-stretching_ can be used to increase the noise level of a quantum computation. Similar results can be obtained, at a gate-level, with _unitary folding_ or _identity insertion scaling_.
- **Step 2: Extrapolate to the noiseless limit**. This can be done by fitting a curve (often called _extrapolation model_) to the expectation values measured at different noise levels to extrapolate the noiseless expectation value.

## Step 1: Intentionally scale noise.

A technique to increase the noise level of a circuit at the gate level is to intentionally increase its depth. This can be obtained using either _unitary folding_ or _identity scaling_.

In _unitary folding_, we perform a mapping 𝐺↦𝐺𝐺†𝐺. This mapping can be applied _globally_ or _locally_ (first and second image)
![Global Folding](https://mitiq.readthedocs.io/en/latest/_images/zne_global_folding.png)
![Local Folding](https://mitiq.readthedocs.io/en/latest/_images/zne_local_folding.png)

In _identity insertion scaling_, we perform a mapping 𝐺↦𝐼𝐺. This mapping can be applied as shown in the diagram below.

![Identity insertion](https://mitiq.readthedocs.io/en/latest/_images/zne_id_scaling_layers.png)

Additional details on the theory of identity insertion scaling are similar to those in unitary folding. The only difference is that instead of scaling gate noise, the insertion of an identity gate increases the wait time after each circuit layer is executed. This allows the qubits to interact with the environment through some noisy process and decohere if the system-environment interaction is strong. The decoherence time for the qubits in a quantum system is determined by the amount of time our system of interest remains coherent and uncouples from the external environment.

A noise scaling technique similar to unitary folding is _pulse-stretching_: a method that only applies to devices with pulse-level access. The noise of the device can be altered by increasing the time over which pulses are implemented.

## Step 2: Extrapolate to the noiseless limit

In both gate-model and pulse-model scenarios, let 𝜏 be a parameter quantifying noise level in the circuit and let 𝜏′=𝜆𝜏 the scaled noise level.
For 𝜆=1, the input circuit remains unchanged since the noise level 𝜏′=𝜏 is the same as the noise of the physical device without any scaling.

Let 𝜌(𝜏′) be the state prepared by a noise scaled quantum circuit. The expectation value of an observable 𝐴 can be described as a function of the noise scaling parameter as follows:
$$\langle E(\lambda) \rangle = \text{Tr}[\rho(\tau') A] = \text{Tr}[\rho(\lambda \tau) A]$$
The idea of ZNE is that one can estimate the ideal expectation value ⟨𝐸(𝜆=0)⟩, by measuring a range of different expectation values ⟨𝐸(𝜆)⟩ for different values of 𝜆≥1 and extrapolating to the zero-noise limit.

In practice the extrapolation can be done as follows:

1. Assume $E(\lambda)\simeq f(\lambda; p_1, p_2, ... p_m)$, where 𝑓 is an _extrapolation model_, i.e., a function of 𝜆 depending on a set of real parameters $p_1, p_2, ... p_m$.
2. Fit the function 𝑓 to the measured noise-scaled expectation values, obtaining an optimal set of parameters $\tilde p_1, \tilde p_2, \dots \tilde p_m$.
3. Evaluate the corresponding zero-noise limit, i.e., $f(0; \tilde p_1, \tilde p_2, \dots \tilde p_m)$.

Different choices of 𝑓, produce different extrapolations. Typical choices for 𝑓 are: a linear function, a polynomial, an exponential. For example, Richardson extrapolation, corresponds to the following polynomial model:

$$f(\lambda; p_1, p_2, ... p_m) = p_1 + p_2 \lambda + p_3 \lambda^2 + \dots p_m \lambda^{m-1},$$

where 𝑚 is equal to the number of data points in the fit (i.e. the number of noise scaled expectation values).

One can select a noise scaling method via _noise scaling functions_. A noise scaling function takes a circuit and a real scale factor as two inputs and returns a new circuit. The returned circuit is equivalent to the input one (if executed on a noiseless backend), but is more sensitive to noise when executed on a real noisy backend. In practice, by applying a noise scaling function before the execution of a circuit, one can indirectly scale up the effect of noise. The noise scaling function can either increase the total circuit execution time by inserting unitaries or increase the wait times in the middle of a circuit execution. These two methods are the aforementioned _unitary folding_ and _identity scaling_ respectively.

**The special case of odd integer scale factors**
For any noise scaling function, if `scale_factor` is equal to 1, the input circuit is unchanged and it is subject to the base noise of the backend.
Both local and global folding, if applied uniformly to all the gates of `circuit`, produce a `scaled_circuit` that has 3 times more gates than the input `circuit`. This corresponds to the `scale_factor=3` setting.

**The general case of real scale factors**
More generally, the `scale_factor` can be set to any real number larger than or equal to one. In this case, Mitiq applies additional folding to a selection of gates (for local folding) or to a final fraction of the circuit (for global folding), such that the total number of gates is _approximately_ scaled by `scale_factor`.

### Identity Scaling

The goal of this technique is to insert layers of identity gates to extend the duration of the circuit, which, when used in the context of ZNE, provides a useful noise-scaling method. Mathematically, this is represented as composing identity operations after the target unitary 𝐺.

𝐺⟶𝐼𝐺

Here, 𝐺 is a single circuit layer containing individual that can be performed simultaneously.

#### Integer and Real Scale Factors

When the scale factor is 1, no identity layers are inserted and circuit depth remains unchanged.

For some scale factor greater than 1, there will need to be some layers inserted non-uniformly to approach the desired scale factor. This is determined by the scale factor being an integer or a float.

- When the scale factor is an integer, identity layers are inserted uniformly after each moment in the input circuit.
- When the scale factor is a non-integer, identity layers are inserted uniformly until the closest integer less than the scale factor is achieved. Then the layers are inserted at random to achieve a value approximately close to the intended scale factor. If the scale factor is a non-integer greater than or equal to 1, the identity layer insertion can be described as a mix of uniform and randomly inserted layers. In some cases, achieving the exact scale factor is not possible, but this method will insert identities appropriately to closely approximate it.

## Advantages

Zero noise extrapolation is one of the simplest error mitigation techniques and, in many practical situations, it can be applied with a relatively small sampling cost. The main advantage of ZNE is that the technique can be applied without a detailed knowledge of the undelying noise model. Therefore it can be a good option in situations where tomography is impractical.

## Disadvantages

In some instances the results of the extrapolation can exhibit a large bias. ZNE may not be helpful in cases where a low degree polynomial curve obtained by fitting the noisy expectation values does not match the zero-noise limit. When using circuits of less trivial depth on real devices, the lowest error points may be too noisy for the extrapolation to show improvement over the unmitigated result.


**Notes**: 
-  _if `scale_factor` is not an odd integer and if the input circuit is very short, there can be a large error in the actual scaling of the number of gates. For this reason, when dealing with very short circuits, we suggest to use odd integer scale factors._
- For identity scaling, two options are available: fixed identity insertion method (FIIM) and random identity insertion method (RIIM). The latter and newer method provides better results both in terms of number of gates and effective mitigation. Whilst in the FIIM after every gate 2n+1 CNOT (or generally unitaries) are added, in the RIIM n is promoted to a random variable $n_i$ that changes for every gate in the original circuit (more details in reference [[Zero Noise Extrapolation#^21ca86|1]]). 

**Open Questions**:
 - [ ]  

### References
- [2003.04941 (arxiv.org)](https://arxiv.org/pdf/2003.04941))  ^21ca86
- [1611.09301](https://arxiv.org/abs/1611.09301) (yet to read)
- [1612.02058](https://arxiv.org/abs/1805.04492) (yet to read)
- [1805.04492](https://arxiv.org/abs/1805.04492) (yet to read)
- [What is the theory behind ZNE?](https://mitiq.readthedocs.io/en/latest/guide/zne-5-theory.html)