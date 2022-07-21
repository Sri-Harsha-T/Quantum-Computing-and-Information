import cirq
import numpy as np
import math

class EigenValueInversion(cirq.Gate):
    """
    Rotates the ancilla bit around the Y axis
    by an angle theta = 2* sin inv(C/eigen value)
    corresponding to each Eigen value state basis |eigen value>.
    This rotation brings the factor (1/eigen value) in
    the amplitude of the basis |1> of the ancilla qubit
    """

    def __init__(self, num_qubits, C, t):
        super(EigenValueInversion, self)
        self._num_qubits_ = num_qubits
        self.C = C
        self.t = t
        # No of possible Eigen values self.N
        self.N = 2**(num_qubits - 1)

    def num_qubits(self):
        return self._num_qubits