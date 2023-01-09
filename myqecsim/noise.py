import numpy as np
import myqecsim.circuit as qcirc
import random
import myqecsim.pauli_tools as pt

class DepolarizingNoise:
    def __init__(self, probability) -> None:
        #self.num_qubits = num_qubits
        #self.prob = probability / pow(2, self.num_qubits)
        self.prob = probability

    def create_pauli_noise(self, gate = None, num_qubits = None):
        if isinstance(gate, qcirc.Gate):
            if gate.targets is not None:
                tmp = 1
            if gate.controls is not None:
                tmp += 1
        
        num_qubits = tmp

        # Only consider single and two qubits pauli noise 
        assert num_qubits == 1 or num_qubits == 2, "Number of qubits wrong"
        
        sample = pt.all_pauli_string(num_qubits)
        del sample[0]

        return random.choices(sample)[0]