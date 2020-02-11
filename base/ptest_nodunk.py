import RPi.GPIO as GPIO
import time
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as GPIOp
import numpy as np
<<<<<<< HEAD
from multiprocessing import Process, Value, Array
=======
import os
import datetime

now = datetime.datetime.now() # Current Date and Time
date = now.strftime('%Y_%m_%d')
time = now.strftime('%Hh_%Mm_%Ss')
path = 'Desktop/Pneumatic_Logs/' + date
try:
    os.mkdir(path)
except OSError:
    print('Creation of directory ', path, ' failed')
file = open(path + str(now) + ".txt", "a")
file.write("P(psi), t(s),\n")
>>>>>>> 2dc606bd07f916a1f4b2e140897637d63c14d7ce

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

<<<<<<< HEAD
def read_trans(value):
    start = time.time()
    j = 0
    while True:
        time.sleep(.02)
        for i in range(3):
            value[i] = mcp.read_adc(i)
        file.write('| {0:.4f} | {1:.4f} | {2:.4f} | time: {3:.4f}'.format(value[0]/10.23 - 15.4, value[1]/10.23 - 15.4, value[2]/10.23 - 15.4, time.time() - start))
        if j % 10 == 0:
            print('| {0:.4f} | {1:.4f} | {2:.4f} | time: {3:.4f}'.format(value[0]/10.23 - 15.4, value[1]/10.23 - 15.4, value[2]/10.23 - 15.4, time.time() - start))
        j += 1
        
# initialize
file = open("launchpress_2.txt", "a")
file.write("New Launch Values\n")
=======
#initialize
>>>>>>> 2dc606bd07f916a1f4b2e140897637d63c14d7ce
charge  = True
value = Array('f', range(3))

read_trans_in_background = Process(target=read_trans, args=(value,))
read_trans_in_background.start()

# charge compressor
while charge == True:
<<<<<<< HEAD
    time.sleep(.20)
    GPIO.output(comp, 0)
    if value[0] >= FP:
        charge = False
    time.sleep(.25)
    
# Launch sequence
=======
	value = mcp.read_adc(0)
	tm = tm + 0.2
	file.write(str(value/10.23 - 15.4) + ", " + str(tm) + ",\n")
	print('| %5.3f Psi |' %(value/10.23 - 15.4))
	print("______________________")
	time.sleep(.20)
	GPIO.output(comp, 0)
	if value >= FP:
		charge = False
	time.sleep(.25)
>>>>>>> 2dc606bd07f916a1f4b2e140897637d63c14d7ce
GPIO.output(comp, 1)
time.sleep(4)
GPIO.output(vent_sol, 0)
time.sleep(1)
GPIO.output(launch_sol,0)
time.sleep(2)
GPIO.output(safety_sol,0)
time.sleep(3)
GPIO.output(safety_sol, 1)
time.sleep(2)
GPIO.output(vent_sol, 1)
time.sleep(4)
GPIO.output(launch_sol, 1)
LP = 0



file.close()
GPIO.cleanup()
read_trans_in_background.terminate()