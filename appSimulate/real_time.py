import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import numpy as np
from PySpice.Spice.Library import SpiceLibrary
import time
import math

# Define constants for the circuit
R1 = 10000
R2 = 10000
C1 = 0.0000001
INITIAL_VOLTAGE = 0
VCC = 5
SIMULATION_TIME = 0.1

# Initialize the time and voltage lists for the capacitor and output
times = []
cap_voltages = []
out_voltages = []

# Calculate the frequency and duty cycle of the circuit
frequency = 1.44 / ((R1 + 2 * R2) * C1)
duty_cycle = (R1 + R2) / (R1 + 2 * R2)

# Define a function to simulate the behavior of an astable 555 timer circuit
def simulate_astable():
    global times, cap_voltages, out_voltages
    # Clear the lists
    times = []
    cap_voltages = []
    out_voltages = []
    # Simulate the behavior of the circuit for the specified amount of time
    for t in np.arange(0, SIMULATION_TIME, 0.00001):
        capacitor_voltage = INITIAL_VOLTAGE + VCC * (1 - math.exp(-t / (R1 + 2 * R2) / C1))
        cap_voltages.append(capacitor_voltage)
        out_voltages.append(VCC if capacitor_voltage > (duty_cycle * VCC) else 0)
        times.append(t)
        time.sleep(0.00001)

# Simulate the circuit initially
simulate_astable()

# Set up the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("555 Timer Astable Mode Simulation"),
    html.Div([
        html.Div([
            dcc.Graph(id="cap_graph", animate=True),
            dcc.Interval(id="cap_interval", interval=1000, n_intervals=0)
        ], className="six columns"),
        html.Div([
            dcc.Graph(id="out_graph", animate=True),
            dcc.Interval(id="out_interval", interval=1000, n_intervals=0)
        ], className="six columns")
    ], className="row")
])

# Define the callbacks for the graphs
@app.callback(
    dash.dependencies.Output("cap_graph", "figure"),
    dash.dependencies.Input("cap_interval", "n_intervals")
)
def update_cap_graph(n=8):
    # Simulate the circuit
    simulate_astable()
    # Create the plot
    fig = px.line(x=times, y=cap_voltages, labels={"x": "Time (s)", "y": "Capacitor Voltage (V)"})
    fig.update_layout(title="Capacitor Voltage vs. Time")
    return fig

@app.callback(
    dash.dependencies.Output("out_graph", "figure"),
    dash.dependencies.Input("out_interval", "n_intervals")
)
def update_out_graph(n=8):
    # Simulate the circuit
    simulate_astable()
    # Create the plot
    fig = px.line(x=times, y=out_voltages, labels={"x": "Time (s)", "y": "Output Voltage (V)"})
    fig.update_layout(title="Output Voltage vs. Time")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
    