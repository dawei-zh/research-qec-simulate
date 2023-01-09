import numpy as np
import myqecsim.pauli_tools as pt
import random

_single_qubit_gates = ["RX", "RY", "RZ", "PHASEGATE", "X", "Y", "Z", "S", "T", "QASMU"]
_ctrl_gates = ["CNOT"]
_swap_like = ["SWAP", "ISWAP", "SQRTISWAP", "SQRTSWAP", "BERKELEY",
              "SWAPalpha"]

class Gate:
    def __init__(self, targets=None, controls=None, para=None):
        """
        Create a gate with specified parameters. Number of qubit starts from 1
        """
        self.targets = targets
        self.controls = controls
        if para is not None:
            self.para = para
        self.noise_flag = False # noise_flag = True means the gate is noisy

class Circuit:
    def __init__(self, num_qubits):
        # number of qubits in the register
        self.tot_qubits = num_qubits
        self.gates = []
        self._index = None

    def add_gate(self, gate, targets=None, controls=None, arg_value=None):
        if isinstance(gate, Gate):
            self.gates.append(gate)

    def _clear_noise(self):
        for i in range(len(self.gates)):
            self.gates[i].noise_flag = False

    def _noise_gate(self, noise_prob):
        #noise_prob = noise.prob
        random_flag = [random.uniform(0, 1) for i in range(len(self.gates))]

        for i in range(len(random_flag)):
            if random_flag[i] <= noise_prob:
                self.gates[i].noise_flag = True

class CNOT(Gate):
    def __init__(self, controls, targets, para=None):
        super().__init__(targets, controls, para)
        self.name = 'cnot'


    def _pauli_operation(self, input):

        if isinstance(input, np.ndarray):
            input = pt.bsf_to_pauli(input)

        # ignore minus sign in some cases
        _cnot_propagation = {'II': 'II', 'IX': 'IX', 'IY': 'ZY', 'IZ':'ZZ', 
                             'XI': 'XX', 'XX': 'XI', 'XY': 'YZ', 'XZ':'YY',
                             'YI': 'YX', 'YX': 'YI', 'YY': 'XZ', 'YZ':'XY',
                             'ZI': 'ZI', 'ZX': 'ZX', 'ZY': 'IY', 'ZZ':'IZ'}

        return _cnot_propagation[input]

class H(Gate):
    def __init__(self, targets, controls=None, para=None):
        super().__init__(targets, controls, para)
        self.name = 'hadamard'


    def _pauli_operation(self, input):

        if isinstance(input, np.ndarray):
            input = pt.bsf_to_pauli(input)

        # ignore minus sign in some cases
        _hadamard_propagation = {'I': 'I', 'X': 'Z', 'Y': 'Y', 'Z':'X'}

        return _hadamard_propagation[input]

class Rx(Gate):
    def __init__(self, targets, angle):
        super().__init__(targets, para = angle)
        self.name = 'rotation X'
        self.angle = angle


    def _pauli_operation(self, input):

        if isinstance(input, np.ndarray):
            input = pt.bsf_to_pauli(input)

        # Consider only first term
        _rx_propagation = {'I': 'I', 'X': 'X', 'Y': 'Y', 'Z':'Z'}

        return _rx_propagation[input]

class Rz(Gate):

    def __init__(self, targets, angle):
        super().__init__(targets, para = angle)
        self.name = 'rotation Z'
        self.angle = angle


    def _pauli_operation(self, input):

        if isinstance(input, np.ndarray):
            input = pt.bsf_to_pauli(input)

        # Consider only first term
        _rz_propagation = {'I': 'I', 'X': 'X', 'Y': 'Y', 'Z':'Z'}

        return _rz_propagation[input]

class Rx_pi(Gate):
    def __init__(self, targets, sign):
        super().__init__(targets, para = sign)
        self.name = 'rotation X pi/2'
        self.sign = sign

    def _pauli_operation(self, input):

        if isinstance(input, np.ndarray):
            input = pt.bsf_to_pauli(input)

        # Consider only first term
        _rxpi_propagation = {'I': 'I', 'X': 'X', 'Y': 'Z', 'Z':'Y'}

        return _rxpi_propagation[input]

class SWAP(Gate):
    def __init__(self, targets, controls, para=None):
        super().__init__(targets, controls)
        self.name = 'swap'

    def _pauli_operation(self, input):

        if isinstance(input, np.ndarray):
            input = pt.bsf_to_pauli(input)

        # ignore minus sign in some cases
        _swap_propagation = {'II': 'II', 'IX': 'XI', 'IY': 'YI', 'IZ':'ZI', 
                             'XI': 'IX', 'XX': 'XX', 'XY': 'YX', 'XZ':'ZX',
                             'YI': 'IY', 'YX': 'XY', 'YY': 'YY', 'YZ':'ZY',
                             'ZI': 'IZ', 'ZX': 'XZ', 'ZY': 'YZ', 'ZZ':'ZZ'}

        return _swap_propagation[input]