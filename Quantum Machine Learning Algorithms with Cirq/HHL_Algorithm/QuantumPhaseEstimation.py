import cirq
from quantum_fourier_transform import QFT

class ControlledUnitary(cirq.Gate):

    def __init__(self, num_qubits, num_input_qubits, U):
        self._num_qubits = num_qubits
        self.num_input_qubits = num_input_qubits
        self.num_control_qubits = num_qubits - self.num_input_qubits
        self.U = U

    def num_qubits(self) -> int:
        return self._num_qubits

    def _decompose_(self, qubits):
        qubits = list(qubits)
        input_state_qubit = qubits[:self.num_input_qubits]
        control_qubits = qubits[self.num_input_qubits:]

        for i,q in enumerate(control_qubits):
            _pow_ = 2**(self.num_control_qubits -i -1)
            # yield self.U(q, *input_state_qubit)**_pow_
            yield
            cirq.ControlledGate(self.U**_pow_)
            (q, *input_state_qubit)

class QuantumPhaseEstimation:

    def __init__(self, U, input_qubits, num_output_qubits=None, output_qubits=None, initial_circuit=[], measure_or_sim=False):
        self.U = U
        self.input_qubits = input_qubits
        self.num_input_qubits = len(self.input_qubits)
        self.initial_circuit = initial_circuit
        self.measure_or_sim=  measure_or_sim

        if output_qubits is not None:
            self.output_qubits = output_qubits
            self.num_output_qubits = len(self.output_qubits)

        elif num_output_qubits is not None:
            self.num_output_qubits = num_output_qubits
            self.output_qubits = [cirq.LineQubit(i) for i in range(self.num_input_qubits, self.num_input_qubits+self.num_output_qubits)]

        else:
            raise ValueError("Atleast one of num_output_qubits or output_qubits to be specified")
        
        self.num_qubits = self.num_input_qubits + self.num_output_qubits

    def inv_qft(self):
        self._qft_ = QFT(qubits=self.output_qubits)
        self._qft_.qft_circuit()
        self.QFT_inv_circuit = self._qft_.inv_circuit

    def circuit(self):
        self.circuit = cirq.Circuit()
        self.circuit.append(cirq.H.on_each(*self.output_qubits))
        print(self.circuit)
        print(self.output_qubits)
        print(self.input_qubits)
        print((self.output_qubits + self.input_qubits))
        self.qubits = list(self.input_qubits
        + self.output_qubits)
        self.circuit.append(ControlledUnitary(
        self.num_qubits, self.num_input_qubits,
        self.U)(*self.qubits))
        self.inv_qft()
        self.circuit.append(self.QFT_inv_circuit)
        if len(self.initial_circuit) > 0 :
            self.circuit = self.initial_circuit
            + self.circuit

    def measure(self):
        self.circuit.append(cirq.measure(*self.output_qubits, key = 'm'))

    def simulate_circuit(self, measure=True):
        sim = cirq.Simulator()
        if measure == False:
            result = sim.simulate(self.circuit)
        else:
            result = sim.run(self.circuit, repetitions=1000).histogram(key='m')
        return result