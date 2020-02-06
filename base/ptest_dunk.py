
import RPi.GPIO as GPIO
import time
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as GPIOp
import numpy as np

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Pinouts for Relay Connectors
comp       = 16
safety_sol = 13
vent_sol   = 15
launch_sol = 11
values = np.zeros(8)

LP = input("Enter Launch Pressure: ")
LP = LP + 15.4
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

#initialize
charge  = True
while charge == True:
	value = mcp.read_adc(0)
	print('| %5.3f Psi |' %(value/10.23 - 15.4))
	print("______________________")
	time.sleep(.20)
	GPIO.output(comp, 0)
	if value >= FP:
		charge = False
	time.sleep(.25)
GPIO.output(comp, 1)
time.sleep(4)
GPIO.output(vent_sol, 0)
time.sleep(1)
GPIO.output(safety_sol,0)
time.sleep(2)
GPIO.output(launch_sol,0)
time.sleep(1)
GPIO.output(safety_sol, 1)
time.sleep(1)
GPIO.output(vent_sol, 1)
time.sleep(1)
GPIO.output(launch_sol, 1)
LP = 0

GPIO.cleanup()
