import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# Pinouts for Relay Connectors
comp       = 16
safety_sol = 13
vent_sol   = 11
launch_sol = 15

# Set Pins
GPIO.setup(comp, GPIO.OUT)
GPIO.setup(safety_sol, GPIO.OUT)
GPIO.setup(vent_sol, GPIO.OUT)
GPIO.setup(launch_sol, GPIO.OUT)

# Clear Pins 
GPIO.output(comp, 1)
GPIO.output(safety_sol, 1)
GPIO.output(vent_sol, 1)
GPIO.output(launch_sol, 1)

# Initialize Pressures
pressure = 0
launch_pressure = 35

Pressurize = True
Launch = True

if(Pressurize == True):
	GPIO.output(comp,0)
	while(pressure < launch_pressure):
		pressure += 1
		time.sleep(1)
		GPIO.output(comp, 0)
	GPIO.output(comp, 1)
	Pressurize = False

if(Launch == True):
	time.sleep(3)
	GPIO.output(vent_sol, 0)
	time.sleep(3)
	GPIO.output(safety_sol, 0)
	time.sleep(3)
	GPIO.output(launch_sol, 0)
	time.sleep(5)
	GPIO.output(safety_sol, 1)
	time.sleep(2)
	GPIO.output(vent_sol, 1)
	time.sleep(2)
	GPIO.output(launch_sol, 1)
	Launch = False
'''
if(Launch == True):
	time.sleep(3)
	GPIO.output(vent_sol, 0)
	time.sleep(3)
	GPIO.output(safety_sol, 0)
	time.sleep(3)
	GPIO.output(vent_sol, 1)
	time.sleep(3)
'''
GPIO.cleanup()

