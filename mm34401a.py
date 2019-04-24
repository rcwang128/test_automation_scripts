import visa
from matplotlib import pyplot as plt
import numpy as np
import time

rm = visa.ResourceManager()
device_list = rm.list_resources()
print(device_list)
for n in device_list:
    if "GPIB0::" in n:
        device = n
        break
inst = rm.open_resource(device)
print(inst, "is connected.")
#inst.write("*RST; *CLS")
time.sleep(0.5)
print(inst.query("*IDN?"))
time.sleep(0.5)

inst.write("DISP OFF")

interval_in_ms = 50
number_of_readings = 120

def config():
    inst.write("CONF:CURR:DC 1, 0.00001")
    inst.write("TRIG:SOUR IMM")
    inst.write("TRIG:DEL %f" % (interval_in_ms / 1000.0))
    inst.write("TRIG:COUN %d" % number_of_readings)
    inst.write("INIT")

t_start = time.perf_counter()
config()
time.sleep(60)
currents = inst.query("FETCh?")
t_elapsed = time.perf_counter() - t_start

#print(inst.query("SYSTem:ERRor?"))
time.sleep(0.5)
inst.write("DISP ON")
inst.close()

# Data processing
currents = currents.split(",")
for n in range(len(currents)):
    currents[n] = float(currents[n]) * 1000
    print(currents[n])

#print(currents)
#print(len(currents))
print("{:.2f} s".format(t_elapsed))


t = np.arange(0., 60., interval_in_ms / 1000.0)
plt.title("Current Log " + str(interval_in_ms) + "ms Interval")
plt.ylabel("Currents (mA)"); plt.xlabel("Time")
plt.axis([0, 60, 0, 8])
plt.plot(t, currents, "bs")
plt.show()



'''
#config_current()
inst.write("DISP OFF")
currents = []
t_start = time.perf_counter()
#for i in range(100):
for i in range(2000):
    value = inst.query("MEASure:CURRent:DC? 1, 0.00001")
    currents.append(value)
    time.sleep(0.05)
t_elapsed = time.perf_counter() - t_start

inst.close()
#for n in range(len(currents)):
#    currents[n] = int(currents[n].rstrip()) * 1000

for current in currents:
    print(current.rstrip())
#print(len(currents))
print("{:.2f} s".format(t_elapsed))
'''

