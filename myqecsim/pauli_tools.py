import numpy as np
import itertools as it

def pauli_to_bsf(pauli):
    """
    Convert the given Pauli operator(s) to binary symplectic form.
    XIZIY -> (1 0 0 0 1 | 0 0 1 0 1)
    Assumptions:
    * pauli is a string of I, X, Y, Z such as 'XIZIY' or a list of such strings of the same length.
    :param pauli: A single or list of Pauli operators.
    :type pauli: str or list of str
    :return: Binary symplectic representation of Pauli.
    :rtype: numpy.array (1d or 2d)
    """

    def _to_bsf(p):
        ps = np.array(list(p))
        xs = (ps == 'X') + (ps == 'Y')
        zs = (ps == 'Z') + (ps == 'Y')
        return np.hstack((xs, zs)).astype(int)

    if isinstance(pauli, str):
        return _to_bsf(pauli)
    else:
        return np.vstack([_to_bsf(p) for p in pauli])

def bsf_to_pauli(bsf):
    """
    Convert the given binary symplectic form to Pauli operator(s).

    (1 0 0 0 1 | 0 0 1 0 1) -> XIZIY

    Assumptions:

    * bsf is a numpy.array (1d or 2d) in binary symplectic form.

    :param bsf: Binary symplectic vector or matrix.
    :type bsf: numpy.array (1d or 2d)
    :return: Pauli operators.
    :rtype: str or list of str
    """
    assert np.array_equal(bsf % 2, bsf), 'BSF is not in binary form'

    def _to_pauli(b, t=str.maketrans('0123', 'IXZY')):  
        xs, zs = np.hsplit(b, 2)
        ps = (xs + zs * 2).astype(str)  # 0=I, 1=X, 2=Z, 3=Y
        return ''.join(ps).translate(t)

    if bsf.ndim == 1:
        return _to_pauli(bsf)
    else:
        return [_to_pauli(b) for b in bsf]

def all_pauli_string(num_qubits): 
    return ["".join(i) for i in it.product(['I', 'X', 'Y', 'Z'], repeat=num_qubits)]

def pauli_product_bsf(a, b):
    """
    ........

    :param a: LHS binary symplectic vector or matrix.
    :type a: numpy.array (1d or 2d)
    :param b: RHS binary symplectic vector or matrix.
    :type b: numpy.array (1d or 2d)
    :return: Binary symplectic product of A with B.
    :rtype: int if A and B vectors; numpy.array (1d if A or B vector, 2d if A and B matrices)
    """
    assert np.array_equal(a % 2, a), 'BSF {} is not in binary form'.format(a) # use mod 2 to check
    assert np.array_equal(b % 2, b), 'BSF {} is not in binary form'.format(b) # use mod 2 to check
    return (a + b) % 2

def commute(a, b):
    """
    Check whether Pauli string a commutes with Pauli string b. 
    Return True if a and b commutes. Return False if a and b anti-commutes
    """
    # Be careful here, we cannot use bst product to determine
    # since the bst product does not include phase
    assert len(a) == len(b), "Input do not have same size"

    anticommute = 0
    anticommute_set = {'XY', 'YX', 'XZ', 'ZX', 'YZ', 'ZY'}

    for i in range(len(a)):
        tmp = a[i] + b[i]
        if tmp in anticommute_set:
            anticommute += 1
            
    if anticommute%2 == 0:
        return True
    else:
        return False


