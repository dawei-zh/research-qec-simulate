import numpy as np
import myqecsim.circuit as qcirc
import myqecsim.pauli_tools as pt
import itertools as it

def run_circuit(circuit, shot, noise = None, initial_pauli = None, verbose = None):
    assert isinstance(circuit, qcirc.Circuit), "Wrong input circuit"

    if initial_pauli is not None:
        _initial_pauli_string = initial_pauli
    else:
        _initial_pauli_string = ["".join(i) for i in it.product(['I'], repeat=circuit.tot_qubits)][0]

    assert len(_initial_pauli_string) == circuit.tot_qubits, "Wrong initial Pauli string"
    
    results = []
    circuit._clear_noise()

    for i in range(shot):
        circuit._clear_noise()
        if verbose == 1 and i % 5000 == 0:
            print(i)
        if noise is not None:
            circuit._clear_noise()
            circuit._noise_gate(noise.prob)

        _pauli_string = _initial_pauli_string # Initialize pauli string for single shot

        for j in range(len(circuit.gates)):
            _gate = circuit.gates[j]

            # Convert whole string into one- or two-qubits string
            # Note that the controlled qubit number might be larger than target qubit
            # _tmp_pauli_string = 'control' + 'target'
            _tmp_pauli_string = ''
            if _gate.controls is not None:
                _tmp_pauli_string += _pauli_string[_gate.controls - 1]

            _tmp_pauli_string += _pauli_string[_gate.targets - 1]

            # Normal operation
            _tmp_pauli_string = _gate._pauli_operation(_tmp_pauli_string)
            
            # Noise operation
            if _gate.noise_flag == True:
                _tmp_pauli_bsf = pt.pauli_to_bsf(_tmp_pauli_string)
                _tmp_noise_bsf = pt.pauli_to_bsf(noise.create_pauli_noise(_gate))
                _tmp = pt.pauli_product_bsf(_tmp_pauli_bsf, _tmp_noise_bsf)
                _tmp_pauli_string = pt.bsf_to_pauli(_tmp)

            # Put the result back to whole string
            # Split the string into a list of characters
            _tmp = [i for i in _pauli_string]
            if _gate.controls is not None:
                _tmp[_gate.controls - 1] = _tmp_pauli_string[0]
            _tmp[_gate.targets - 1] = _tmp_pauli_string[-1]

            # Combine the list of characters into a string
            _pauli_string = ''
            for i in _tmp:
                _pauli_string += i
            
        results.append(_pauli_string)

    return results
