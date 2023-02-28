# TImer-NE555-astabel-
this repo contain the simulation of TImer NE55 in mode astable 


#### Simulation Ne555 Timer in three way

**Notation:** **since we don't have device Ne555 Timer we wwill try to simulate the behaviour of device in three easy ways 


folder **appSimulate**  has the application realTime simulation using Dash components 

```python
python real_rime.py
```
folder **circuit**  has the build Schema of circuit realTime simulation using Pyspecie Package ***Setup***

1. install ngspecies command interface to run file circuit simulation
2. ne555.cir should include file TLC555 
```C++
ngspecies ne555.cir 
```


folder **main**  is plot of ne555 using call function update_cap and update_latch
```python 
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
```