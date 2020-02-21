import RPi.GPIO as GPIO
import time
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as GPIOp
import numpy as np
# import matplotlib.pyplot as plt

from multiprocessing import Process, Value, Array

import os
import datetime

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Pinouts for Relay Connectors
comp       = 16
safety_sol = 11
vent_sol   = 13
launch_sol = 15

LP = input("Enter Launch Pressure: ")
LP = float(LP) + 15.4
FP  = LP * 10.23 # fake pressure
if LP  >= 75: 
    exit()

SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=GPIOp.SpiDev(SPI_PORT, SPI_DEVICE))

# Set Pins
GPIO.setup(comp, GPIO.OUT)
GPIO.setup(safety_sol, GPIO.OUT)
GPIO.setup(vent_sol, GPIO.OUT)
GPIO.setup(launch_sol, GPIO.OUT)

# Clear Pins
GPIO.output(comp, 1)
GPIO.output(safety_sol,1)
GPIO.output(vent_sol,1)
GPIO.output(launch_sol,1)

def read_trans(value, state):
    start = time.time()
    j = 0
    x = []
    y = []
    while True:
        # read pressures
        for i in range(3):
            value[i] = mcp.read_adc(i)
        
        # save pressures to file
        file.write('| {0:.4f} | {1:.4f} | {2:.4f} | time: {3:.4f}\n'.format(value[0]/10.23 - 15.4, 
                                                                            value[1]/10.23 - 15.4, 
                                                                            value[2]/10.23 - 15.4, time.time() - start))
        # add points  to graph
        x.append(time.time() - start)
        y.append(value[0]/10.23 - 15.4)
        
        #print values every 10 data points
        if j % 10 == 0:
            print('| {0:.4f} | {1:.4f} | {2:.4f} | time: {3:.4f}'.format(value[0]/10.23 - 15.4, 
                                                                         value[1]/10.23 - 15.4, 
                                                                         value[2]/10.23 - 15.4, time.time() - start))
        #shleep and increment
        time.sleep(.02)
        j += 1
             
        # if launch is done, create graph and exit
        if state.value == 1:
#             fig=plt.figure()
#             ax=fig.add_axes([0,0,1,1])
#             ax.scatter(x, y, color='r')
#             ax.set_xlabel('time(s)')
#             ax.set_ylabel('pressure(psi)')
#             ax.set_title('plot bitch')
#             plt.show()
            return
                  
        
# initialize
file = open("launchpress.txt", "a")
file.write("New Launch Values\n")
charge  = True
pressures = Array('f', range(3))
state = Value('i', 0)

read_trans_in_background = Process(target=read_trans, args=(pressures,state))
read_trans_in_background.start()

# charge compressor
# time.sleep(2)
while charge == True:
    time.sleep(.20)
    GPIO.output(comp, 0)
    if pressures[0] >= FP:
        charge = False
    time.sleep(.25)
    
# Launch sequence
GPIO.output(comp, 1)
time.sleep(3)
GPIO.output(vent_sol, 0)
time.sleep(1)
GPIO.output(launch_sol,0)
time.sleep(2)
GPIO.output(safety_sol,0)
time.sleep(3)
GPIO.output(safety_sol, 1)
time.sleep(2)
GPIO.output(vent_sol, 1)
time.sleep(2)
GPIO.output(launch_sol, 1)
LP = 0



file.close()
GPIO.cleanup()
state.value = 1 # we done
print("done")
# read_trans_in_background.terminate()