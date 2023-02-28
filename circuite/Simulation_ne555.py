from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Spice.Netlist import SubCircuitFactory, Circuit, SubCircuit, Pin, Node

import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Define the NE555 subcircuit using Pins
# Define the NE555 subcircuit using Pins
class NE555(SubCircuitFactory):
    __name__ = 'NE555'

    def __init__(self):
        super().__init__()

        self.pins = [
            Pin(1, 'CTRL'),
            Pin(2, 'TRIGGER'),
            Pin(3, 'OUTPUT'),
            Pin(4, 'RESET'),
            Pin(5, 'CONTROL_VREF'),
            Pin(6, 'THRESHOLD'),
            Pin(7, 'DISCHARGE'),
            Pin(8, 'VCC')
        ]

        self.model('NE555', 'sw')
        self.X('X1', 'NE555', *[pin.name for pin in self.pins])



# Define the circuit and subcircuit instances
spice_library = SpiceLibrary('pyspice')
circuit = Circuit('NE555 Astable')
ne555 = NE555('X1')

# Create the circuit and subcircuit instances
circuit = Circuit('NE555 Astable')

ne555 = NE555()

# Define the circuit components
circuit.V('input', '+15V', ne555['TRIGGER'], 15@u_V)
circuit.R(1, ne555['TRIGGER'], ne555['CTRL'], 10@u_kΩ)
circuit.R(2, ne555['CTRL'], '+15V', 10@u_kΩ)
circuit.R(3, ne555['CTRL'], '-15V', 10@u_kΩ)
circuit.C(1, ne555['OUTPUT'], ne555['DISCHARGE'], 1@u_uF)
circuit.R(4, ne555['OUTPUT'], ne555['THRESHOLD'], 10@u_kΩ)
circuit.R(5, ne555['THRESHOLD'], '-15V', 10@u_kΩ)
circuit.R(6, ne555['CONTROL_VREF'], '-15V', 10@u_kΩ)
circuit.C(2, ne555['CONTROL_VREF'], ne555['CTRL'], 10@u_uF)
circuit.R(7, ne555['DISCHARGE'], '-15V', 1@u_kΩ)

ne555.build(circuit)

# Define the simulation parameters
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
simulator.include(spice_library['1N4148'])
simulator.include(spice_library['LM358'])
simulator.include(spice_library['NE555'])

waveforms = simulator.transient(step_time=1@u_us, end_time=100@u_ms)

time = waveforms.time.as_ndarray()
voltage_out = waveforms['OUTPUT'].as_ndarray()
voltage_ctrl = waveforms['CTRL'].as_ndarray()

fig = make_subplots(rows=2, cols=1, shared_xaxes=True)

fig.add_trace(
    go.Scatter(x=time, y=voltage_ctrl, name='Control Voltage'),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(x=time, y=voltage_out, name='Output Voltage'),
    row=2, col=1
)

fig.update_layout(title='NE555 Astable Simulation',
                  xaxis_title='Time [s]',
                  yaxis_title='Voltage [V]')
fig.show()
