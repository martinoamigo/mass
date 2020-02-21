import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# Pinouts for Relay Connectors
comp       = 16
safety_sol = 13
vent_sol   = 11
launch_sol = 15
sol_act1   = 31
sol_act2   = 33
lin_act1   = 35
lin_act2   = 37

# Set Pins
GPIO.setup(comp, GPIO.OUT)
GPIO.setup(safety_sol, GPIO.OUT)
GPIO.setup(vent_sol, GPIO.OUT)
GPIO.setup(launch_sol, GPIO.OUT)
GPIO.setup(sol_act1, GPIO.OUT)
GPIO.setup(sol_act2, GPIO.OUT)
GPIO.setup(lin_act1, GPIO.OUT)
GPIO.setup(lin_act2, GPIO.OUT)

# Clear Pins
GPIO.output(comp, 1)
GPIO.output(safety_sol, 1)
GPIO.output(vent_sol, 1)
GPIO.output(launch_sol, 1)
GPIO.output(sol_act1, 1)
GPIO.output(sol_act2, 1)
GPIO.output(lin_act1, 1)
GPIO.output(lin_act2, 1)
GPIO.cleanup()
