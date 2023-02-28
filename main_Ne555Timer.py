import math     
import matplotlib.pyplot as pplot


####  Constants  ###############################################################

vin = 5.0           # Voltage in

out_high = 3.3      # Voltage output from pin 3 when "high" 
out_low  = 0.25     # Voltage output from pin 3 when "low"
                    # (These are not simply vin and zero. See datasheet.)

farads = 2/1000000  
ohms_a = 1000       
ohms_b = 100000     
sim_time = 1       
step = sim_time / 1000  




def update_latch(latch, trigger, threshold, vin):
    
    if trigger < vin / 3:
        latch = True
    
    
    if threshold > vin * 2 / 3:
        latch = False
        
    return latch
    


def update_capacitor(cap, farads, res_a, res_b, vin, latch, step):

    if latch:
        
        tc = farads * (res_a + res_b)
        # Time proportion
        tp = step / tc
        # Percent change from existing voltage to full voltage (vin)
        pc = 1 - (1/math.e**tp)
        cap += (vin - cap) * pc
    else:
        # Discharging...
        # Calculate time constant based on going through resistor B only
        tc = farads * res_b
        # Time proportion
        tp = step / tc
        # Percent change from existing voltage down to zero
        pc = 1 - (1/math.e**tp)
        cap -= cap * pc

    return cap



time = 0
cap = 0
latch = True
vout = out_high

cap_list = []
out_list = []
time_list = []


####  Simulate  

while time < sim_time:
    cap = update_capacitor(cap, farads, ohms_a, ohms_b, vin, latch, step)
    latch = update_latch(latch, cap, cap, vin)
    if latch:
        vout = out_high
    else:
        vout = out_low
    cap_list.append(cap)
    out_list.append(vout)
    time_list.append(time)
    time += step
    


# Print constants
print()
print('Capacitor: ' + str(farads * 1000000) + 'mf')
print('Resistor A: ' + str(ohms_a/1000) + 'K')
print('Resistor B: ' + str(ohms_b/1000) + 'K')
print('Vcc: +' + str(vin) + 'V')
print()

time_high = 0.693 * (ohms_a + ohms_b) * farads
time_low = 0.693 * ohms_b  * farads
time_total = time_high + time_low
print('Time high: ' + str(time_high*1000) + 'ms')
print('Time low: ' + str(time_low*1000) + 'ms')
print('Total period: ' + str(time_total*1000) + 'ms')
print('Duty cycle: ' + str(round(time_high/time_total*100, 2)) + '%')
print('Frequency: ' + str(round(1/time_total, 2)) + 'Hz')
print('Periods simulated: ' + str(len(time_list)))
print()



# Capacitor voltages
pplot.plot(time_list, cap_list, label='Capacitor')
# Output (Q) voltages
pplot.plot(time_list, out_list, label='Output')
pplot.xlabel('Time (Seconds)')
pplot.ylabel('Volts')
pplot.ylim(0, vin)
pplot.legend(loc='upper right')

pplot.show()