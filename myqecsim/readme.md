## My QEC Simulation Python Code

Only for usage of my simple $[[4,2,2]]$ code and surface code simulator. Think about future combination with Qiskit and fast Clifford circuit simulator

#### Simulate Circuit Noise

Here is basic idea to simulate circuit noise and evaluate performance of QEC code. Idea follows the code from Ben

* Step 1: Specify the QEC code, including $n, k, d$, stabilizer and logical operators. We need to **check** (1) the stabilizer commutes with each other and logical operators, and (2) the distance of code matches the minimum weight of logical operators.
* Step 2: Specify error model and quantum circuit
* Step 3: Starting with identity, generate final Pauli string after executing the circuit
* Step 4: Correct or detect the error by decoder

The Pauli string simulation bases on the symplectic matrix. 

#### Code Structure

According to above illustration and also original `qecsim` package, the code should include six parts: 
* Stabilizer code, including $[[n,k,d]]$, stabilizers, logical $X$ and $Z$ operators
* Circuit construction, including circuit object and basic gates objects
* Error Model, generate error under some probability distribution
* Error propagation, including the error propagation of every quantum gate.
* Decoder/syndrome measurement. For error correction, we need to include the recovery process.
* Execution of circuit

Parts of my code is adapted from `qecsim`, `qutip` and `qiskit`. 

---

Here are details of how to create a quantum circuit for pauli string simulation

* Initialize `circ = Circuit(num_qubits)` 
* Add gates `circ.add_gate(gate)`. After adding gates, we should have a list of objects as child of `Gate`
  * Specify child class `cnot`, `h`, `rx`, `rx_pi`, `rz`, `swap`
  * Specify child class operation `gate._pauli_operation(input)`. Use the error propagation maps (a dictionary) to create output

---

Here are details of how to create deploarizing noise

* Initialize `noise = DepolarizingNoise(prob)`  

---

Here is detailed execution process with given circuit 

* `run_circuit(circuit, shot, noise, initial)`
  * Specify initial Pauli string. We can specify stabilizer to test the `_normal_operation` with no noise.  
  * If `noise is not None`, use `circ.noise_gate(prob)` to specify which gate should have error by setting `noise_flag = True`
  * For all gates in circuit, do following for one shot,
    * `_normal_operation(input, gate)` using `gate._pauli_operation` (be careful about which is target and which is control) and put the Pauli string in proper qubit via `gate.target` and `gate.control`. This will return the Pauli string after some gates, with mapping
      * Normal gates, $\rm CNOT$, $H$, $R_{x}(\pi/2)$, $\rm SWAP$
      * Special gate, $R_x(\theta)$ and $R_{z}(\theta)$ **Most important, sum of Pauli string**
    * If the given gate is noisy `noise_flag = True`, then run `_noise_operation(noise_model = noise, gate)`. Here is three steps
      * Run `noise_model.create_pauli_noise()` create a noise
      * Put the noise in proper qubit via `gate.target` and `gate.control`
      * Get new Pauli string by `pauli_product_bsf` 
* `decoder(qec_code, ancilla, output)` Check whether the output anti-commutes with normal stabilizer and ancilla stabilizer using the `pauli_tools.commute(pauli_str1, pauli_str2)` . Return `True` if error is detectable

----

Required function and classes

* For Pauli string, we might need a special class `PauliString` to deal with rotation gate. But *from the error propagation analysis, we might only deal with one term when rotation gate occurs since two terms can be detected by same stabilizer or same ancilla at the same time.* (future)
* For depolarizing noise, we need to create all possible $n-$qubit pauli strings